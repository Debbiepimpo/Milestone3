# My Cookbook

I have the pleasure of introducing my Data-Centric Development Project. My Cookbook was being created with Python, Flask and MnogoDB and the purpose of this project is to create an interactive database of recipes that allows the user to create, read, update and delete (CRUD) recipes and also to share with another users and add their favourites recipes to favourites. My Cookbook can only be used by registered users but non-registered users can see any recipe if wanted.

The idea of this website is to have an online storage for look up, create and save recipes. Also the simplicity makes this website  easy to use with anything to guess for the interaction on it  b the user. The target users for My Cookbook is any one who has the necessity to store recipes online. Traditional media such as books or magazines are continously replaced by online resources and that's why having this online recipe book has many advantages.

## Website Link

My cookbook can be accessed on: [My Cookbook.](https://my-recipe-cookbook.herokuapp.com/)

**Note for CI Assessors** - You need to create a new account with an username  and a password, be aware this won't be encrypted.


## UX
* The main goal was to provide a user-friendly experience on this recipe book website.
* Not registered users can not view any the recipes. However, if they create an account, they will have full access to "My Cookbook". As only registered users can add recipes.
* When viewing a recipe, all the important information is desplayed in blocks, in a legible manner.
* Add Recipe and Edit Recipe pages have the same structure
* All input elements are clearly labeled, and provide placeholders and default values whenever relevant
* All events on the website are complemented by alerts such as when a recipe is successfully added, deleted or edited. 
Also when the results is none or when the user's Cookbook is empty.
* When a user is logged in a "Log Out" link is displayed and vice-versa
* An Info message is displayed on the Login/Register page in order to alert the users about
that usernames and passwords aren't encrypted.


## Functional requirements
The basic requirements on this project are the ability to perform CRUD (Create, Read, Update and Delete) operations on the primary documents in mongoDB database, the recipes. The user should also be able to search on mongoDB database in an easy way, shuch as including queries and navigate through the entire database.  

Nevertheless I believe it is important to have a user registration function and necessarily required for this project, to be able to implement the creation and deletion of recipes. All of the functionality of this website will be recorded as a registered user.  

I created a collection which will store the recipes added to `My Favourite Recipes` and t will be deleted automatically from this collection if the user doesn't want to keep as favourite anymore. 

The site should be responsive and work on all browsers.   

## Wireframes


 * [Mobile Wireframes](hhttps://github.com/Debbiepimpo/Milestone3/tree/master/wireframes/mobile-wireframes)
 * [Desktop Wireframes](https://github.com/Debbiepimpo/Milestone3/tree/master/wireframes/desktop-wireframes)


### User Stories
1. Users whose passion about cooking is strong and are interested  in viewing, searching and adding new recipes.
2. Users who would like not only to browse, search and add for recipes even those ones who are looking tasty and new recipes to implement on their dietary and the love to keep them all recipes in one paperless online storage creating their own Cookbook.
3. A third category will be those who would be just interested to store their own favourite recipes, without viewing other recipes.


## Features

The content requirements for the functions proposed above would be as follows:
  - A search box for make the users search any recipe easily. 
  - A recipe display view, which lays out the ingredients, allergies, diet and cuisine of each recipe with all the fields explaind and display clear and easy to read and identify them.
  - Add a recipe form.
  - Edit a recipe form only on that recipes added by the user logged. 
  - User favourite recpies page.
  - Registration/Login form.
  - Log Out button. 

### Existing Features

  *   **Login/Register** 
  *   **Intro Page** 
  *   **View all the recipes** 
  *   **Search bar** 
  *   **Filter and sort recipes** 
  *   **Add Recipes**
  *   **Edit Recipes** 
  *   **Delete Recipes**
  *   **Add/delete ingredients/instructions** 
  *   **Add a picture for each recipe** -
  *   **Add to Favourites** 
  *   **Check boxes that match allergies that the recipe contains** 
  *   **Choos a diet and a Cuisine Type**

### Features Left to Implement

  * Add images for make instructions/ingredients easier to follow
  * Add more info on recipes such as time cooking, how many people can eat if you follow a recipe, etc...
  * Implement that you can share recipes on your social media.
  * Add a delete pop up to ask the user if is sure to delete the recipe.
  * Make the Sorty by lastest, oldest and favourite recipes work.

## Technologies Used

This is a list of technologies I have used to build out my site.
###### Front-end
* HTML
* CSS 
* Bootstrap
* Balsamiq
* Google Fonts
* Font Awesome
* Javascript/JQuery

###### Back-end
* Python
* Flask
* Jinja

###### Database
* MongoDB

###### Other
* GitHub
* Heroku

## Testing

### Responsiveness Testing 
##### W3

I made the automatically testing using the W3 HTML checker:

* [W3C Validator](https://validator.w3.org/#validate_by_input) - For HTML
* [JIGSAW W3C Validator](https://jigsaw.w3.org/css-validator/#validate_by_input) - For CSS

##### Chrome Dev Tools

I used Dev Tools to check if there was an error on my page. 
Then, I changed what was wrong in the dev tools and I would be able to see 
the changes in a live update into my browser.Once I've found the issue I went
back to Cloud9 at AWS and make the changes there. 


##### Manual Testing

I have tested the website on:

* Google Chrome
* Apple Safari
* Internet Explorer
* Mozilla Firefox

##### Devices Tested:

* iPhone X
* iPhone 8
* iPhone 6/7
* iPad Pro
* iPad
* Samsung Galaxy S9
* Huawei M20


### Form Tested
* The same form structure is used for Add and Edit Recipes. 
 Form validation that checks whether the input was provided for all the fields is performed in the backend
* Checks/restrictions like data type or instruction and minimum value attributes for numeric input run in the frontend.
* Tested by partially filling in the input field or inserting data that would be invalid. 
* Clicking buttons out of the expected order or by providing unexpected inputs.
* Submitting empty or partially empty form.
* Checking if the input was correctly stored.
* Editing a recipe and make sure that the new input was kept for the field that was edited, while all
the other fields are kep values from the database.

### View sort and filter recipes
* Ensure that when the search result is zero display the correct message 
* Checked that the recipes that contain allergies were excluded as expected
* Apply filters that have no result and check the alert message is displayed
* Check that the results matched the filters applied
* Check that multiple selection worked correctly


### Login/Registration and Log out Test
* Ensure that user couldn't access "My Recipes" section if not logged in
* Check if the user that is login in is registered. And the username matches usernames in the database
* If username matches any username in database check if the password inserted matched the password from the database associated to the username
* Check that when a user is not logged in a "Log In" text is displayed
* Check that when a user is logged in a "Log Out" text is displayed

### View/Editing/Deleting Recipes in My Cooking Book
* Ensure that user can delete/edit only his/her own recipes. For this, I use two different users where created. 
* When a user has zero recipes a message will be displayed

### Next/Previous Page
* Test that when there are no recipes left the " next page" button is not displayed
* Test that when there are no previous recipes to display left the "previous page" button is not displayed

### Debbuging
Most of the bugs I found while developing this site, had to be realted with "My Favourites Recipes", how I stored them and how to reflect if the recipes were stored as favourites them with an icon. 

  Initially, when a User saved a recipe, that recipe wasn't store properly at mongoDB. When I fixed the issue about stored the recipe on favourites,the icon didn't fill. This was important to  display when the user add a recipe to favourites. 
  
  I've stored the "recipe_id" and "user" in a collection called "favourites" at mongoDB to make sure is only store as "favourite" once for each user. 

## Deployment
My website was created using Cloud9 on AWS and I created an external repository on GitHub and linked it there in a new repository. This lets me protect my work against any unexpected error such as delete something essential to keep the project working.

* I created a new environment in Cloud9.
* Created all my folders and files.
* Inside the bash terminal, entered 'git init'.
* Entered 'git add .' into the terminal.
* Entered 'git commit' into the terminal and created my initial commit.
* Linked my local git repository to a GitHub repository.
* Followed the below steps to deploy the site to GitHub pages.

This Project was deployed also with Heroku in the following way:
* Create Heroku account
* Login into Heroku from console `heroku login`
* Create a new empty App on Heroku as none was created before `heroku create` 
* Rename App `heroku apps: rename my-recipe-cookbook`
Run this command from App's Root. The empty Heroku Git repository is automatically set as a remote for your local repository.
Check `git remote -v`
* Create a `Procfile` (instruction to Heroku as which file should be used as an entry point for our App)
The `Procfile` must be in your app’s root directory `echo web python app.py > Procfile`
* Create a requirements.txt file `sudo pip3 freeze --local > requirements.txt`
* To deploy `git push heroku master`
* Set the `IP`,`PORT`, `SECRET_KEY` and any other environment variables in Heroku Account Settings

### Media 

   All recipes are from following books:
   * Mary Berry Cooks The Perfect: Step by Step.
   * Stir-Fry : Over 70 delicious one-wok meals.
   * Gloriously Gluten Free: Fresh and Simple Gluten-Free.

## Credits
---
* To my mentor, [Sandeep Aggarwall](https://github.com/asandeep), for guiding me through the process of this project, offering assistance when necessary and providing honest feedback about my work to point me in the right direction.
* The Slack community which people who are there trying to help each other with the skills they've learned for coding and can receive from the other students is a great tool to have.

## Acknowledgements

  * [W3Schools](https://www.w3schools.com/) - I used this to ensure I was entering all the information required correctly on my HTML and CSS and even for helping me with the functions on JavaScript.
  * [Stack overflow](https://stackoverflow.com/) - Very good and useful website for implement what you need to use one your backend related with Python and Flask.
  * [MongoDB Manual](https://docs.mongodb.com/manual/) - To get confident using mongoDB on this project.
  * [Pymongo](https://api.mongodb.com/python/current/) - To make sure m website works using Python to make the data base and Jinja templates interactive and linked.
  * [Flask](https://flask.palletsprojects.com/en/1.0.x/) - To solve all problems might had while i was developing this project.
