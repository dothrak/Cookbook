from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)
db_path = "D:\\VS Code\\Projet\\Cookbook\\Database\\Receipes.db"

def get_recipe_titles():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT Title FROM Receipes")
    titles = [row[0] for row in cursor.fetchall()]
    connection.close()
    return titles

def get_ingredients():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT Ingredients FROM Receipes")
    ingredients = [ingredient for row in cursor.fetchall() for ingredient in row[0].split('\n')]
    connection.close()
    return list(set(ingredients))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/recipes_inventory')
def recipes_inventory():
    titles = get_recipe_titles()
    return render_template('recipes_inventory.html', titles=titles)

@app.route('/search_recipes', methods=['GET', 'POST'])
def search_recipes():
    if request.method == 'POST':
        selected_ingredients = []
        for i in range(1, 11):
            ingredient = request.form.get(f'ingredient{i}')
            if ingredient:
                selected_ingredients.append(ingredient)

        if selected_ingredients:
            connection = sqlite3.connect("D:\\VS Code\\Projet\\Cookbook\\Database\\Receipes.db")
            cursor = connection.cursor()

            query = "SELECT Title FROM Receipes WHERE " + " AND ".join(["Ingredients LIKE ?" for _ in selected_ingredients])
            
            cursor.execute(query, ['%' + ingredient + '%' for ingredient in selected_ingredients])
            titles = [row[0] for row in cursor.fetchall()]

            connection.close()
            
            return render_template('search_results.html', titles=titles)

    ingredients = get_ingredients()
    return render_template('search_recipes.html', ingredients=ingredients)


@app.route('/get_recipe/<title>', methods=['GET'])
def get_recipe(title):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Receipes WHERE Title=?", (title,))
    recipe = cursor.fetchone()
    connection.close()
    return jsonify({'title': recipe[1], 'ingredients': recipe[2], 'directions': recipe[3], 'tags': recipe[4], 'source': recipe[5], 'url': recipe[6]})

if __name__ == '__main__':
    app.run(debug=True)