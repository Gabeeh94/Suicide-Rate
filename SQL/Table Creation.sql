

CREATE DATABASE Suicide_Project;

use Suicide_Project;

--Create blank table to insert the WHO suicide rate data from a csv

CREATE TABLE suicide_data (

IndicatorCode VARCHAR(100),
Indicator VARCHAR(100) ,
ValueType VARCHAR(100),
ParentLocationCode VARCHAR(100),
ParentLocation VARCHAR(100),
LocationType VARCHAR(100),
SpatialDimValueCode VARCHAR(100),
Location VARCHAR(100),
PeriodType VARCHAR(100),
Period INT,
IsLatestYear VARCHAR(100),
Dim1Type VARCHAR(100),
Dim1 VARCHAR(100),
Dim1ValueCode VARCHAR(100),
Dim2Type VARCHAR(100),
Dim2 VARCHAR(100),
Dim2ValueCode VARCHAR(100),
Dim3Type VARCHAR(100),
Dim3 VARCHAR(100),
Dim3ValueCode VARCHAR(100),
DataSourceDimValueCode VARCHAR(100),
DataSource VARCHAR(100),
FactValueNumericPrefix VARCHAR(100),
FactValueNumeric FLOAT,
FactValueUoM VARCHAR(100),
FactValueNumericLowPrefix VARCHAR(100),
FactValueNumericLow FLOAT,
FactValueNumericHighPrefix VARCHAR(100),
FactValueNumericHigh FLOAT,
Value VARCHAR(100),
FactValueTranslationID VARCHAR(100),
FactComments VARCHAR(100),
Language VARCHAR(100),
DateModified VARCHAR(100)
);

--Insert data from csv to the table

BULK INSERT suicide_data
FROM '/home/gabriel/Desktop/Projects/Suicide/CSV/suicide rate.csv'
WITH (
    FIELDTERMINATOR = ',',
    FIRSTROW = 2,
    ROWTERMINATOR ='\r\n'
)

 
CREATE TABLE GDPPerCapitaPPP (

CountryName VARCHAR(100),

GDP2000 VARCHAR(100),
GDP2001 VARCHAR(100),
GDP2002 VARCHAR(100),
GDP2003 VARCHAR(100),
GDP2004 VARCHAR(100),
GDP2005 VARCHAR(100),
GDP2006 VARCHAR(100),
GDP2007 VARCHAR(100),
GDP2008 VARCHAR(100),
GDP2009 VARCHAR(100),
GDP2010 VARCHAR(100),
GDP2011 VARCHAR(100),
GDP2012 VARCHAR(100),
GDP2013 VARCHAR(100),
GDP2014 VARCHAR(100),
GDP2015 VARCHAR(100),
GDP2017 VARCHAR(100),
GDP2018 VARCHAR(100),
GDP2019 VARCHAR(100),
GDP2020 VARCHAR(100),

);


BULK INSERT GDPPerCapitaPPP
FROM '/home/gabriel/Desktop/Projects/Suicide/CSV/GDP per Capita World bank.csv'
WITH (

    FIELDTERMINATOR = ';',
    FIRSTROW = 2,
    ROWTERMINATOR ='0x0a'
)

 



