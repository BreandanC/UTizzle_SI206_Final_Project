import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

def fetch_location_and_pm25_data(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT latitude, longitude, value as PM25
        FROM AirQuality
    ''')
    rows = cursor.fetchall()
    connection.close()

    return pd.DataFrame(rows, columns=['Latitude', 'Longitude', 'PM25'])

def main():
    # Get data from db
    database_name = 'FinalProject_v2.db'
    df_data = fetch_location_and_pm25_data(database_name)
    #print(df_data.head())

    # Extract lists
    lons = df_data['Longitude'].tolist()
    lats = df_data['Latitude'].tolist()
    pollution_data = df_data['PM25'].tolist()

    # Create a figure 
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})

    # Set the extent of the map to the USA (rough coordinates)
    ax.set_extent([-128, -62, 24, 50], crs=ccrs.PlateCarree())

    # Add map features like coastlines and borders
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Add a colorbar to represent the pollution data
    sc = plt.scatter(lons, lats, c=pollution_data, cmap='Reds', marker='o', s=100, alpha=0.6, transform=ccrs.PlateCarree())

    # Add a colorbar and its title
    cbar = plt.colorbar(sc)
    cbar.set_label('PM2.5 Concentration (µg/m³)')

    plt.title('PM2.5 Heatmap Over USA')
    plt.show()

if __name__ == "__main__":
    main()
