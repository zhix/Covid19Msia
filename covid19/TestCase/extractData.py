#! /usr/bin/env python3

import pandas as pd

df = pd.read_csv('TestCase.csv')
print(df)


print(df["Daily Tests #"])
