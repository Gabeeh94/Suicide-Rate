import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pyodbc

#Detect and deletes outliers in the scores using the Inter Quartile Range
def delete_outliers (var):
    Q1 = np.percentile(hours_sunshine[var], 25, interpolation = 'midpoint')
    Q3 = np.percentile(hours_sunshine[var], 75, interpolation = 'midpoint')
    IQR = Q3-Q1 
    #Above Upper Bound
    upper = hours_sunshine.index[hours_sunshine[var] >= (Q3 + 1.5*IQR)]
    #Below Lower Bound
    lower = hours_sunshine.index[hours_sunshine[var] <= (Q1 - 1.5*IQR)]
    # Drops outliers
    hours_sunshine.drop(upper, inplace = True)
    hours_sunshine.drop(lower, inplace = True)
    return upper, lower



#Path of the csv

csv_file = '/home/gabriel/Desktop/Projects/Suicide/CSV/UNdata_Export_20220114_120948452.csv'

#Reads data and assigns it to a pandas' dataframe

df = pd.read_csv(csv_file,na_values=('-9999.9','-9999'))

hours_sunshine = df[['Country or Territory','Annual NCDC Computed Value', 'Statistic Description', 'Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']].copy(deep=True)

if hours_sunshine.isnull().any().any() == True:  #Checks is there are any null values in the dataframe
    hours_sunshine_with_nan = hours_sunshine.index[hours_sunshine.isnull().any(axis=1)] #Creates dataframe with countries with null values
    hours_sunshine.drop(hours_sunshine_with_nan, axis = 0, inplace = True) #Deletes countries without rows
    


delete_outliers('Annual NCDC Computed Value')


#Make a dataframe whit only the countries names
countries = hours_sunshine.drop_duplicates(subset=['Country or Territory'])


countries_mean = pd.DataFrame(columns = ['Country','MeanAnnualSunlightHours'])
 
#Take all ocurrences of a country and append the mean of them to the dataframe countries_mean
for i in range (0, len(countries)):
    
    country = countries.iloc[i,0]

    ocurrences = hours_sunshine[hours_sunshine['Country or Territory']==country]
    
    mean = ocurrences['Annual NCDC Computed Value'].mean()
    
    row = pd.Series([country,mean], index=countries_mean.columns)
    
    countries_mean = countries_mean.append(row, ignore_index=True)
    
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

#Set the environment to upload the dataframe to a SQL Server table

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

#Upload table to SQL database
countries_mean.to_sql('SunshineMean', con=engine, index=False) 