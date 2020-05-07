#! /usr/bin/env python3

import pandas as pd
import random

def extractData(): 
	accumFile = "accumCasesFromDay12.csv"
	newFile = "newCasesFromDay12.csv"


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
	populationFile = "populationRef4.csv" 
	populations = pd.read_csv(populationFile)
	return populations

def getCodeDay1Date(country):
	df = extractCountriesPopulation()
	countryCode = df.loc[df["World"]==country,["CountryCode"]]
	day1Date = df.loc[df["World"]==country,["Date of Day 1"]]
	return countryCode, day1Date


def getStringency(country):
	stringencyFile = "exportStringencyScore.csv" 
	rawData = pd.read_csv(stringencyFile)
	return rawData[country].tolist() 


def getColor(anyInt):

	if anyInt==0:
		color = 'rgba(0, 0, 0, 0.9)'
	elif anyInt==1:
		color = 'rgba(255, 0, 0, 0.9)'
	elif anyInt==2:
		color = 'rgba(0, 0, 255, 0.9)'
	elif anyInt==3:
		color = 'rgba(204, 0, 204, 0.9)'
	elif anyInt==4:
		color = 'rgba(0, 255, 0, 0.9)'

	return color


def randomCountriesBasedonSize(numberOfCountries, 
	size=["A","B","C","D"], 
	randomOrNot = True, 
	listAddition = [], 
	listRemoval = [],
	listRequired = ["Malaysia"]):
	
	# print(listAddition)

	df = extractCountriesPopulation()
	countriesA = df.loc[df["CountrySize"]=="A",["World"]]["World"].tolist()
	countriesB = df.loc[df["CountrySize"]=="B",["World"]]["World"].tolist()
	countriesC = df.loc[df["CountrySize"]=="C",["World"]]["World"].tolist()
	countriesD = df.loc[df["CountrySize"]=="D",["World"]]["World"].tolist()
	listOfA = []
	listOfB = []
	listOfC = []
	listOfD = []
	for country in listAddition: 
		# print(country)
		if country in countriesA:
			listOfA.append(country)
		elif country in countriesB:
			listOfB.append(country)
		elif country in countriesC:
			listOfC.append(country)
		elif country in countriesD:
			listOfD.append(country)					 
	# print(listOfA, listOfB, listOfC)

	if numberOfCountries > len(listOfA):
		randSampleNumberA = random.sample(range(len(countriesA)), numberOfCountries-len(listOfA))
		listOfA = listOfA + [countriesA[i] for i in randSampleNumberA]
		listOfA = list(dict.fromkeys(listOfA))

	if numberOfCountries > len(listOfB):
		randSampleNumberB = random.sample(range(len(countriesB)), numberOfCountries-len(listOfB))
		listOfB = listOfB + [countriesB[i] for i in randSampleNumberB]
		listOfB = list(dict.fromkeys(listOfB))

	if numberOfCountries > len(listOfC):
		randSampleNumberC = random.sample(range(len(countriesC)), numberOfCountries-len(listOfC))
		listOfC = listOfC + [countriesC[i] for i in randSampleNumberC]	
		listOfC = list(dict.fromkeys(listOfC))

	if numberOfCountries > len(listOfD):
		randSampleNumberD = random.sample(range(len(countriesD)), numberOfCountries-len(listOfD))
		listOfD = listOfD + [countriesD[i] for i in randSampleNumberD]	
		listOfD = list(dict.fromkeys(listOfD))																						   



	if "A" not in size: 
		listOfA=[]
	if "B" not in size: 
		listOfB=[]
	if "C" not in size: 
		listOfC=[]
	if "D" not in size: 
		listOfD=[
	if randomOrNot == False: 
		listOfA = ["New Zealand","Puerto Rico","Iceland","Ireland","Finland"]
		listOfB = ["Singapore","Portugal","Belgium","Ecuador","United Arab Emirates"]
		listOfC = ["Canada","Australia","Peru","Ghana","Saudi Arabia"]
		listOfD = ["Japan","South Korea","Italy","China","United Kingdom"]
	for country in listRemoval:
		if country in listOfA:
			listOfA.remove(country)
		elif country in listOfB:
			listOfB.remove(country)
		elif country in listOfC:
			listOfC.remove(country)
		elif country in listOfD:
			listOfD.remove(country)
	return listOfA, listOfB, listOfC, listOfD, listRequired

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