from flask import Flask, render_template, request, jsonify
import json
from unidecode import unidecode
from var import db_path

app = Flask(__name__)
json_path = db_path

def get_recipe_titles():
    with open(json_path, 'r', encoding='utf-8') as json_file:
        recipes = json.load(json_file)
    titles = [recipe["name"] for recipe in recipes]
    return titles


def get_ingredients():
    with open(json_path, 'r', encoding='utf-8') as json_file:
        recipes = json.load(json_file)

    tags = set()
    for recipe in recipes:
        tags.update(recipe["tags"])

    filtered_tags = set()
    for recipe in recipes:
        for tag in recipe["tags"]:
            for ingredient in recipe["ingredients"]:
                if tag.lower() in ingredient.lower():
                    filtered_tags.add(tag)

    filtered_tags.discard("")
    sorted_tags = sorted(filtered_tags, key=lambda x: unidecode(x.lower()))

    return sorted_tags

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
            with open(json_path, 'r', encoding='utf-8') as json_file:
                recipes = json.load(json_file)

            matching_recipes = []
            for recipe in recipes:
                if all(tag.lower() in recipe["tags"] for tag in selected_ingredients):
                    matching_recipes.append(recipe["name"])

            return render_template('search_results.html', titles=matching_recipes)

    ingredients = get_ingredients()
    return render_template('search_recipes.html', ingredients=ingredients)



@app.route('/get_recipe/<title>', methods=['GET'])
def get_recipe(title):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        recipes = json.load(json_file)

    for recipe in recipes:
        if recipe["name"] == title:
            directions = recipe["steps"]
            formatted_directions = ["\nStep {}: {}".format(i + 1, direction) for i, direction in enumerate(directions)]
            
            print("Retrieved Recipe:", recipe)
            return jsonify({
                'title': recipe["name"],
                'ingredients': recipe["ingredients"],
                'directions': formatted_directions,
                'source': recipe["url"]
            })


if __name__ == '__main__':
    print("Connexion établie. Allez à http://127.0.0.1:5000/ \n")
    app.run(debug=False)
