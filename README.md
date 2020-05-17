# Project 3 - Pizza

Web Programming with Python and JavaScript

In this project, an online order app for a pizza restaurant is built using Django. After registration, users will be able to browse the restaurant menu and choose and custumize items to a shopping cart. After this, they can proceed to checkout to place the order and review their confirmed orders. Admins might use the admin page to add, modify and remove items from the menu, as well as for reviewing orders and marking them as complete.

The following is a description of the main files of the project and their use:

-- [orders]
  |-- [migrations] --> Contains Django python files used for database changes that we define in our models.
  |-- [templates]
    |-- [orders] --> All our app html templates
      |-- layout.html   --> Defines general page layout, shared by all pages
      |-- index.html    --> Starting page, if logged in, i.e. the online restaurant menu
      |-- login.html    --> Login page
      |-- register.html --> Register new user page
      |-- shoppingCart.html --> Shopping cart review page
      |-- checkout.html --> Checkout page with stripe card payment
      |-- orders.html   --> Orders review page for user
      |-- orderConfirmed.html --> Confirmation message page
  |-- importProducts.py --> This file just contains a script to be run in django shell to speed up the product filling up process from the individual menu item categories.
  |-- models.py --> Our database models are defined here
  |-- views.py --> All app methods and functionality are defined here   
      
-- [pizza]
  |-- settings.py --> Main app settings

-- [static]
  |-- client.js --> Stripe javascript functions for the card payment
  |-- functions.js --> Some app javascript functions for interactivity
  |-- styles.css --> Page style is defined in css here. Bootstrap is also used throughout the templates
  
-- db.sqlite3 --> The Database is contained in this file
-- manage.py --> Root python file
-- ...

As final notes:
* A consistent theme was chosen, corresponding with the colors of the original Pinnochio's pizzeria website.
* Personal touches include:
    * The style of the site. 
    * Allowing site admins to mark orders (shopping carts) as complete or pending from a modified version of the admin page
    * Stripe API integration for payment
    * Allowing users to see the status of their orders.
    * Navigation menu with shopping cart badge dynamically indicating the number of items in the shopping cart!
