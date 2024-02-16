import json
import sqlite3

def create_recipe_database(json_data):
    conn = sqlite3.connect("Recipes.db")
    cursor = conn.cursor()
    cursor.execute('PRAGMA encoding="UTF-8";')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes
                      (name TEXT, rate REAL, url TEXT, ingredients TEXT, author TEXT,
                      images TEXT, steps TEXT, description TEXT, difficulty INTEGER,
                      budget INTEGER, tags TEXT, prepTime INTEGER, totalTime INTEGER,
                      people INTEGER)''')

    # Insert data into the Recipes table
    for recipe in json_data:
        name = recipe["name"]
        author = recipe["author"]
        rate = recipe["rate"]
        url = recipe["url"]
        ingredients = json.dumps(recipe["ingredients"])
        images = json.dumps(recipe["images"])
        steps = json.dumps(recipe["steps"])
        description = recipe["description"]
        difficulty = recipe["difficulty"]
        budget = recipe["budget"]
        tags = json.dumps(recipe["tags"])
        prepTime = recipe["prepTime"]
        totalTime = recipe["totalTime"]
        people = recipe["people"]

        cursor.execute('''INSERT INTO Recipes
                          (name, rate, url, ingredients, author, images, steps, description,
                          difficulty, budget, tags, prepTime, totalTime, people)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (name, rate, url, ingredients, author, images, steps, description,
                        difficulty, budget, tags, prepTime, totalTime, people))

    conn.commit()
    conn.close()

def remove_duplicate_recipes():
    conn = sqlite3.connect("Recipes.db")
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM Recipes
                      WHERE rowid NOT IN (SELECT MIN(rowid) FROM Recipes
                                         GROUP BY name, author)''')

    conn.commit()
    conn.close()


json_file = "unique_db.json"

with open(json_file) as file:
    json_data = json.load(file)

create_recipe_database(json_data)

remove_duplicate_recipes()
