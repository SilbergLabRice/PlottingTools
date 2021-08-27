# PlottingTools
A collection of plotting scripts with basic application 

## General dependencies
* matplotlib
* numpy
* pandas

## Dyanmic grabber
Takes in slightly-reformatted .csv files output by kinetic runs when run in "by row" mode. 
Sample objects are defined under the main() function by editing the "plateKey" dictionary.
```
  plateKey=[{100:["A1","A2","A3"],50:["B1","B2","B3"], 25:["C1","C2","C3"]},
  {100:["A4","A5","A6"],50:["B4","B5","B6"], 25:["C4","C5","C6"]}]
```

The above plate key will create two sample objects, with three growth conditions each (100, 50, and 25).
