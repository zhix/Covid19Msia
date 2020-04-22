#! /usr/bin/env python3

import pandas as pd
import random

def extractData(): 
	accumFile = "accumCasesFromDay1.csv"
	newFile = "newCasesFromDay1.csv"


	accumData = pd.read_csv(accumFile)
	# print(accumData.head())


	newcaseData = pd.read_csv(newFile)
	# print(newcaseData.head())
	# print(newcaseData.iloc[:,[10]])

	return accumData, newcaseData

def getDays():
	daySeries = extractData()[1]["Day since 100cases"]
	numDays = len(daySeries)
	# print(daySeries.iloc[2])
	# print(numDays)
	return numDays

def extractCountriesPopulation():
	populationFile = "populationRef3.csv" 
	populations = pd.read_csv(populationFile)
	return populations


def getColor(anyInt):

	if anyInt==0:
		color = 'rgba(0, 0, 0, 0.9)'
	elif anyInt==1:
		color = 'rgba(255, 0, 0, 0.9)'
	elif anyInt==2:
		color = 'rgba(0, 0, 255, 0.9)'
	elif anyInt==3:
		color = 'rgba(0, 255, 0, 0.9)'

	return color


def randomCountriesBasedonSize(numberOfCountries, size=["A","B","C"], randomOrNot = True, listRequired = ["Malaysia"]):
	
	df = extractCountriesPopulation()
	countriesA = df.loc[df["CountrySize"]=="A",["World"]]
	countriesB = df.loc[df["CountrySize"]=="B",["World"]]
	countriesC = df.loc[df["CountrySize"]=="C",["World"]]
	# print(countriesA)
	# randA = random.choice(countriesA["World"].tolist())

	randSampleNumberA = random.sample(range(len(countriesA)), numberOfCountries)
	listOfA = [countriesA["World"].tolist()[i] for i in randSampleNumberA]

	randSampleNumberB = random.sample(range(len(countriesB)), numberOfCountries)
	listOfB = [countriesB["World"].tolist()[i] for i in randSampleNumberB]

	randSampleNumberC = random.sample(range(len(countriesC)), numberOfCountries)
	listOfC = [countriesC["World"].tolist()[i] for i in randSampleNumberC]	

	if "A" not in size: 
		listOfA=[]
	if "B" not in size: 
		listOfB=[]
	if "C" not in size: 
		listOfC=[]

	if randomOrNot == False: 
		listOfA=[]
		listOfB=[]
		listOfC=[]
	
	return listOfA, listOfB, listOfC, listRequired

def getPopulation(country): 
	populationsDF = extractCountriesPopulation()
	populationDF = populationsDF.loc[populationsDF["World"]==country, "Population"]
	# print(populationDF)
	populationSTR = populationDF.iloc[0].replace(",","")
	populationINT = int(populationSTR)
	return populationINT

def combineData(country): 
	pop = getPopulation(country)
	accumData = extractData()[0][country]
	newData = extractData()[1][country]
	t7newData = newData.rolling(window=7).mean()
	t7accumData = accumData.rolling(window=7).mean()

	t7newPrev = t7newData/pop
	t7accumPrev = t7accumData/pop


	# print(accumData.head())
	# print(newData.head())

	df = pd.concat([accumData,newData,t7newData, t7accumData, t7newPrev, t7accumPrev],axis=1)
	df.columns = ["Accum","New","Trailing7DayNewCases", "Trailing7DayAccumCases", "Trailing7DayNewPrev", "Trailing7DayAccumPrev"]
	# print(df)

	return df

# if __name__ == '__main__':
# 	a = randomCountriesBasedonSize(5)
# 	print(a)
	# country1 = "Australia"
	# country2 = "Malaysia"
	# combineData(country2)
# 	accumData = extractData()[0][country1]
	# pop = getPopulation(country1)
	# print(pop)

# 	print(accumData/pop) 