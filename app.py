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
    recipes=mongo.db.recipes.find().sort('_id', -1).limit(3) #display the latest 6 recipes
    return render_template('mypage.html',recipes=recipes)
            
@app.route('/recipes',defaults={'page': 1})
@app.route('/recipes/page/<page>')
def recipes(page):
    filters={}
    message=""
    
    #Allergies not being checked by the results
    if "excluded_allergy[]" in request.args and request.args.get('submit') =="Submit":
        filters['excluded']=request.args.getlist('excluded_allergy[]')
        excludedParams={"allergies":{'$nin':filters['excluded']}}
    else:
        excludedParams={}
        filters['excluded']=[]
        
   #Check if user search by Browse(with cuisine or diet)
    if "browse" in request.args and request.args.get('browse')!="None" and request.args.get('submit') =="Submit":
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
    # When the user looked for a recipe by a keyword,  
    # it displays the results applying the filters required for that search result

    if "keyword" in request.args and request.args.get('keyword')!="" and request.args.get('submit') =="Submit":
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
        if request.args.get('sort')=="Latest Recipe First":
            sortField = '_id'
            sortOrder = -1
        elif request.args.get('sort')=="Oldest Recipe First":
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
    
    page_size=9 #It set how many recipes will be maximum display per page
    recipes_total= recipes_all.count() #Number of total recipes displayed
    
    #If there are no recipes, it will be displayed this message.
    if recipes_total==0:
        message = "Unfortunately there are not results found by the search criteria. Why no try different filters?"
       
    page=int(page)
    skips = page_size * (int(page) - 1) #Skip won't be applied for page 1
    '''
    add 1 to check if there are any recipes left after the actual page. If the result is FALSE 
    this means there aren't any more recipes and the 'Next Page' button won't be displayed
    
    '''
    recipes=recipes_all.skip(skips).limit(page_size + 1) 
    recipes_length=recipes.count(True)
  
    # Get Diet, Cuisine and Allergens Lists from DB
    _diet=mongo.db.diet.find()
    diet=[diet for diet in _diet]
    _cuisine=mongo.db.cuisine.find()
    cuisine=[cuisine for cuisine in _cuisine ]
    _allergies=mongo.db.allergies.find()
    allergies=[allergy for allergy in _allergies]
    
    
    return render_template('recipes.html',page=page,recipes=recipes,recipes_count=recipes_total,
    _diet=diet,_cuisine=cuisine,_allergies=allergies,filters=filters,
    page_size=page_size,recipes_length=recipes_length,keyword=keyword,message=message)

    
# The user can view his own recipes on their own cookbook
@app.route('/myrecipes',defaults={'page':1})
@app.route('/myrecipes/page/<page>')
def myrecipes(page):
    # If the user is not logged the page will be redirected to Login page.
    if session.get('logged_in') is None:
        flash("Please login for getting full access to your website")
        return redirect(url_for('sign_in'))
        
    # When the user is in session, the  username is stored on a variable
    user = session['user']
    # It will show only recipes that belongs to the user.
    recipes_total_user= mongo.db.recipes.find({ 'user': user  }).sort('_id', -1)
    recipes_total_count=recipes_total_user.count()
    # If the user hasn't got any recipes on his cookbook to display then this message wil be display
    message=""
    if recipes_total_count==0:
        message="Sorry, there's no recipes to display"
    
    # It set how many recipes will be maximum display per page (same as the recipes above) 
    page_size=9
    page=int(page)
    skips = page_size * (int(page) - 1)
    recipes_per_page=recipes_total_user.skip(skips).limit(page_size + 1)
    recipes_length=recipes_per_page.count(True)
    
    return render_template('myrecipes.html',recipes=recipes_per_page,page_size=page_size,page=page,
            recipes_length=recipes_length,total_recipes=recipes_total_count,message=message)

