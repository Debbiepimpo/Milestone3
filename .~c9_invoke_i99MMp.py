import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["MONGO_DBNAME"]="CookBook"
app.config["MONGO_URI"]=os.getenv("MONGO_URI")

mongo=PyMongo(app)

@app.route("/")
def index():
    return render_template("index.html")
    
# It logs into user's coobook site
@app.route('/sign_in')
def sign_in():
    session.pop('logged_in', None)
    session.pop('user', None)
    return render_template('login.html')   
   
@app.route('/login',methods=['GET','POST'])
def login():
    users=mongo.db.users
    username=request.form['user']
    #Search into the data base on mongoDB the username requested by the user
    user=users.find_one({"user":username})
    #If the username match on mongoDB, this checks if the password match with the username
    if user:
        password=user['password']
        if request.form['password']==password:
            session['user']=username
            session['logged_in']=True
            return redirect(url_for('mypage'))
        else:
            flash('Wrong password')    
            return redirect(url_for('sign_in'))
    else:        
        flash('Wrong username')    
        return redirect(url_for('sign_in')) 
        
# Registration template for new user.
@app.route('/newuser')
def newuser():
    return render_template('newuser.html')  

# It finish the submision of a new user.
@app.route('/newuser/register', methods=['GET','POST'])
def register():
    user={}
    users=mongo.db.users
    username=request.form['user']
    # Checks if the username requested by the user is in use 
    if users.find_one({"user":username}):
        flash('Username already taken. Please try another one.')
        return redirect(url_for('newuser'))
    else: 
        # When the username is valid as new user, this redirect the user to the login page
        user["user"]=username
        user["password"]=request.form['password']
        users.insert_one(user)
        flash('User registered successfully. You can now login.')
        return redirect(url_for('sign_in'))
        
@app.route('/mypage')
def mypage():
    recipes=mongo.db.recipes.find().sort('_id', -1).limit(4) #display the latest 6 recipes
    return render_template('mypage.html',recipes=recipes)
            
@app.route('/recipes',defaults={'page': 1})
@app.route('/recipes/page/<page>')
def recipes(page):
    filters={}
    message=""
    #Allergies not being checked by the results
    if "excludedAllergy[]" in request.args:
        filters['excluded']=request.args.getlist('excludedAllergy[]')
        excludedParams={"allergies":{'$nin':filters['excluded']}}
    else:
        excludedParams={}
        filters['excluded']=[]
        
   #Check if user search by Browse(with cuisine or diet)
    if "browse" in request.args:
        filters['browse']=request.args.get("browse")
        tmpParams = [];
        tmpParams.append({"cuisine":request.args.get("browse")})
        tmpParams.append({"diet":request.args.get("browse")})
        
        if request.args.get("browse")=="All":
            findParams={}
        else:
            findParams = { '$or': tmpParams }
    else:
        findParams = {}
        
    '''
    When the user looked for a recipe by a keyword,  
    it displays the results applying the filters required for that search result
    '''
    if "keyword" in request.args and request.args.get('keyword')!="":
        keyword = request.args.get('keyword')
        mongo.db.recipes.create_index([('$**','text')])
        findParams['$text'] = { '$search': keyword  }
    else:
        keyword=None
   
   # Sort as latest recipes by default.
    sortField = "_id"
    sortOrder = -1
    
    # Get parameters based on the imput: Sort
    if "sort" in request.args:
        filters['sort']=request.args.get("sort")
        if request.args.get('sort')=="Latest Entry First":
            sortField = '_id'
            sortOrder = -1
        elif request.args.get('sort')=="Oldest Entry First":
            sortField = '_id'
            sortOrder = 1
            
    # Looking for the recipes based from the imput above
    if findParams and filters['excluded']:
        recipes_all = mongo.db.recipes.find({'$and':[findParams,excludedParams]}).sort(sortField,sortOrder)
    
    if findParams and not filters['excluded']:
        recipes_all = mongo.db.recipes.find(findParams).sort(sortField,sortOrder)
        
    if  filters['excluded'] and not findParams:
        recipes_all = mongo.db.recipes.find(excludedParams).sort(sortField,sortOrder)
    
    if not filters['excluded'] and not findParams:
        recipes_all = mongo.db.recipes.find().sort(sortField,sortOrder)
    
    page_size=10 #It set how many recipes will be maximum display per page
    recipes_total= recipes_all.count() #Number of total recipes displayed
    
    #If there are no recipes, it will be displayed this message.
    if recipes_total==0:
        message = "Unfortunately there are not results found by the search criteria. Why no try different filters?"
       
    page=int(page)
    skips = page_size * (int(page) - 1) #Skip won't be applied for page 1
    '''
    add 1 to check if there are any recipes left after the actual page. If the result is FALSE 
    this means there aren't any more recipes and the Next Page button won't be displayed
    
    '''
    recipes=recipes_all.skip(skips).limit(page_size + 1) 
    recipes_length=recipes.count(True)
  
    #Get all th Lists from DB
    _diet=mongo.db.diet.find()
    diet=[diet for diet in _diet]
    _cuisine=mongo.db.cuisine.find()
    cuisine=[cuisine for cuisine in _cuisine ]
    _allergies=mongo.db.allergies.find()
    allergies=[allergy for allergy in _allergies]
    
    
    return render_template('recipes.html',page=page,recipes=recipes,recipes_count=recipes_total,
    _diet=diet,_cuisine=cuisine,_allergies=allergies,filters=filters,
    page_size=page_size,recipes_length=recipes_length,keyword=keyword,message=message)

    
