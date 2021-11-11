# PlottingTools
A collection of plotting scripts for basic synthetic biology applications



## Dynamic grabber
Takes .csv formatted continuous/kinetic growth data (OD600) and makes a nice plot. This does not calculate growth rates etc. only does plotting.
_Manually grab the relevant data from the .xlsx output by kinetic runs and save as .csv files (this works when run in "by row" mode)_

- Define the way the samples should be split into distinct plots for distinct categories by : `normalNames=["Condition 1","Condition 2"]`
- Sample objects are defined under the main() function by editing the `"plateKey"`, which is a list of dictionaries that define which wells correspond to which growth conditions in the various samples.
```
  plateKey=[{100:["A1","A2","A3"],50:["B1","B2","B3"], 25:["C1","C2","C3"]},
  {100:["A4","A5","A6"],50:["B4","B5","B6"], 25:["C4","C5","C6"]}]
```

The above plate key will create two sample objects, with three growth conditions each (100, 50, and 25) that are defined by the well strings within their respective dictionaries.

Running the exampleData with these parameters gives the following plot 
![exampleData](https://user-images.githubusercontent.com/14856479/141382278-45028111-0f79-484b-95cb-c2438da45c39.png)

### General dependencies
_Make sure you install these with `pip install` or `conda install` before running the code`
* matplotlib
* numpy
* pandas


## Growth Curve Modeler (GCM)
A utility for modelling growth rate, lag time, and max optical density given a set of growth curves.  Algorithm citation (https://doi.org/10.1016/j.mimet.2016.11.015).  The folder contains the original algorithm, the conda environment (.yml file) needed to run the script, and a second script for formatting Tecan data for the gcm script.

Growth parameters are calculated by smoothing the data with a median filter, and then fitting to a modified logistic equation

This program has many dependancies so in order to make it easy to install all of them in one go, we use `Conda` environment manager (comes with `Anaconda` or a more minimal `Miniconda`)

Build conda environment:
```
$ conda env create -n RA -f RA.yml
```
_This installs all the perequisite packages such as Numpy, matplotlib etc. 
in a containerized environment so you don't need to worry about them individually. All these packages are named in the `RA.yml` file from where they are being read_

Activate RA environment
```
$ conda activate RA
```
_This activates the environment that has all the packages needed for the script_ 

After activating environment, follow these steps
1. Go to RA directory
2. Edit raPrepper.py to transform data of interest into RA format
   - Needs to be Tecan data
    - Copy and paste the “Table” values into csv (include Time, cycle number, temp, etc.)
   - Edit raPrepper.py variable: wellNamesMod to include list of wells of interest, but keep “Time [s]”.
   - Set desired DataDivisor value and max Data value in the main function at the bottom
3. Run raPrepper.py
```
$ python raPrepper.py
```
4. Save output csv as .xlsx file
5. Edit gcmRunner.py to “call” file of interest
6. Run gcmRunner.py
```
$ python gcmRunner.py
```