# The user will be able to delete exclusively his own recipes  
@app.route('/del_recipe/<recipe_id>')
def del_recipe(recipe_id):
    # Make sure if the user is logged on.
    if session.get('logged_in') is None:
        flash("Please login for getting full access to your website")
        return redirect(url_for('sign_in')) 
    '''
    This make sure if the user is logged with his username and check recipe if it match,
    if the user is not logged, he will be redirected to sign_in. But if the user is logged 
    and the recipe match with the recipe written under the username logged, the recipe will
    be deleted and user will be redirected to the recipes on his own cookbook.
    '''
    user=session['user']    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    if recipe['user'] != user:
        return redirect(url_for('sign_in'))
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    flash('The recipe is now delete.')
    return redirect(url_for('myrecipes'))

@app.route('/editrecipe/<recipe_id>', methods = ['GET','POST'])
def editrecipe(recipe_id):
    if session.get('logged_in') is None:
        flash("Please login for getting full access to your website")
        return redirect(url_for('sign_in')) 
    user = session['user']    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    
    # As being on the delete above, the user will be able to edit his own recipes
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
        flash("Please login for getting full access to your website.")
        return redirect(url_for('sign_in')) 
    
    message=""
    keys=[] # This will store the keys from the fields that are empty
    # Get the recipe from mongoDB
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    # Take the data written into the form and convert into dictionary
    recipes=request.form.to_dict()
  
    ingredient_length=len(request.form.getlist("ingredientName[]"))
    instructions_length=len(request.form.getlist("instructions"))
    
    # This will create an array with the name, the quantity and the measurements of each ingredient
    headers = ('name', 'quantity','measurements')
    values = (
        request.form.getlist('ingredientName[]'),
        request.form.getlist('ingredientQuantity[]'),
        request.form.getlist('ingredientMeasurements[]'),
    )
    items = [{} for i in range(len(values[0]))]
    for x,i in enumerate(values):
        for _x,_i in enumerate(i):
            items[_x][headers[x]] = _i
    
    # Take instructions and allergies writen into the form
    form_allergies = request.form.getlist("allergies[]")
    print(form_allergies)
    form_instructions = request.form.getlist("instructions")
    
    #Delete the name, the quantity and the measurements when this are not required by the format for mongoDB
    del recipes["ingredientName[]"]
    del recipes["ingredientQuantity[]"]
    del recipes["ingredientMeasurements[]"]
    del recipes["instructions"]
   
    # Put the data into the dictionary
    recipes["ingredients"]=items
    recipes["instructions"]=form_instructions
    
    if form_allergies:
        del recipes["allergies[]"]
        recipes["allergies"]=form_allergies
    else:
        recipes["allergies"]=["None"]
        
    if request.form.get('submit') == 'submit':
        #If there's no image link provided a image settled as default will be used
        if request.form["image"]=="":
            request.form["image"]="../static/img/default.jpg"

        # Check allergies, description and recipe name only, to make sure if the key length has a value equals to 0 
        keys = [key for key,val in recipes.items() if not val]
        # Check also ingredients and instructions
        keys_ingredients = [val for val in recipes["ingredients"] if not val["measurements"] or not val["name"] or not val["quantity"]]
        keys_instructions = [val for val in recipes["instructions"] if not val]
         # If cuisine not able at the dictionary    
        if 'cuisine' not in recipes:
            keys.append('cuisine')
        # If diet is not able at the dictionary 
        if 'diet' not in recipes:
            keys.append('diet')
        # If ingredients and instructions have no values into the array, then it will contain empy keys
        if keys_ingredients:
            keys.append('ingredients')
        if keys_instructions:
            keys.append('instructions')
        if keys:
            message="This fields are required. Please fill them in."
        else:
            recipes=mongo.db.recipes
            recipes.update_one({'_id': ObjectId(recipe_id)},{"$set":recipes})  
            flash('The recipe has being updated')
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
    
    recipes = mongo.db.recipes
    recipe.update( {'_id': ObjectId(recipe_id)},
    {
        'user':request.form.get('user'),
        'image':request.form.get('recipe_image'),
        'recipeName': request.form.get('recipeName'),
        'allergy_name': request.form.get('allergy_name'),
        'cuisine_name':request.form.get('cuisine_name'),
        'ingredients': request.form.get('ingredientName, ingredientQuantity, ingredientMeasurements'),
        'instructions':request.form.get('instructions')
    })
    
    return render_template('editrecipe.html',recipe=recipe,recipes=recipes,
                            _diet=diet,_cuisine=cuisine,
                            _allergies=allergies,measurements=measurements,
                            ingredient_length=ingredient_length,instructions_length=instructions_length,
                            keys=keys,message=message)

