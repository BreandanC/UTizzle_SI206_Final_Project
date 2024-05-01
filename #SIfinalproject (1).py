'SI206 Final Project'
"Emma's Portion"

import requests
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3
import re


        
def get_walk_data(link):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.content, 'html.parser')
    cities = soup.find_all('td', class_="city")
    walk = soup.find_all('td', class_="score")
    ret = {}
    for city, score in zip(cities, walk):
        city_name = city.get_text(strip=True)
        score_value = float(score.get_text(strip=True))
        ret[city_name] = score_value
    return ret

def create_tables():
    with sqlite3.connect('walkability_scores.db') as con:
        curr = con.cursor()
        curr.execute('''CREATE TABLE IF NOT EXISTS Cities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT UNIQUE
                        )''')
        curr.execute('''CREATE TABLE IF NOT EXISTS WalkabilityScores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city_id INTEGER,
                        score FLOAT,
                        FOREIGN KEY (city_id) REFERENCES Cities(id)
                        )''')

def make_data_base(data):
    with sqlite3.connect('walkability_scores.db') as con:
        curr = con.cursor()
        entries_count = 0  # Keep track of the number of entries
        
        for city, score in data.items():
            # Insert or ignore new city
            curr.execute("INSERT OR IGNORE INTO Cities (city) VALUES (?)", (city,))
            # Get the city_id for the city
            curr.execute("SELECT id FROM Cities WHERE city = ?", (city,))
            city_id = curr.fetchone()[0]
            
            # Check if there's already a score for the city_id
            curr.execute("SELECT score FROM WalkabilityScores WHERE city_id = ?", (city_id,))
            existing_score = curr.fetchone()
            
            # Add or update walkability score entry
            if existing_score is None:
                curr.execute("INSERT INTO WalkabilityScores (city_id, score) VALUES (?, ?)", (city_id, score))
            else:
                curr.execute("UPDATE WalkabilityScores SET score = ? WHERE city_id = ?", (score, city_id))
            
            entries_count += 1  # Increment the counter after each entry
            if entries_count >= 25:
                con.commit()  # Commit changes after every 25th entry
                entries_count = 0  # Reset the counter

        con.commit()  # Make sure to commit any remaining changes after the loop
def retrieve_data_from_db():
    with sqlite3.connect('walkability_scores.db') as con:
        curr = con.cursor()
        curr.execute('''SELECT WalkabilityScores.score FROM WalkabilityScores''')
        scores = [row[0] for row in curr.fetchall()]
    return scores  # Return a list of scores

def plot_histogram(scores):
    plt.figure(figsize=(10, 5))
    plt.hist(scores, bins=10, color='pink', edgecolor='brown')
    plt.title('Histogram of Walkability Scores')
    plt.xlabel('Walkability Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show() 


def main():
    create_tables()
    walk_data = get_walk_data('https://www.walkscore.com/cities-and-neighborhoods/')
    make_data_base(walk_data)
    scores = retrieve_data_from_db()
    plot_histogram(scores)

if __name__ == "__main__":
    main()
