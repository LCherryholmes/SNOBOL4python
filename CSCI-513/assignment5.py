#------------------------------------------------------------------------------
import pandas as pd
verbose = False
titanic = pd.read_csv("./titanic.csv")
#------------------------------------------------------------------------------
print("1. How many rows do we have?", end=" ")
print(titanic.shape[0])
#------------------------------------------------------------------------------
print("2. How many columns do we have?", end=" ")
print(titanic.shape[1])
#------------------------------------------------------------------------------
print("3. Which columns are numeric in value?", end=" ")
if verbose: print(titanic.dtypes)
if verbose: print(titanic.dtypes[titanic.dtypes == "int64"])
if verbose: print(titanic.dtypes[titanic.dtypes == "float64"])
if verbose: print((titanic.dtypes == "int64") | (titanic.dtypes == "float64"))
if verbose: print(titanic.dtypes[(titanic.dtypes == "int64") | (titanic.dtypes == "float64")])
if verbose: print(titanic.dtypes[(titanic.dtypes == "int64") | (titanic.dtypes == "float64")].values)
if verbose: print(titanic.dtypes[(titanic.dtypes == "int64") | (titanic.dtypes == "float64")].index)
print(titanic.dtypes[(titanic.dtypes == "int64") | (titanic.dtypes == "float64")].index.tolist())
#------------------------------------------------------------------------------
print("4. How many people were traveling to New York city?", end=" ")
if verbose: print(titanic.columns)
if verbose: print(titanic["home.dest"])
if verbose: print(titanic["home.dest"].unique())
if verbose: print(titanic[titanic["home.dest"].str.contains("NY")])
if verbose: print(titanic[titanic["home.dest"].str.contains("New York, NY")])
if verbose: print(titanic[titanic["home.dest"].str.contains("New York, NY")]["home.dest"])
if verbose: print(titanic[titanic["home.dest"].str.contains("New York, NY")]["home.dest"].unique())
if verbose: print(titanic[titanic["home.dest"].str.contains(r"(?:^| )New York, NY$")]["home.dest"].unique())
if verbose: print(titanic[titanic["home.dest"].str.contains(r"(?:^| )New York, NY$")])
if verbose: print(titanic[titanic["home.dest"].str.contains(r"(?:^| )New York, NY$")].shape)
print(titanic[titanic["home.dest"].str.contains(r"(?:^| )New York, NY$")].shape[0])
#------------------------------------------------------------------------------
print("5. Which fare was bought the most?", end=" ")
if verbose: print(titanic.columns)
if verbose: print(titanic.fare)
if verbose: print(titanic.fare.unique())
if verbose: print(titanic.fare.sort_values(ascending=False))
if verbose: print(titanic.groupby(["fare"]))
if verbose: print(titanic.groupby(["fare"]).size().reset_index(name='counts'))
if verbose: print(titanic.groupby(["fare"]).size().reset_index(name='counts').sort_values("counts", ascending=False))
if verbose: print(titanic.groupby(["fare"]).size().reset_index(name='counts').sort_values("counts", ascending=False).iloc[0])
print(titanic.groupby(["fare"]).size().reset_index(name='counts').sort_values("counts", ascending=False).iloc[0].fare)
#------------------------------------------------------------------------------
print("6. What is the highest paid fare?", end=" ")
if verbose: print(titanic.max())
print(titanic.max().fare)
#------------------------------------------------------------------------------
print("7. How many females survived the crash?", end=" ")
if verbose: print(titanic.columns)
if verbose: print(titanic.sex.unique())
if verbose: print(titanic.survived.unique())
if verbose: print(titanic[titanic.sex == "female"])
if verbose: print(titanic[titanic.survived == 1])
if verbose: print(titanic[(titanic.sex == "female") & (titanic.survived == 1)])
if verbose: print(titanic[(titanic.sex == "female") & (titanic.survived == 1)].shape)
print(titanic[(titanic.sex == "female") & (titanic.survived == 1)].shape[0])
#------------------------------------------------------------------------------
print("8. How many males survived the crash?", end=" ")
print(titanic[(titanic.sex == "male") & (titanic.survived == 1)].shape[0])
#------------------------------------------------------------------------------
print("9. How many survivors purchased a 2nd class ticket?", end=" ")
if verbose: print(titanic.columns)
if verbose: print(titanic.pclass.unique())
if verbose: print(titanic[titanic.pclass == 2])
if verbose: print(titanic[titanic.pclass == 2].shape)
print(titanic[titanic.pclass == 2].shape[0])
#------------------------------------------------------------------------------
print("10. Draw a pie plot to show the age count for the survivors.")
print("11. Draw a bar plot of the count of people in each boat. Do not include in the plot the '?' value.")
print("Press ENTER key when ready for consecutive pop-up windows: ", end=""); input()
import matplotlib.pyplot as pyplot
#titanic[titanic["age"] == '?'] = -1
titanic.loc[titanic["age"] == '?', "age"] = -1
titanic['age'] = titanic['age'].astype(float)
if verbose: print(titanic.age.unique())
if verbose: print(len(titanic.age.unique()))
if verbose: print(sorted(titanic.age.unique()))
if verbose: print(titanic[titanic.survived == 1].value_counts())
if verbose: print(titanic[titanic.survived == 1].groupby(["age"]).size().reset_index(name='counts'))
if verbose: print(titanic[titanic.survived == 1].groupby(["age"]).size().reset_index(name='counts').columns)
if verbose: print(titanic[titanic.survived == 1].groupby(["age"]).size())
#  Answer is:
ages = titanic[titanic.survived == 1] \
        .sort_values(by="age", ascending=False) \
        .groupby(["age"]) \
        .size()