#User can view his/her own recipes/cookbook
@app.route('/myrecipes',defaults={'page':1})
@app.route('/myrecipes/page/<page>')
def myrecipes(page):
    #If not logged in user is redirected to Autentication page
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('sign_in'))
        
    #Otherwise store username in a session variable
    user = session['user']
    #Display ONLY user's recipes
    recipes_total_user= mongo.db.recipes.find({ 'user': user  }).sort('_id', -1)
    recipes_total_count=recipes_total_user.count()
    #If there are no recipes to display, how this message
    message=""
    if recipes_total_count==0:
        message="You don't have any recipes yet"
    
    #Same logic as in Recipes
    page_size=8
    page=int(page)
    skips = page_size * (int(page) - 1)
    recipes_per_page=recipes_total_user.skip(skips).limit(page_size + 1)
    recipes_length=recipes_per_page.count(True)
    
    return render_template('myrecipes.html',recipes=recipes_per_page,page_size=page_size,page=page,
            recipes_length=recipes_length,total_recipes=recipes_total_count,message=message)

#User cand delete ONLY own recipes   
@app.route('/del_recipe/<recipe_id>')
def del_recipe(recipe_id):
    #Check if logged in
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('sign_in')) 
    '''
    Check if user from session and from recipe and from Recipe match
    if not user will be redirected to sign_in. If the match is 
    True the recipe will be deleted and user redirected to his/her recipes
    '''
    user=session['user']    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    if recipe['user'] != user:
        return redirect(url_for('sign_in'))
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    flash('Your recipe was successfully deleted')
    return redirect(url_for('myrecipes'))

@app.route('/editrecipe/<recipe_id>', methods = ['GET','POST'])
def editrecipe(recipe_id):
    if session.get('logged_in') is None:
        flash("Please login if you would like to make any modification on the cookbook")
        return redirect(url_for('sign_in')) 
    user = session['user']    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    
    #in order to avoid users editing recipes that are not theirs
    if recipe['user'] != user:
        return redirect(url_for('sign_in'))
    
    #Get diet,allergies,measurements lists
    _diet=mongo.db.diet.find()
    diet=[diet for diet in _diet]
    _cuisine=mongo.db.cuisine.find()
    cuisine=[cuisine for cuisine in _cuisine ]
    _allergies=mongo.db.allergies.find()
    allergies=[allergy for allergy in _allergies]
    _measurements=mongo.db.measurements.find()
    measurements=[measurement for measurement in _measurements]
    
    ingredient_length=len(recipe['ingredients'])
    instructions_length=len(recipe['instructions'])
    
    return render_template('editrecipe.html',recipe=recipe,
                            _diet=diet,_cuisine=cuisine,
                            _allergies=allergies,measurements=measurements,
                            ingredient_length=ingredient_length,instructions_length=instructions_length)
                        
