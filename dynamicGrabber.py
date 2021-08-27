"""
Grabs a csv of dynamic growth data from the Tecan Spark.
Uses pandas to sort the data into a dataframe and 
uses a dictionary to group samples under different conditions (inducer concentrations) into one object.
Outputs a graph of each sample object, with all conditions for one object on the same graph.
"""


from matplotlib import pyplot as pp
import csv, re
import numpy as np
from matplotlib.ticker import Locator
from matplotlib.font_manager import FontProperties
from matplotlib import rc
import matplotlib.ticker as plticker
import pandas as pd

rc('font',**{'family':'sans-serif','sans-serif':['Segoe UI']})
rc('ytick',**{'major.size': 5})
rc('xtick',**{'major.size': 5})
rc('ytick',**{'labelsize': 10})
rc('xtick',**{'labelsize': 10})
rc('axes',**{'labelsize': 12})
rc('svg', **{'fonttype': 'none'})

"""Defining Sample Class
-Should take in sample name as .name
-Should take in pandas dataframes as .data
-Upon instantiation should calculate the average of .data dataframes and save as .mean attribute
-Upon instantiation should calculate the standard deviation of .data dataframes and save as .std attribute
-Dependent on pandas package for dataframes and numpy for calculation of mean and std 
"""
class Sample:
  def __init__(self, name, data):
    self.name=name
    self.data=data
    
    meanDict={}
    stdDict={}
    for key in data.keys():
      meanDict[key]=data[key].mean() #Calculates mean for each inducer and dumps into new meanDict
      stdDict[key]=data[key].apply(np.std) #Calculates std for each inducer and dumps into new meanDict
    
    self.meanDict=meanDict    
    self.stdDict=stdDict

def plate_Grabber(file_name):
  plate=pd.read_csv(file_name, index_col=0, encoding = "ISO-8859-1")
  return plate


"""Function that divides up dense data into fewer point 
and truncates data, if values are given.
Otherwise, it returns the dataframe it is given.
"""
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

def babyPlotter(time, samples, fileHandle):
  samples=samples
  sampleCount = len(samples)
  #Setup figure parameters
  figWidth = 7.08*2/3
  figHeight = 2
  fig, axs = pp.subplots(1,2, figsize=(figWidth, figHeight),constrained_layout=True)

  color1= [229/255.0, 57/255.0, 53/255.0,1] #Rich red
  color2= [255/255.0, 111/255.0, 0/255.0,1] #A&M orange
  color3= [48/255.0, 63/255.0, 159/255.0,1] #Deep Blue
  color4= [0/255.0, 188/255.0, 212/255.0,1] #Soft torquoise
  color5= [255/255.0, 235/255.0, 59/255.0,1] #King's yellow
  color6= [103/255.0, 58/255.0, 183/255.0,1] #Imperator's purple
  color7= [2/255.0, 163/255.0, 209/255.0,1] #Sea Blue
  color8= [139/255.0, 195/255.0, 74/255.0,1] #Vibrant green    

  colorList=[color3, color8, color1, color2, color6, color4]
  purpleColorGradient=["#B89BD4","#9B63CD","#8130C6","#6900BF"]
  redColorGradient=["#D49BA9", "#A36777", "#723346", "#420015"]
  redColorGradient_rev=redColorGradient[::-1]
  labelList= ["A","B","C","D","E","F","G","H","I","J"]

  #axs_flat=[item for sublist in axs for item in sublist]
  #Cycle through samples and plot each one, cycling through each inducer concentration to plot first error from stdDict and then the scatter plot from meanDict
  singleConcentration=25
  for i in range(sampleCount):
    sample=samples[i]
    ax = axs[i]

    ax.plot(time, sample.meanDict[singleConcentration], color = redColorGradient_rev[3], label = str(singleConcentration) + " mM", linewidth=3, zorder=100)

    eAll=[]
    e = ax.errorbar(time, sample.meanDict[singleConcentration], yerr = sample.stdDict[singleConcentration],  linestyle = '-', color = (0,0,0,0.8), capsize = 0, zorder=50, clip_on=False)
    eAll.append(e)

    #Turn off all error bar clips for all inducer concentrations
    for e in eAll:
        for b in e[1]:
            b.set_clip_on(False)
        for b in e[2]:
            b.set_clip_on(False)

    #ax.text(-0.9,0.62,labelList[i], fontsize=16)  #Setting up A, B, or C at top left corner of each sub figure

    ax.set_title(sample.name)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 0.5) , fontsize=10)
    ax.legend(frameon=False, fontsize=6)

    #Turn off symlog stuff for just a timecourse
    #ax.set_xscale("symlog")
    #ax.xaxis.set_minor_locator(MinorSymLogLocator(1e-1))
    ax.set_xlim([0, 2])
    ax.set_xticks([0,0.5,1,1.5,2])
    #ax.set_yticks([0,0.2,0.4,0.6])
    #ax.set_ylim([0, 0.6])

    ax.set_ylabel("OD$_{600}$")
    ax.set_xlabel('Time (days)')
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


  #Plot all 100 aTc inductions state on the last axis together
  """for i, sample in enumerate(samples):
    lastAx=axs_flat[6]
    lastAx.plot(time,sample.meanDict[100], color=colorList[i], label = sample.name , linewidth=3, zorder=100)
    lastAx.legend(loc='upper left', bbox_to_anchor=(1.05, 0.5) , fontsize=10)
    lastAx.legend(frameon=False, fontsize=6)
    lastAx.set_xlim([0, 1])
    lastAx.set_xticks([0,0.25,0.5,0.75,1])
    lastAx.set_yticks([0,0.2,0.4,0.6])
    lastAx.set_ylim([0, 0.6])
    lastAx.spines['right'].set_visible(False)
    lastAx.spines['top'].set_visible(False)'"""

  #fileout = re.findall('(.*).csv', fileName)[0] + '.svg'
  fileHandle=str(singleConcentration)
  fileout =  fileHandle + '.png'
  pp.savefig(fileout)
  pp.savefig(fileHandle+'.svg')


