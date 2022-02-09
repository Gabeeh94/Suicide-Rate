import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
from fuzzywuzzy import process
import matplotlib as plt

def get_row (df_1, df_2, header_1_1, header_1_2,header_2_1, header_2_2, loc_1, loc_2, summary):
    
    item_1 = float(df_1.loc[df_1[header_1_1] == loc_1,header_1_2].values)
              
    item_2 = df_2.loc[df_2[header_2_1] == loc_2, header_2_2].values[0]

    
    row = pd.Series([loc_1, item_1, item_2], index=countries_summary.columns)
    return row

    
def country_mod (country):
    country = country.replace('REPUBLIC','')
    country = country.replace('DEMOCRATIC','')
    country = country.replace('OF','')
    return country
    


#Set the environment to upload the dataframe to a SQL Server table

# Defining our connection variables
driver = 'FreeTDS'
server = 'localhost'  # change this to your db’s IP address
port = '1433'
database = 'Suicide_Project' # change this to the name of your db
username = 'sa' # replace with your username
password = '' # replace with your password
version  = '7.3'

#Create string to connect
mssql_string = 'DRIVER={'+driver+'};SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+password+';TDS_Version='+version+';'

#Connect to pyodbc
conn = pyodbc.connect(mssql_string)

#Create sqlalchemy engine to communicate with the SQL Server database
engine = create_engine('mssql+pyodbc://{}:{}@{}:{}/{}?driver={}'.format(username, password, server, port, database, driver))

#Query the sunshine table
sunshine_level = pd.read_sql_query('''SELECT * FROM SunshineLevel''', con=engine)

#Query the Suicide table
suicide_rate = pd.read_sql_query('''SELECT Location, FactValueNumeric  FROM suicide_data
WHERE Dim1 = 'Both sexes' AND Period = '2019' AND Dim2 IS NULL''', con=engine)



# Make a list with only the countries names on the sunlight dataframe
countries_sunlight = sunshine_level['Country'].tolist()

# Create a container dataframe for the matching data
countries_summary = pd.DataFrame(columns = ['Country','SuicideRate','SunshineLevel'])

# Create a blank list to store the unmatched countries
countries_unmatched = []

# Make a list with only the countries names on the suicide dataframe
suicide_unmatched = suicide_rate.Location.tolist()


# Iterate through the list of countries and compare the names of countries in both dataframes using fuzzy matching,
# in case of a coincidence score of at least 90, it appends the data to the summary dataframe. 

for country in countries_sunlight:
    country_new = country_mod(country)
    fuzzy = process.extract(country_new, suicide_unmatched, limit=1)
    match = fuzzy[0][0]
    score = fuzzy[0][1]
    if score >= 90:
        row = get_row(suicide_rate, sunshine_level, 'Location', 'FactValueNumeric', 'Country', 'Sunlight Level', match, country, countries_summary)
        countries_summary = countries_summary.append(row, ignore_index=True)
        suicide_unmatched.remove(match)
    else:
        countries_unmatched.append(country)
  

# Flexibilizes the similarity criteria to 70 for the last iteration. As it is a small sample because of all the
# previous matches it doesn't need so much accuracy.

for country in countries_unmatched:
    country_new = country_mod(country)
    fuzzy = process.extract(country_new, suicide_unmatched, limit=4)
    score = fuzzy[0][1]
    match = fuzzy[0][0]
    if score >= 80:
        row = get_row(suicide_rate, sunshine_level, 'Location', 'FactValueNumeric', 'Country', 'Sunlight Level', match, country, countries_summary)
        countries_summary = countries_summary.append(row, ignore_index=True)
        suicide_unmatched.remove(match)

# Upload table to SQL database
countries_summary.to_sql('SuicideSunlight', con=engine, index=False)      