@app.route('/updaterecipe/<recipe_id>',methods=['GET','POST'])
def updaterecipe(recipe_id):
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('sign_in')) 
    
    message=""
    keys=[] # This will be used to store the keys from empty fields
    #Get the recipe as is from DB
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    #Get all the data input from the form and transform into dictionary
    recipes=request.form.to_dict()
  
    ingredient_length=len(request.form.getlist("ingredient-name[]"))
    instructions_length=len(request.form.getlist("instructions"))
    
    #Create an array with name, quantity and measurements of each ingredient
    headers = ('name', 'quantity','measurements')
    values = (
        request.form.getlist('ingredient-name[]'),
        request.form.getlist('ingredient-quantity[]'),
        request.form.getlist('ingredient-measurements[]'),
    )
    items = [{} for i in range(len(values[0]))]
    for x,i in enumerate(values):
        for _x,_i in enumerate(i):
            items[_x][headers[x]] = _i
    
    #Get instructions and allergies from the form
    form_allergies = request.form.getlist("allergies[]")
    print(form_allergies)
    form_instructions = request.form.getlist("instructions")
    
    #Delete current name,quantity and measurements as they are not in the format required for DB
    del recipes["ingredient-name[]"]
    del recipes["ingredient-quantity[]"]
    del recipes["ingredient-measurements[]"]
    del recipes["instructions"]
   
    #Insert data into dictionary
    recipes["ingredients"]=items
    recipes["instructions"]=form_instructions
    if form_allergies:
        del recipes["allergies[]"]
        recipes["allergies"]=form_allergies
    else:
        recipes["allergies"]=["None"]
        
    if request.form.get('submit') == 'submit':
        #If no link is provided a default image is used
        if request.form["image"]=="":
            request.form["image"]="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1024px-Good_Food_Display_-_NCI_Visuals_Online.jpg"

        # To get keys which having zero length value(checks only allergies, description and title):
        keys = [key for key,val in recipes.items() if not val]
        #Chek ingredients and instructions
        keys_ingredients = [val for val in recipes["ingredients"] if not val["measurements"] or not val["name"] or not val["quantity"]]
        keys_instructions = [val for val in recipes["instructions"] if not val]
        #If diet not in the recipes-dictionary-form
        if 'diet' not in recipes:
            keys.append('diet')
        #If diet not in the recipes-dictionary-form    
        if 'cuisine' not in recipes:
            keys.append('cuisine')
        #If ingredients and instructions have missing values append to the array containing empy keys
        if keys_ingredients:
            keys.append('ingredients')
        if keys_instructions:
            keys.append('instructions')
        if keys:
            message="Please fill in the following data"
        else:
            recipes=mongo.db.recipes
            recipes.update_one({'_id': ObjectId(recipe_id)},{"$set":recipes})  
            flash('Your recipe was successfully updated')
            return redirect(url_for('myrecipes'))
        
    elif request.form.get('submit') == 'addInstruction':
        instructions_length += 1
    elif request.form.get('submit') == 'addIngredient': 
        ingredient_length += 1
    elif request.form.get('submit') == 'del_instruction':
        instructions_length -= 1 
    elif request.form.get('submit') == 'del_ingredient':  
        ingredient_length -= 1
    _diet=mongo.db.diet.find()
    diet=[diet for diet in _diet]
    _cuisine=mongo.db.cuisine.find()
    cuisine=[cuisine for cuisine in _cuisine ]
    _allergies=mongo.db.allergies.find()
    allergies=[allergy for allergy in _allergies]
    _measurements=mongo.db.measurements.find()
    measurements=[unit for unit in _measurements]
    
    return render_template('editrecipe.html',recipe=recipe,recipes=recipes,
                            _diet=diet,_cuisine=cuisine,
                            _allergies=allergies,measurements=measurements,
                            ingredient_length=ingredient_length,instructions_length=instructions_length,
                            keys=keys,message=message)

