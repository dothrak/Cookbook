# Dothrak's Cookbook

It's a little web application I created because I never knew what to make myself to eat with the leftovers in my fridge. So I came up with an app that would let me pull out a set of culinary recipes to help me avoid wasting certain foods.

The application's database is made up of recipes from the French website Marmiton. Thanks to the SoTrxII API for helping me retrieve them.

The database is completely customizable to suit individual culinary tastes, so you'll need to build it up before installing the application.

## Database creation


## Installation

Install the packages required to run the application.

```
pip install pyinstaller flask unidecode
```

Enter the path to the unique_db.json file in the Database folder in var.py.

```python
db_path = "ENTER PATH HERE"
```

Modify the file DothraksCookbook.spec with the path of the repository folder downloaded on your machine in each location of the type :

```python
['FILE PATH']
```

Install the application on your machine using the command : 
```
python -m PyInstaller .\DothraksCookbook.spec
```
Once the process is complete, you should find a "dist" directory in your application directory. Inside, you'll see your executable.
