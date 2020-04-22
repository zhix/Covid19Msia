#! /usr/bin/env python3

import pandas as pd

df = pd.read_csv('HospitalData12Apr.csv')
print(df)

stateids = []
print(df["Available Capacity of Hospitals"].dtype)

for i in df["StateID"]:
	if i < 10:
		i = "0"+str(i)
	else:
		i = str(i)
	stateids = stateids + [i]

df["StateID"] = stateids

print(int(df["Available Capacity of Hospitals"][1]))