@app.route('/addrecipe')
def addrecipe():
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('sign_in')) 
    allergies=mongo.db.allergies.find()
    _diet=mongo.db.diet.find()
    diet=[diet for diet in _diet]
    _cuisine=mongo.db.cuisine.find()
    cuisine=[cuisine for cuisine in _cuisine ]
    _measurements=mongo.db.measurements.find()
    measurements=[measurement for measurement in _measurements]
    instructions = 2
    ingredients=2
    recipes={}
    return render_template('addrecipe.html',_allergies=allergies,
    _diet=diet,_cuisine=cuisine,measurements=measurements,instructions=instructions,
    recipes=recipes,ingredients=ingredients)

@app.route('/insertrecipe', methods =["POST","GET"])
def insertrecipe():
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('sign_in')) 
    
    message=""
    keys=[] #keys of fields with no values will be stored
    
    #Units, cuisine, diet and allergies lists
    _measurements=mongo.db.measurements.find()
    measurements=[measurement for measurement in _measurements]
    _cuisine=mongo.db.cuisine.find()
    cuisine=[cuisine for cuisine in _cuisine ]
    _diet=mongo.db.diet.find()
    diet=[diet for diet in _diet]
    _allergies=mongo.db.allergies.find()
    allergies=[allergy for allergy in _allergies]
    
    instructions = len(request.form.getlist("instructions"))
  
    ingredientsList = request.form.getlist("ingridientName[]")
    ingredients = len(ingredientsList)
    
    #Array of tuples with name,quantity and measurements for each ingredient
    recipes=request.form.to_dict()
    headers = ('name', 'quantity','measurements')
    values = (
        request.form.getlist('ingridientName[]'),
        request.form.getlist('ingridientQuantity[]'),
        request.form.getlist('ingridientMeasurements[]'),
    )
    items = [{} for i in range(len(values[0]))]
    for x,i in enumerate(values):
        for _x,_i in enumerate(i):
            items[_x][headers[x]] = _i
    
    form_allergies = request.form.getlist("allergies[]")
    form_instructions = request.form.getlist("instructions")
    
    del recipes["ingridientName[]"]
    del recipes["ingridientQuantity[]"]
    del recipes["ingridientMeasurements[]"]
    del recipes["instructions"]
    
    if form_allergies:
        del recipes["allergies[]"]
        recipes["allergies"]=form_allergies
    else:
        recipes["allergies"]=["None"]
    
    recipes["ingredients"]=items
    recipes["instructions"]=form_instructions
    recipes["user"]=session['user']
  
    if request.form.get('submit') == 'submit':
        
        if recipes["image"]=="":
            #if no image provided the default image is used
            recipes["image"]="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1024px-Good_Food_Display_-_NCI_Visuals_Online.jpg"
        
        # To get keys which having zero length value(checks only allergies, description and title):
        keys = [key for key,val in recipes.items() if not val]
        #Chek ingredients and instructions
        keys_ingredients = [val for val in recipes["ingredients"] if not val["measurements"] or not val["name"] or not val["quantity"]]
        keys_instructions = [val for val in recipes["instructions"] if not val]
        #If diet not in the recipes-dictionary-form
        if 'diet' not in recipes:
            keys.append('diet')
        #If diet not in the recipes-dictionary-form    
        if 'cuisine' not in recipes:
            keys.append('cuisine')
        #If ingredients and instructions have missing values append to the array containing empy keys
        if keys_ingredients:
            keys.append('ingredients')
        if keys_instructions:
            keys.append('instructions')
        if keys:
            message="Please fill in the following data:"
        else:
            recipes["view"]=0
            recipes=mongo.db.recipes
            recipes.insert_one(recipes)
            flash('Your recipe was successfully added')
            return redirect(url_for('myrecpies'))
        
    elif request.form.get('submit') == 'addInstruction':
        # add instruction
        instructions += 1
    elif request.form.get('submit') == 'addIngredient': 
        ingredients += 1
    elif request.form.get('submit') == 'del_instruction':
        instructions -= 1 
    elif request.form.get('submit') == 'del_ingredient':  
        ingredients -= 1
 
    return render_template('addrecipe.html', instructions=instructions, form_instructions=form_instructions, recipes=recipes,
    ingredients=ingredients,measurements=measurements,_cuisine=cuisine, _diet=diet,
    _allergies=allergies,form_allergies=form_allergies,message=message,keys=keys )                                
    
@app.route("/favourites")
def favourites():
    return render_template("favourites.html")
    
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)