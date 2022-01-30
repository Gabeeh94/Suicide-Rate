import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pyodbc
import geopandas
import folium
# We import the required library:
from branca.element import Template, MacroElement
import branca


#Set the environment to get the table from the databse in SQL Server

# Defining our connection variables
driver = 'FreeTDS'
server = 'localhost'  # change this to your db’s IP address
port = '1433'
database = 'Suicide_Project' # change this to the name of your db
username = 'sa' # replace with your username
password = 'Yajirobe1+' # replace with your password
version  = '7.3'

#Create string to connect
mssql_string = 'DRIVER={'+driver+'};SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+password+';TDS_Version='+version+';'

conn = pyodbc.connect(mssql_string)

engine = create_engine('mssql+pyodbc://{}:{}@{}:{}/{}?driver={}'.format(username, password, server, port, database, driver))

#Query the Suicide table
suicide_rate = pd.read_sql_query(
    '''SELECT SpatialDimValueCode, Location, FactValueNumeric
    FROM suicide_data
    WHERE Period = '2019' AND Dim1 = 'Both sexes' AND Dim2 IS NULL''', 
con=engine)

# Read the geopandas dataset
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

#For some reason France and Norway don't have country codes so I will manually append them to not use fuzzy matching again

world.at[43,'iso_a3'] = 'FRA'
world.at[21,'iso_a3'] = 'NOR'



# Merge the two DataFrames together
world = world.merge(suicide_rate, how="left", left_on=['iso_a3'], right_on=['SpatialDimValueCode'])

# Clean data: remove rows with no data
world = world.dropna(subset=['FactValueNumeric'])


variable = 'FactValueNumeric' #metric of interest
name = 'Suicide Rate per 100.000 people'


# Create a map
my_map = folium.Map()

bins = list(world["FactValueNumeric"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))


# Add the data
folium.Choropleth(
    geo_data=world,
    nan_fill_color = "White",
    name='choropleth',
    data=world,
    columns=['name', 'FactValueNumeric'],
    key_on='feature.properties.name',
    fill_color='OrRd',
    fill_opacity=1,
    line_opacity=0.2,
    bins = bins,
    legend_name='Suicide Rate per 100.000 people'  
).add_to(my_map)



# Add hover functionality.
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
NIL = folium.features.GeoJson(
    data = world,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['name','FactValueNumeric'],
        aliases=['name','FactValueNumeric'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
my_map.add_child(NIL)
my_map.keep_in_front(NIL)
my_map

my_map.save('suicide.html')

