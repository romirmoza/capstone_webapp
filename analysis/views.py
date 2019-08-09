from django.shortcuts import render
from wordcloud import WordCloud, STOPWORDS
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

def  analysis(request):
    module_dir = os.path.dirname(__file__) 
    file_path = os.path.join(module_dir, '911_Police_Calls_for_Service.csv')
    
    data911 = pd.read_csv(file_path)
    #data911['CallDateTime'] = pd.to_datetime(data911['CallDateTime'])
    #data911.info()
    
    for i in range(2003, 2019):
        year = str(i)
        data911.loc[data911['CallDateTime'].str.find(year) != -1,'Year'] = int(i)
    
    d = data911.groupby(['PoliceDistrict','Year']).count()['RecordID'].unstack()

    figsizx = 8
    figsizy = 8
    #plt.figure(1)
    d.plot.bar(figsize = (figsizx, figsizy), stacked = False)
   
    file_path = os.path.abspath(os.curdir) + '/static/img/plot1.png'
    plt.savefig(file_path, bbox_inches="tight")
    
    d = data911.groupby(['Year', 'PoliceDistrict']).count()['RecordID'].unstack()
    #print(d)
    plt.figure(2)
    fig = d.boxplot(figsize = (figsizx, figsizy))
    fig.set_title('District vs # 911 calls', size = 10)
    fig.set_xlabel('Police Districts', size = 10)
    fig.set_ylabel('# of 911 calls', size = 10)
    fig.tick_params(axis='x', rotation=45)
	
    file_path = os.path.abspath(os.curdir) + '/static/img/plot2.png'
    plt.savefig(file_path, bbox_inches="tight")
	
	
    data911['Description'] = data911['Description'].str.lower()
    data911['Description'] = data911['Description'].replace(to_replace = '911/no  voice' , value = '911/no voice')
    wordcloud = WordCloud(width = 1000, height = 1000, stopwords = STOPWORDS).generate(str(data911.Description.to_string()))
    
    plt.figure(num = 3, figsize = (figsizx, figsizy), facecolor = 'k', edgecolor = 'k')
    
    file_path = os.path.abspath(os.curdir) + '/static/img/wordcloud.png'
    plt.savefig(file_path, bbox_inches="tight")
    wordcloud.to_file(file_path)
    #plt.imshow(wordcloud, interpolation = 'bilinear')

    #print(data911.groupby('Description')['Description'].count().sort_values(ascending = False).head(10))


    d = data911[data911['Description'].str.find('disorderly') != -1]
    d = d.groupby(['Year', 'PoliceDistrict']).count()['RecordID'].unstack()

    plt.figure(4)
    fig = d.boxplot(figsize = (figsizx, figsizy))
    fig.set_title('District vs # 911 calls regarding disorderly conduct', size = 10)
    fig.set_xlabel('Police Districts', size = 10)
    fig.set_ylabel('# of 911 calls', size = 10)	
    fig.tick_params(axis='x', rotation=45)

    file_path = os.path.abspath(os.curdir) + '/static/img/plot3.png'
    plt.savefig(file_path, bbox_inches="tight")
	
    return render(request, 'analysis.html', {})
