from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)
db_path = "D:\\VS Code\\Projets\\Cookbook\\Database\\Recipes.db"

def correct_encoding(texte):
    try:
        corrected_text = texte.encode('latin-1').decode('utf-8')
        return texte, corrected_text
    except UnicodeDecodeError:
        return texte, None
    
def get_recipe_titles():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM Recipes")
    titles = [row[0] for row in cursor.fetchall()]
    connection.close()
    return titles

def get_ingredients():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT description FROM Recipes")
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
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            query = "SELECT name FROM Recipes WHERE " + " AND ".join(["description LIKE ?" for _ in selected_ingredients])
            
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
    cursor.execute("SELECT * FROM Recipes WHERE name=?", (title,))
    recipe = cursor.fetchone()
    connection.close()
    return jsonify({'title': recipe[0], 'ingredients': recipe[3], 'directions': recipe[6], 'source': recipe[2]})

if __name__ == '__main__':
    app.run(debug=True)
