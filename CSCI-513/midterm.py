# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# CSCI 513.01W – Mid-term Quiz
# CWID: 50417840
# Name: Lon Jones Cherryholmes
import numpy as np
import pandas as pd
df = pd.read_csv("C:/SNOBOL4python/CSCI-513/titanicm.csv")
#------------------------------------------------------------------------------
print(df.info)
print(df.columns)
print(df.dtypes)
print(df.describe())
print(df.head())
print(df.tail())
print(df.count())
df[df.age.isnull()].count()
df.ticketno.isnull().count()
df.fare.isnull().count()
df[df.sibsp.isnull()].count()
df.parch.isnull().count()
#------------------------------------------------------------------------------
# How many of the ship crew survived? Please enter the total number of survivors as integer value.
df[df.survived == "no"].shape
df[df.survived == "yes"].shape
df[~df['class'].str.contains("1st|2nd|3rd")].shape
df[(~df['class'].str.contains("1st|2nd|3rd")) & (df.survived == "yes")].shape
#------------------------------------------------------------------------------
# Let us create two new columns 'firstName'  and 'lastName' based on the
# values in the 'name' column. There are two useful functions: the str
# function that converts a series into a string series, and split with the
# expand option. What is the most common last name from the crew? Please
# enter the name exactly as it is in the dataframe (case sensitive).
df['lastName'] = df.name.str.split(',', expand=True)[0]
df['firstName'] = df.name.str.split(',', expand=True)[1]
df.info()
df[df['class'].str.contains("crew$")]['class']
df[df['class'].str.contains("crew")].groupby("lastName")["lastName"].count().sort_values(ascending=False)
df[df['class'].str.contains("staff")].groupby("lastName")["lastName"].count().sort_values(ascending=False)
df[df['class'].str.contains("crew|staff")].groupby("lastName")["lastName"].count().sort_values(ascending=False)
# Smith
#------------------------------------------------------------------------------
# What is the most common last name from the passengers? Please enter the
# name exactly as it is in the dataframe (case sensitive).
df.groupby("class")["class"].count()
df[df['class'].str.contains("1st|2nd|3rd")]['class']
df[df['class'].str.contains("1st|2nd|3rd")]
df[df['class'].str.contains("1st|2nd|3rd")]
df[df['class'].str.contains("1st|2nd|3rd")].groupby("lastName")["lastName"].count().sort_values(ascending=False)
# Sage
#------------------------------------------------------------------------------
# What was the age of the oldest person on the ship? Please enter the integer
# value.
df.age.sort_values(ascending=False)
df.groupby('age').age.count().sort_values(ascending=False)
#------------------------------------------------------------------------------
# How many of the ship crew were from Scotland? Please enter the integer
# value.
df['class'].shape
df[df['class'].str.contains("1st|2nd|3rd")].shape
df[df['class'].str.contains("crew|staff")].shape
df[df['class'].str.contains("crew|staff")]
df.country
df[df.country == "Scotland"].shape
#------------------------------------------------------------------------------
# How many male passengers survived the crash? Please enter the integer value.
df[df.gender == 'female'].shape
df[df.gender == 'male'].shape
df[df.survived == 'yes'].shape
df[~df['class'].str.contains("1st|2nd|3rd")].shape
df[df['class'].str.contains("1st|2nd|3rd")].shape
df[(df['class'].str.contains("1st|2nd|3rd")) & (df.gender == 'male') & (df.survived == 'yes')].shape
#------------------------------------------------------------------------------
# What is the last name of the oldest person. Please enter the last name
# exactly as it is in the dataframe (case sensitive).
df.age.sort_values(ascending=False)
df.iloc[1176]
# Svensson
#------------------------------------------------------------------------------
# How many columns do we have ()? Please enter the integer value.
df.columns
df.dtypes
len(df.dtypes)
#------------------------------------------------------------------------------
# Which class ticket had the lowest survival rate? Please enter either 1 for
# first-class, 2 for 2nd-class, or 3 for 3rd-class.
df.groupby('class')['class'].count()
df.groupby(['class', 'survived']).count()
201/(201+123)
118/(118+166)
181/(181+528)
# Answer: 3rd class
df.shape
#------------------------------------------------------------------------------
