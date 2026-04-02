#This scripts combines all generated csv files into training data for 1D-CNN model
import binascii
from csv import writer
import subprocess as sp
import os, json
import numpy as np
import pandas as pd

def colFill(fileName):
    df=pd.read_csv(fileName)
    lcol=len(df.columns)
    if df.columns[0]=='Label':
        print("with label")
        cols=['Label', 'Type', 'f_0']
        for i in range(1, lcol-2):
            cols.append('f_' +str(i))
    else:
        print("without label")
        cols=['Label', 'Type', 'f_0']
        #df['Label']= 'Malicious'
        #df['Type']= type
        for i in range(1, lcol):
            cols.append('f_' +str(i))
    df.columns=cols
    df.to_csv(fileName)

def colFill(flist):
	df1 = pd.read_csv(flist[0])
	df2 = pd.read_csv(flist[1])
	df3 = pd.read_csv(flist[2])
	df4 = pd.read_csv(flist[3])
	df5 = pd.read_csv(flist[4])
	#handle shape here. We take min here to handle dimensions. If you select max then fill the rest with zeros
	nrow=min(df1.shape[0], df2.shape[0], df3.shape[0], df6.shape[0], df5.shape[0])
	ncol=min(df1.shape[1], df2.shape[1], df3.shape[1], df6.shape[1], df5.shape[1])
	#['Unnamed: 0'] column handling, if there is one
	df1=df1.drop(columns=['Unnamed: 0'])
	df2=df2.drop(columns=['Unnamed: 0'])
	df3=df3.drop(columns=['Unnamed: 0'])
	df4=df4.drop(columns=['Unnamed: 0'])
	df5=df5.drop(columns=['Unnamed: 0'])
	
	dfa=pd.concat([df1,df2,df3,df6,df5], ignore_index=True, axis=0, sort=False)
	dfa.to_csv("showAll_training.csv")
    
if __name__=="__main__":
    thisdir=os.getcwd()
    #All the csv files are in `thisdir` folder
	flist = [f for f in os.listdir(thisdir) if f.startswith('showAll')]
    #Fix the column names
    for filename in flist:
    	colFill("showAll_benign.csv")
    #Merge files
    merge_csv(flist)