@app.route('/addrecipe')
def addrecipe():
    if session.get('logged_in') is None:
        flash("Please login for getting full access to your website")
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
        flash("Please login for getting full access to your website")
        return redirect(url_for('sign_in')) 
    
    message=""
    keys=[] # It will store keys of empty fields

    # This are the list from mongoDB
    _measurements=mongo.db.measurements.find()
    measurements=[measurement for measurement in _measurements]
    _cuisine=mongo.db.cuisine.find()
    cuisine=[cuisine for cuisine in _cuisine ]
    _diet=mongo.db.diet.find()
    diet=[diet for diet in _diet]
    _allergies=mongo.db.allergies.find()
    allergies=[allergy for allergy in _allergies]
    
    instructions = len(request.form.getlist("instructions"))
  
    ingredientsList = request.form.getlist("ingredientName[]")
    ingredients = len(ingredientsList)
    
    # Array of tuples for each ingredient
    recipe=request.form.to_dict()
    headers = ('name', 'quantity','measurements')
    values = (
        request.form.getlist('ingredientName[]'),
        request.form.getlist('ingredientQuantity[]'),
        request.form.getlist('ingredientMeasurements[]'),
    )
    items = [{} for i in range(len(values[0]))]
    for x,i in enumerate(values):
        for _x,_i in enumerate(i):
            items[_x][headers[x]] = _i
    
    form_allergies = request.form.getlist("allergies[]")
    form_instructions = request.form.getlist("instructions")
    
    # To delete the extra lines of ingredients and instructions
    del recipe["ingredientName[]"]
    del recipe["ingredientQuantity[]"]
    del recipe["ingredientMeasurements[]"]
    del recipe["instructions"]
    
    
    if form_allergies:
        del recipe["allergies[]"]
        recipe["allergies"]=form_allergies
    else:
        recipe["allergies"]=["None"]
    
    recipe["ingredients"]=items
    recipe["instructions"]=form_instructions
    recipe["user"]=session['user']
    
  
    if request.form.get('submit') == 'submit':
        
        if recipe["image"]=="":
            # If there's no image link provided a image settled as default will be used
            recipe["image"]="http://sozkibris.com/wp-content/uploads/2017/10/3dbf0726e1dc41349d0.jpg"
        
        # Check allergies, description and recipe name only, to make sure if the key length has a value equals to 0 
        keys = [key for key,val in recipe.items() if not val]
        # Check  also ingredients and instructions
        keys_ingredients = [val for val in recipe["ingredients"] if not val["measurements"] or not val["name"] or not val["quantity"]]
        keys_instructions = [val for val in recipe["instructions"] if not val]
         # If cuisine not able at the dictionary    
        if 'cuisine' not in recipe:
            keys.append('cuisine')
        # If diet is not able at the dictionary 
        if 'diet' not in recipe:
            keys.append('diet')
        # If ingredients and instructions have no values into the array, then it will contain empy keys
        if keys_ingredients:
            keys.append('ingredients')
        if keys_instructions:
            keys.append('instructions')
        if keys:
            message="This fields are required. Please fill them in."
        else:
            recipes=mongo.db.recipes
            recipes.insert_one(recipe)
            flash('The recipe has being added.')
            return redirect(url_for('myrecipes'))
        
    elif request.form.get('submit') == 'addInstruction':
        instructions += 1
    elif request.form.get('submit') == 'addIngredient': 
        ingredients += 1
    elif request.form.get('submit') == 'del_instruction':
        instructions -= 1 
    elif request.form.get('submit') == 'del_ingredient':  
        ingredients -= 1

    return render_template('addrecipe.html', instructions=instructions, form_instructions=form_instructions, recipes=recipe,
    ingredients=ingredients,measurements=measurements,_cuisine=cuisine, _diet=diet,
    _allergies=allergies,form_allergies=form_allergies,message=message,keys=keys )                                


