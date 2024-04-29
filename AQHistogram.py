import sqlite3
import matplotlib.pyplot as plt

def fetch_particle_data(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT value
        FROM AirQuality
        WHERE parameter = "pm25"
    ''')
    data = cursor.fetchall()
    
    connection.close()
    
    return data

def main():
    # Get data from the db
    database_name = 'FinalProject_v2.db'
    particle_data = fetch_particle_data(database_name)

    # Extract particle values
    particle_values = [entry[0] for entry in particle_data]

    # Create histogram
    plt.hist(particle_values, bins=25, color='lightblue', edgecolor='grey')

    # Add labels and title
    plt.xlabel('Particle Value')
    plt.ylabel('Frequency')
    plt.title('Distribution of PM2.5 Particles In The United States')

    # Show histogram
    plt.show()

if __name__ == "__main__":
    main()