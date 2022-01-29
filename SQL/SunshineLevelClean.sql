
-- Inserts a row with the average of the countries that have two values as they are both in Europe and Asia
INSERT INTO SunshineMean (Country, MeanAnnualSunlightHours)
SELECT 'KAZAKSTAN' AS Country ,Avg(MeanAnnualSunlightHours)
FROM SunshineMean 
WHERE Country = 'KAZAKSTAN (ASIA)'
OR Country = 'KAZAKSTAN (EUROPE)'

INSERT INTO SunshineMean (Country, MeanAnnualSunlightHours)
SELECT 'RUSSIA' AS Country ,Avg(MeanAnnualSunlightHours)
FROM SunshineMean 
WHERE Country = 'RUSSIAN FEDERATION (ASIA)'
OR Country = 'RUSSIAN FEDERATION (EUROPE)'

--Deletes the values from non-mainland regions of countries or the residue from the average calculation
DELETE
FROM
    SunshineMean 
WHERE
    Country = 'FRANCE (CARIBBEAN ISLANDS, GUADELOUPE, MARTINIQUE)'
    OR Country = 'FRANCE (FRENCH DEPARTMENT OF GUYANA)'
    OR Country = 'FRANCE (ISLANDS IN THE INDIAN OCEAN)'
    OR Country = 'AUSTRALIA (ANTARCTIC STATIONS)'
    OR Country = 'COLOMBIA (SAN ANDRES AND PROVIDENCIA ISLANDS)'
    OR Country = 'NETHERLANDS ANTILLES AND ARUBA'
    OR Country = 'PORTUGAL (MADEIRA)'
    OR Country = 'SPAIN (CANARY ISLANDS, CEUTA AND MELILLA)'
    OR Country = 'UNITED STATES OF AMERICA (PACIFIC ISLANDS)'
    OR Country = 'YUGOSLAVIA'
    OR Country = 'KAZAKSTAN (ASIA)'
	OR Country = 'KAZAKSTAN (EUROPE)'
	OR Country = 'RUSSIAN FEDERATION (ASIA)'
	OR Country = 'RUSSIAN FEDERATION (EUROPE)'




    

