import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
from fuzzywuzzy import process

def get_row (df_1, df_2, header_1_1, header_1_2,header_2_1, header_2_2, loc_1, loc_2, summary):
    
    item_1 = float(df_1.loc[df_1[header_1_1] == loc_1,header_1_2].values)
              
    item_2 = float(df_2.loc[df_2[header_2_1] == loc_2, header_2_2].values)

    row = pd.Series([loc_1, item_1, item_2], index=countries_summary.columns)
    return row

    #Deletes superfluous word to make the fuzzy matching more accurate
def country_mod (country):
    country = country.replace('Republic','')
    country = country.replace('Democratic','')
    country = country.replace('of','')
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

#Query the suicide rate table
suicide_rate = pd.read_sql_query('''SELECT Location, FactValueNumeric  FROM suicide_data
WHERE Dim1 = 'Both sexes' AND Period = '2019' AND Dim2 IS NULL''', con=engine)

#Query the GDP table
gdp_2019 = pd.read_sql_query('''SELECT CountryName, GDP2019  FROM GDPPerCapitaPPP
WHERE NOT GDP2019='..' ''', con=engine)

#Deletes row that aren't countries to make the fuzzy matching more accurate
gdp_2019 = gdp_2019.iloc[0:193]

#Make a list with only the names of the countries contained in the suicide dataframe
countries_suicide = suicide_rate['Location'].tolist()

#Create a container dataframe for the matching data
countries_summary = pd.DataFrame(columns = ['Country','SuicideRate','GDP2019'])

#Create a blank list to store the unmatched countries
countries_unmatched = []

#Clone the GDP dataframe to delete the already matched countries
gdp_2019_unmatched = gdp_2019

# Iterate through the list of countries and compare the names of countries in both dataframes,
# in case of a coincidence, it appends the data to the summary dataframe. If it doesn't find a perfect
# match, it appends the country to the unmatched list
for country in countries_suicide:
    if country in gdp_2019.values:
        
        row = get_row(suicide_rate, gdp_2019, 'Location', 'FactValueNumeric', 'CountryName', 'GDP2019', country, country, countries_summary)
           
        countries_summary = countries_summary.append(row, ignore_index=True)
        
        gdp_2019_unmatched = gdp_2019_unmatched[gdp_2019_unmatched.CountryName != country]
        
    else:
        countries_unmatched.append(country)

# Create a list of the unmatched countries of the GDP dataframe to use fuzzy matching
gdp_2019_unmatched = gdp_2019_unmatched.CountryName.tolist()

##Create a blank list to store the remaining unmatched countries
countries_remaining = []


# Uses a similar process than the last loop but uses fuzzy matching to select the closest match. If this match has
# a similarity score of at least 90, it appends it to the summary dataframe
for country in countries_unmatched:
    country_new = country_mod(country)
    fuzzy = process.extract(country_new, gdp_2019_unmatched, limit=1)
    match = fuzzy[0][0]
    score = fuzzy[0][1]
    if score >= 90:
        row = get_row(suicide_rate, gdp_2019, 'Location', 'FactValueNumeric', 'CountryName', 'GDP2019', country, match, countries_summary)
        countries_summary = countries_summary.append(row, ignore_index=True)
        gdp_2019_unmatched.remove(match)
    else:
        countries_remaining.append(country)


# Flexibilizes the similarity criteria to 70 for the last iteration. As it is a small sample because of all the
# previous matches it doesn't need so much accuracy.
for country in countries_remaining:
    country_new = country_mod(country)
    fuzzy = process.extract(country_new, gdp_2019_unmatched, limit=1)
    score = fuzzy[0][1]
    match = fuzzy[0][0]
    if score >= 70:
        row = get_row(suicide_rate, gdp_2019, 'Location', 'FactValueNumeric', 'CountryName', 'GDP2019', country, match, countries_summary)
        countries_summary = countries_summary.append(row, ignore_index=True)
        gdp_2019_unmatched.remove(match)


# Upload table to SQL database
countries_summary.to_sql('SuicideGDP', con=engine, index=False)      
    

    
    






