# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 02:01:03 2019

@author: Alfred Zane Rajan
"""

import pandas as pd

support = 50   #float(sys.argv[1])
confidence = 70     #float(sys.argv[2])
file = "apriori.txt"    #(sys.argv[3])
df = pd.read_csv( file, skipinitialspace = True, names = ['0', '1','2','3','4','5','6','7','8','9','10'])
df = df.drop('0', axis=1)
df = df.T
for col in df:
    df[col] = df[col].str.replace(" ", "")
db = list(list(df[i]) for i in df)
db = [[j for j in i if not pd.isna(j)] for i in db]
#for trans in db:
#item = ["diapers", "sweaters", "tissues", "belts", "water", "noodles", "cereals", "books", "pen", "batteries"]
items = []
for trans in db:
        for item in trans:
            if not item in items:
                items.append(item)
support = support*len(db)/100
confidence = confidence/100

count = {}
for item in items:
    count[item] = 0
for item in items:
    for trans in db:
        if item in trans:
            count[item]+=1
for item in items:
    if count[item] < support:
        items.remove(item)
    
itemsets = [{i} for i in items]
while itemsets:
    tempsets = []
    for iset in itemsets:
        for item in items:
            if not {item}.issubset(iset):
                match = 0
                total = 0
                for trans in db:
                    if iset.issubset(trans):
                        total+=1
                        if item in trans:
                            match+=1
                if match>=support:
                    temp = {i for i in iset}
                    temp.add(item)
                    if temp not in tempsets:
                        tempsets.append(temp)
                    if (match/total)>=confidence:
                        print(iset," -> ",item)
    itemsets = tempsets
    for item in items:
        flag = 0
        for iset in itemsets:
            if {item}.issubset(iset):
                flag = 1
        if flag == 0:
            items.remove(item)

    