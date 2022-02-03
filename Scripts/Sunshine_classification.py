import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pyodbc

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

conn = pyodbc.connect(mssql_string)

    
engine = create_engine('mssql+pyodbc://{}:{}@{}:{}/{}?driver={}'.format(username, password, server, port, database, driver))

countries_mean = pd.read_sql_query('''SELECT * FROM SunshineMean''', con=engine)

#Create Dataframe to put the sunlight level of countries

countries_sunlight_level = pd.DataFrame(columns = ['Country','Sunlight Level'])

var = 'MeanAnnualSunlightHours'

#Define Quartiles to dscriminate fairly how the countries should be categorized

Q1 = np.percentile(countries_mean[var], 25, interpolation = 'midpoint')
Q2 = np.percentile(countries_mean[var], 50, interpolation = 'midpoint')
Q3 = np.percentile(countries_mean[var], 75, interpolation = 'midpoint')

# Get the countries categorized

low = countries_mean.loc[(countries_mean[var] <= Q1)].assign(level = 'Low')
medium_low = countries_mean.loc[(countries_mean[var]> Q1) & (countries_mean[var] <= Q2)].assign(level = 'Medium-Low')
medium_high = countries_mean.loc[(countries_mean[var]> Q2) & (countries_mean[var] <= Q3)].assign(level = 'Medium-High')
high = countries_mean.loc[(countries_mean[var] > Q3)].assign(level = 'High')

#Append those countries to a dataframe with the countries by sunlight level

for i in (low, medium_low, medium_high, high):
    for j in range (0, len(i)):
        country = i.iloc[j,0]

        level = i.iloc[j,2]
        
        row = pd.Series([country,level], index=countries_sunlight_level.columns)
        
        countries_sunlight_level = countries_sunlight_level.append(row, ignore_index=True)


#Upload table to SQL database
countries_sunlight_level.to_sql('SunshineLevel', con=engine, index=False) 

