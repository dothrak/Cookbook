import sqlite3
import json
import os
from tqdm import tqdm

def parse_json(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if not content:
            return "", "", "", "", "", ""  

        data = json.loads(content)

    title = data.get('title', '')
    directions = '\n'.join(map(str, data.get('directions', [])))
    ingredients = '\n'.join(map(str, data.get('ingredients', [])))
    source = data.get('source', '')
    tags = '\n'.join(map(str, data.get('tags', [])))
    url = data.get('url', '')

    return title, directions, ingredients, source, tags, url

def db_structure(db_name, title, ingredients, directions, tags, source, url):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Receipes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Ingredients TEXT,
            Description TEXT,
            Tags TEXT,
            Source TEXT,
            URL TEXTE                    
        )
    ''')

    cursor.execute('''
        INSERT INTO Receipes (Title, Ingredients, Description, Tags, Source, URL)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, ingredients, directions, tags, source, url))

    connection.commit()
    connection.close()

def count_json_files(folder_path):
    count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                count += 1
    return count

def process_folder(folder_path, db_name):
    total_files = count_json_files(folder_path)
    pbar = tqdm(total=total_files, desc='Processing Files', unit=' Mo', dynamic_ncols=True, miniters=1)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                title, directions, ingredients, source, tags, url = parse_json(file_path)
                db_structure(db_name, title, ingredients, directions, tags, source, url)
                pbar.update(1)

    pbar.close()

def main():
    folder_path = 'D:\\VS Code\\Projet\\Cookbook\\Database\\1'
    db_name = 'D:\\VS Code\\Projet\\Cookbook\\Database\\Receipes.db'
        
    if os.path.exists(db_name):
        print("Existing database found. Deleting and recreating...")
        os.remove(db_name)

    process_folder(folder_path, db_name)

if __name__ == "__main__":
    main()