def plotter(time, samples, fileHandle):
  samples=samples
  sampleCount = len(samples)
  #Setup figure parameters
  figWidth = 7.08*2/3
  figHeight = 2
  fig, axs = pp.subplots(1,2, figsize=(figWidth, figHeight),constrained_layout=True)

  color1= [229/255.0, 57/255.0, 53/255.0,1] #Rich red
  color2= [255/255.0, 111/255.0, 0/255.0,1] #A&M orange
  color3= [48/255.0, 63/255.0, 159/255.0,1] #Deep Blue
  color4= [0/255.0, 188/255.0, 212/255.0,1] #Soft torquoise
  color5= [255/255.0, 235/255.0, 59/255.0,1] #King's yellow
  color6= [103/255.0, 58/255.0, 183/255.0,1] #Imperator's purple
  color7= [2/255.0, 163/255.0, 209/255.0,1] #Sea Blue
  color8= [139/255.0, 195/255.0, 74/255.0,1] #Vibrant green    

  colorList=[color3, color8, color1, color2, color6, color4]
  purpleColorGradient=["#B89BD4","#9B63CD","#8130C6","#6900BF"]
  redColorGradient=["#D49BA9", "#A36777", "#723346", "#420015"]
  redColorGradient_rev=redColorGradient[::-1]
  labelList= ["A","B","C","D","E","F","G","H","I","J"]

  #axs_flat=[item for sublist in axs for item in sublist]
  #Cycle through samples and plot each one, cycling through each inducer concentration to plot first error from stdDict and then the scatter plot from meanDict
  for i in range(sampleCount):
    sample=samples[i]
    ax = axs[i]

    j=0
    for key in sample.meanDict.keys():    
      #ax.scatter(time, sample.meanDict[key],  label = str(key) + " aTc (ng/mL)", marker= "o", edgecolor = (0,0,0,0), facecolor = redColorGradient[j], zorder=100, clip_on=False)
      ax.plot(time, sample.meanDict[key], color = redColorGradient_rev[j], label = str(key) + " mM", linewidth=3, zorder=100)
      j+=1

    eAll=[]
    #Plot each std and for all inducer concentrations, cycling through the keys (inducer concentrations)
    j=0
    for key in sample.stdDict.keys():
      e = ax.errorbar(time, sample.meanDict[key], yerr = sample.stdDict[key],  linestyle = '-', color = (0,0,0,0.8), capsize = 0, zorder=50, clip_on=False)
      eAll.append(e)
      j+=1

    #Turn off all error bar clips for all inducer concentrations
    for e in eAll:
        for b in e[1]:
            b.set_clip_on(False)
        for b in e[2]:
            b.set_clip_on(False)

    #ax.text(-0.9,0.62,labelList[i], fontsize=16)  #Setting up A, B, or C at top left corner of each sub figure

    ax.set_title(sample.name)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 0.5) , fontsize=10)
    ax.legend(frameon=False, fontsize=6)

    #Turn off symlog stuff for just a timecourse
    #ax.set_xscale("symlog")
    #ax.xaxis.set_minor_locator(MinorSymLogLocator(1e-1))
    ax.set_xlim([0, 2])
    ax.set_xticks([0,0.5,1,1.5,2])
    ax.set_yticks([0,0.2,0.4,0.6])
    ax.set_ylim([0, 0.6])

    ax.set_ylabel("OD$_{600}$")
    ax.set_xlabel('Time (days)')
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


  #Plot all 100 aTc inductions state on the last axis together
  """for i, sample in enumerate(samples):
    lastAx=axs_flat[6]
    lastAx.plot(time,sample.meanDict[100], color=colorList[i], label = sample.name , linewidth=3, zorder=100)
    lastAx.legend(loc='upper left', bbox_to_anchor=(1.05, 0.5) , fontsize=10)
    lastAx.legend(frameon=False, fontsize=6)
    lastAx.set_xlim([0, 1])
    lastAx.set_xticks([0,0.25,0.5,0.75,1])
    lastAx.set_yticks([0,0.2,0.4,0.6])
    lastAx.set_ylim([0, 0.6])
    lastAx.spines['right'].set_visible(False)
    lastAx.spines['top'].set_visible(False)'"""

  #fileout = re.findall('(.*).csv', fileName)[0] + '.svg'
  fileout =  fileHandle + '.png'
  pp.savefig(fileout)
  pp.savefig(fileHandle+'.svg')

