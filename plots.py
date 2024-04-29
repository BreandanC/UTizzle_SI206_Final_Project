'Combining Data to make Plots'

import sqlite3 as sql
import matplotlib.pyplot as plt

'x axis population'
'y axis walkability'
'Calculate Average Slope of Graph == Increase in Walkability per Increase in Population'

# Get pop data
conn = sql.connect('us_cities.db')
curr = conn.cursor()

# Query the database
query = 'SELECT population FROM city_details'
populations = []
for row in curr.execute(query):
    populations.append(row[0])

conn.commit()
conn.close()

# Get walk data 
conn = sql.connect('walkability_scores.db')
curr = conn.cursor()

# Query the database
query = 'SELECT score FROM WalkabilityScores'
scores = []
for row in curr.execute(query):
    scores.append(row[0])

conn.commit()
conn.close()

populations = populations[:100]
scores = scores[:100]

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(populations, scores, alpha=0.5)

# Add labels and title
plt.title('Walkability Score vs. Population')
plt.xlabel('Population')
plt.ylabel('Score')

# Show grid
plt.grid(True)

# Show the plot
plt.show()

score_per_pop = sum(scores) / sum(populations) * 1_000_000
# print(score_per_pop)

with open('results.txt', 'w') as f:
    f.write("Score Increase per 1,000,000 Population:\n")
    f.write(str(score_per_pop))



# Now, create a histogram with Matplotlib
plt.figure(figsize=(10, 5))  # You can adjust the size of the figure
plt.hist(populations, bins=50, color='blue', edgecolor='black')  # Customize the number of bins & color

plt.title('Histogram of City Populations')  # Add a title
plt.xlabel('Population')  # Add an x-label
plt.ylabel('Number of Cities')  # Add a y-label

# Show the plot
plt.show()