@app.route('/viewrecipe/<recipe_id>')
def viewrecipe(recipe_id):
    if session.get('logged_in') is None:
        flash("Please login for getting full access to your website")
        return redirect(url_for('sign_in')) 
    
    user=session['user']
    
    the_recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    exist=mongo.db.favourites.find_one({"recipe_id":recipe_id,"user":user})
    favouriteExist=False;
    if exist is None:
        favouriteExist=True
        
    return render_template('viewrecipe.html',recipe=the_recipe,favourite=favouriteExist)

@app.route('/favourites',defaults={'page':1})
@app.route('/favourites/page/<page>')
def favourites(page):
    # If the user is not logged the page will be redirected to Login page.
    if session.get('logged_in') is None:
        flash("Please login for getting full access to your website")
        return redirect(url_for('sign_in'))
    
    # When the user is in session, the  username is stored on a variable
    user = session['user']
    # It will show only recipes that belongs to the user.
    favourites_total_user= mongo.db.favourites.find({ 'user': user  }).sort('_id', -1)
    favourites_total_count=favourites_total_user.count()
    # If the user hasn't got any recipes on his cookbook to display then this message wil be display
    message=""
    recipes_total_user=[]
    if favourites_total_count==0:
        message="Sorry, there's no recipes to display"
    else:
        for favourite in favourites_total_user :
            recipes_total_user.append(mongo.db.recipes.find_one({"_id":ObjectId(favourite.get('recipe_id'))}))
        recipes_total_count=len(recipes_total_user)

        # It set how many recipes will be maximum display per page (same as the recipes above) 
        page_size=9
        page=int(page)
        skips=page_size * (int(page) - 1)
        recipes_per_page=recipes_total_user[skips:skips+(page_size + 1)]       
        recipes_length=len(recipes_per_page)
        
        
    return render_template('favourites.html',recipes=recipes_per_page,page_size=page_size,page=page,
            recipes_length=recipes_length,total_recipes=recipes_total_count,message=message)

@app.route('/insertfavourite/<recipe_id>', methods =["POST","GET"])
def insertfavourite(recipe_id):
    if session.get('logged_in') is None:
        flash("Please login for getting full access to your website")
        return redirect(url_for('sign_in')) 
    
    user=session['user']
    favourites=mongo.db.favourites
    recipe={'recipe_id':recipe_id,'user':user}
    favourites.insert_one(recipe)
    flash('The recipe has being added to favourites.')
    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    
    return render_template('viewrecipe.html',recipe=recipe,favourite=False)
    
@app.route('/removefavourite/<recipe_id>', methods =["POST","GET"])
def removefavourite(recipe_id):
    if session.get('logged_in') is None:
        flash("Please login for getting full access to your website")
        return redirect(url_for('sign_in')) 
    
    user=session['user']
    
    favourite=mongo.db.favourites.find_one({"recipe_id":recipe_id,"user":user})
    favouriteId=favourite.get('_id')
    mongo.db.favourites.remove({'_id':ObjectId(favouriteId)})
    flash('The recipe has being removed from favourites.')
    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    return render_template('viewrecipe.html',recipe=recipe,favourite=True)
    
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)