def main():
  fileHandle='210521_MHT_salt_titration_lab'
  file = fileHandle+'.csv'
  #fileHandle='210401_sEMF60_barCodeTest_core'
  #file = fileHandle+'.csv'

  normalNames=["NaBr","NaCl"]

  divisor=10
  maxValue=1000
  startAdjust=0
  #maxValue=None

  #plateKey is a list of dictionaries.  Each dictionary corresponds to a name.  Each dictionary has inducer concentration as the keys and the associated wells as the values.
  plateKey=[{100:["A1","A2","A3"],50:["B1","B2","B3"], 25:["C1","C2","C3"]},
  {100:["A4","A5","A6"],50:["B4","B5","B6"], 25:["C4","C5","C6"]}]


  plate=plate_Grabber(file)
  plate.loc["Time [s]"]=plate.loc["Time [s]"].apply(lambda x : (x/(3600*24))+startAdjust) #turning seconds to hours to days and adjusting for missing data in the beginning

  dataDicts=[]
  
  for sample in plateKey:
    workingDict={}

    for key in sample.keys():
      rawData=plate.loc[sample[key]]#Looks up the data in the plate dataframe for each sample based on the well nametag (via the sample dictionary; the key is the induct concentration)
      minimizedData=dataDivider(rawData,maxValue,divisor)
      #print(minimizedData)
      workingDict[key]=minimizedData
    dataDicts.append(workingDict)

  """Instantiates sample objects using names and data dictionaries.
  Names and corresponding data dicts must be in the same order.
  Generates sample objects with samples names, and a dictionary that gives out the three data traces when given the inducer concentration as the key.""" 
  sampleBox=[] #Box to store samples in
  for i in range(len(normalNames)):
    newSample=Sample(normalNames[i], dataDicts[i])
    sampleBox.append(newSample)

  rawTimeCourse=plate.loc["Time [s]"]

  truncatedTimeCourse=rawTimeCourse.iloc[:maxValue]# Truncate timecourse to the endpoint we want
  timeCourse=truncatedTimeCourse[::divisor]# Divide up timecourse by the divisor selected to make dataset smaller

  plotter(timeCourse, sampleBox, fileHandle)
  babyPlotter(timeCourse, sampleBox, fileHandle)

if __name__ == "__main__":
    main()