import sqlite3
from passlib.hash import bcrypt

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class RecipesDB:
    def __init__(self):
        self.connection = sqlite3.connect("recipes.db")
        #This is assigning a pointer to the function
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    #INSERT
    def insertRecipe(self, title, diet, ingredients, instructions):
        data = [title, diet, ingredients, instructions]
        self.cursor.execute("INSERT INTO recipes (title, date, diet, ingredients, instructions) VALUES (?, date('now'), ?, ?, ?)", data)
        self.connection.commit()

    def insertUser(self, firstName, lastName, email, password):
        data = [firstName, lastName, email, bcrypt.hash(password)]
        self.cursor.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()

    #READ
    def getAllRecipes(self):
        self.cursor.execute("SELECT * FROM recipes")
        recipes = self.cursor.fetchall()
        return recipes

    def getOneRecipe(self, member_id):
        data = [member_id]
        self.cursor.execute("SELECT * FROM recipes WHERE id = ?", data)
        recipe = self.cursor.fetchone()
        return recipe

    def getOneUser(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM users WHERE email = ?", data)
        recipe = self.cursor.fetchone()
        return recipe

    #Delete
    def deleteOneRecipe(self, member_id):
        data = [member_id]
        self.cursor.execute("DELETE from recipes WHERE id = ?", data)
        self.connection.commit() 
        return
    
    def deleteOneUser(self, email):
        data = [email]
        self.cursor.execute("DELETE from users WHERE email = ?", data)
        self.connection.commit() 
        return

    #Update
    def updateRecipe(self, title, diet, ingredients, instructions, recipe_id):
        data = [title, diet, ingredients, instructions, recipe_id]
        self.cursor.execute("UPDATE recipes SET title = ?, date = date('now'), diet = ?, ingredients = ?, instructions = ? WHERE id = ?", data)
        self.connection.commit()

    def updateUser(self, firstName, lastName, email):
        data = [firstName, lastName, email, email]
        self.cursor.execute("UPDATE users SET firstName = ?, lastName = ?, email = ?  WHERE email = ?", data)
        self.connection.commit()





