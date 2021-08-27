"""
Grabs a csv of dynamic growth data from the Tecan Spark.
Uses pandas to sort the data into a dataframe and prepare for RA code

"""
import csv, re
import numpy as np
import pandas as pd
import sys

global wellNames
wellNames= [["Time [s]"],
"A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12",
"B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11","B12",
"C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12",
"D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","D12",
"E1","E2","E3","E4","E5","E6","E7","E8","E9","E10","E11","E12",
"F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",
"G1","G2","G3","G4","G5","G6","G7","G8","G9","G10","G11","G12",
"H1","H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12"]

global wellNamesMod
wellNamesMod= [["Time [s]"],
"B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11","B12",
"G1","G2","G3","G4","G5","G6","G7","G8","G9","G10","G11","G12"]

def plate_Grabber(file_name):
  plate=pd.read_csv(file_name, index_col=0, encoding = "ISO-8859-1")
  return plate

def dataDivider(df,maxValue=None,divisor=None):
  rawData=df
  if maxValue:  
    truncatedData=rawData.iloc[:,:maxValue]#Select data only up to the max you want
  else:
    truncatedData=rawData
      
  if divisor:
    minimizedData=truncatedData[truncatedData.columns[::divisor]] #Only take every n columns where n is the divisor value
  else:
    minimizedData=truncatedData
 
  return minimizedData

def fileWriter(plate,fileName):
  with open('RA_'+fileName,'w', newline="") as csvfile:
    halfWriter= csv.writer(csvfile)
    halfWriter.writerow([""]+["M9Sa" for x in range(len(wellNamesMod)-1)])
    halfWriter.writerow(["Time"]+wellNamesMod[1:])

    for name in plate:
      col=plate[name]
      data=[float(col[x]) for x in wellNamesMod]
      halfWriter.writerow(data)
     
def main():
  fileName = 'example_gcm_data.csv'
  divisor=10
  maxValue=None
  
  plate=plate_Grabber(fileName)
  plate.loc["Time [s]"]=plate.loc["Time [s]"].apply(lambda x : x/(3600)) #turning seconds to hours
  plate=dataDivider(plate,maxValue,divisor)
  fileWriter(plate,fileName)

if __name__ == "__main__":
    main()