(   ages.plot(
            kind = "pie",
            use_index = False,
            y = "age",
            ylabel = "Age",
            title = "Count of the ages of the survivors",
            figsize = (11.0, 6.8),
            fontsize = 8,
            legend = True,
            autopct = "",
            labels = [''] * len(ages),
            colors = [
                "Blue", "Green", "Red", "Cyan", "Magenta", "Yellow", "Black",
                "Gray", "Maroon", "Olive", "Navy", "Teal", "Aqua",
                "Lime", "Fuchsia", "Purple", "Silver", "Gold", "Orange",
                "Brown", "Pink", "Violet", "Indigo", "Lavender", "Chocolate",
                "Coral", "Crimson", "DarkBlue", "DarkGreen", "DarkRed",
                "DeepPink", "DeepSkyBlue", "DimGray", "DodgerBlue", 
                "FireBrick", "ForestGreen", "GoldenRod", "HotPink", 
                "IndianRed", "Khaki", "LightBlue", "LightCoral", "LightGreen",
                "LightPink", "LightSalmon", "LightSeaGreen", "LightSkyBlue",
                "LightSlateGray", "LightSteelBlue", "LimeGreen", "MediumBlue",
                "MediumOrchid", "MediumPurple", "MediumSeaGreen",
                "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise",
                "MediumVioletRed", "MidnightBlue", "OliveDrab", "OrangeRed",
                "Orchid", "PaleVioletRed", "PeachPuff", "Peru", "Plum", 
                "PowderBlue", "RoyalBlue", "Salmon", "SeaGreen",
                "DarkOrange"])
        .legend(
            bbox_to_anchor = (1, 1),
            loc = 'upper left',
            ncol = 3,
            prop={'size': 8},
            markerscale = 0.6,
            labels = ages.index,
            frameon = True)
)        
pyplot.savefig("ages.png")
pyplot.show()
pyplot.close()
#------------------------------------------------------------------------------
if verbose: print(titanic.columns)
if verbose: print(titanic.boat.unique())
if verbose: print(titanic[titanic.boat != '?'].groupby(["boat"]).size())
#  Answer is:
(   titanic[titanic.boat != '?']
        .groupby(["boat"])
        .size()
        .reset_index(name='count')
        .plot(
            kind = "bar",
            use_index = True,
            x = "boat",
            y = "count",
            title = "Count of the survivors in each boat",
            xlabel = "Boat",
            ylabel = "Count",
            rot = "vertical",
            figsize = (10.0, 6.8),
            fontsize = 8)
)
pyplot.savefig("boats.png")
pyplot.show()
pyplot.close()
#------------------------------------------------------------------------------
