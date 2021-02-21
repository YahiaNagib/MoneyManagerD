# Money Manager
This application is used to manage financial data for a user, the user can add their income and expenses for each day. The application gives an overall summary for each month and detailed statistics.

### App features:
##### Main page
* Display financial data for each day in the main page.
* Ability to add income or expenses. It is required to choose a category, write the date of the operation and write the value and some notes.
* The main page has an overall summary including how much the user spent and how much money is remaining.
* The main page views only the operations for the current month, and it is possible to choose another month to view its data.
* The user can select a data to delete or modify it.

#### Categories page
* This page is used to manage the categories.
* The user can view the categories for income and expenses.
* Users can add new categories to the list.

#### Statistics page
* This page includes a simple chart to view total financial data.
* The page also includes a list for every category and views its percentage of total financial data whether it is income or expense.
* If the user clicked on an category of the list, another page will be viewed to show all data saved for thiss category.


# What is contained in each file
* The project contains only one app called home.
* It has a static file for both css and js files.
* It also has templates folder which include all html files.
#### models.py
* The model includes 4 tables, they are CategoryType, Category, Account and Item. There is also a User table added by default.
* CategoryType table includes only two entries which are income and expenses, this table has a one to many relationship with Category table.
* Category table used to store categories which are added by the user.
* Account table is used to map between the item and the user because each item must has a user. The user can has multiple accounts but this feature has not been added yet.
* Account table inclued the user, the name of the account, total income, total expenses and whether this account is active or not.
* Item table can store an item which has five properties: the date, value, category, account which is associated with a user and notes.

#### forms.py
* This file contains two forms.
* The first form which is UserRegisterForm is used for registeration of a user. Only an email field is added because django does not add this field by default.
* The othe form AddItemForm is used to add items.
* It inherits its data from Item model. Since category type is not included in this model, it has to be added in the form fiels as well.
* The meta class includes some widgets to add bootstrap classes to the form items.
* The __init__ function is overridden to change the categories list depending on the choice of category type item. For example if the user chooses expenses, then only expenses categories will be viewed in the dropdown list.

#### utils.py
* This file contains some utility functions used in the views.
* data_reshaping function is used to change the structure of the items retrieved from the database so it can be viewed correctly in the home page.
* get_statistics is used to get the list of categories and their percentages.
* account_after_item_delete is used to change total spending of a user when an item is deleted.

#### views.py
* It included several routes in the application.
* home: used to render the home page.
* add_item: to add item to the database.
* edit_item: to edit items in the database.
* delete_item: to delete an item.
* categories: to render the categories page.
* delete_category: to delete a category. (not working at this moment)
* register: to register a user.
* accounts: to render the accounts page (not implemented in the frontend yet)
* activate_account: to activate an account to view its data.
* statistics: render the statistics page.
* category_statistics: render the page which views the category statistics.
* logout_user: to logout
* load_categories: this view is used in the add item page to change the dropdown list of categories.
