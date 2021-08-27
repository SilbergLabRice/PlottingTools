# PlottingTools
A collection of plotting scripts for basic synthetic biology applications

## General dependencies
* matplotlib
* numpy
* pandas

## Dyanmic grabber
Takes in slightly-reformatted .csv files output by kinetic runs when run in "by row" mode. 
Sample objects are defined under the main() function by editing the "plateKey", which is a list of dictionaries that define which wells correspond to which growth conditions in the various samples.
```
  plateKey=[{100:["A1","A2","A3"],50:["B1","B2","B3"], 25:["C1","C2","C3"]},
  {100:["A4","A5","A6"],50:["B4","B5","B6"], 25:["C4","C5","C6"]}]
```

The above plate key will create two sample objects, with three growth conditions each (100, 50, and 25) that are defined by the well strings within their respective dictionaries.

## Growth Curve Modeler (GCM)
A utility for modelling growth rate, lag time, and max optical density given a set of growth curves.  Algorithm citation( .  The folder contains the original algorithm, the conda environment (.yml file) needed to run the script, and a second script for taking 

Build conda environment:
```
$ conda env create -n RA -f RA.yml
```

Activate RA environment
```
$ conda activate RA
```

After activating environment, follow these steps
1.Go to RA directory
2.Edit raPrepper.py to transform data of interest into RA format
  -Needs to be Tecan data
   -Copy and paste the “Table” values into csv (include Time, cycle number, temp, etc.)
  -Edit raPrepper.py variable: wellNamesMod to include list of wells of interest, but keep “Time [s]”.
  -Set desired DataDivisor value and max Data value in the main function at the bottom
3.Run raPrepper.py
```
$ python raPrepper.py
```
4.Save output csv as .xlsx file
5.Edit gcmRunner.py to “call” file of interest
6.Run gcmPrepper.py
```
$ python gcmPrepper.py
```
