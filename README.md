# Suicide Rate Analysis using SQL and Python

An analysis of the suicide rate in the world using SQL and Python to clean and extrapolate conclusions from the data including a regression and classification analysis to see if there is a relationship between GDP per Capita or Sunshine level and the suicide rate.

## Data Loading and Cleaning

Sources:

Suicide rate (World Health Organzation): https://www.who.int/data/gho/data/indicators/indicator-details/GHO/crude-suicide-rates-(per-100-000-population)

GDP per Capita PPP (World Bank): https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.PCAP.PP.CD&country=

Mean Annual Sunshine Hours (United Nations): https://data.un.org/Data.aspx?d=CLINO&f=ElementCode%3a15


The data was downloaded in csv format as it is shown in the CSV folder. Then the "Table Creation.sql" script in the SQL folder was written to load the suicide rate and gdp data to their respective tables. The "Queries.sql" sccreipt was used to check if the upload was okay and make some small updates on some loading errors. 

For the sunshine data, a different process (in Scripts/Sunshine_normalization.py) was needed as the data was unusable in its current state. The table was loaded from the csv file to python through pandas where the null values were deleted as well as the outliers. Then, as the data was organized by station, the code iterated through the table, calculating the mean of a given country stations and appending that value to a dataframe that ended up with all the mean annual sunshine hours of all countries in the database.

Finally, the countries were classified in 4 categories defined by the quartiles calculated from the dataset.

With all three datasets ready, they were all loaded into an SQL Sever Database for some basic cleaning and reloaded to python using the pyodbc and sqlalchemy modules. To make the regression and classification it was needed that the suicide rate data was joined to the gdp and sunshine one. But the problem was that the countries were not written in the same exact way. So two scripts (Scripts/Matching_GDP and Scripts/Matching_Sunlight) were written that used fuzzy matching (that is, looking for the most likely matches) to join the tables. 

## Exploratory analysis

First, the modules geopandas and folium were used to generate an interactive .html map, showing by color the different suicide rates and with the option of hovering over a country to see it's specific value. As Github can't show an .html map in the jupyter notebook, an .html file was generated to be open and show the map.

## Regression and classification analysis

Pending
