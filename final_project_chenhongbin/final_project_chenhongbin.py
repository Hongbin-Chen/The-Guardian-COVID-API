#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import numpy as np
import json
import re


# In[2]:


def access_data_from_guardian():
    """
    First discovered in January 2020, we have suffered from COVID-19 for almost a whole year. 
    It is of great urgency to continuously update our knowledge about the virus.
    It is kind of a bummer that the API only return 9 results at a time for public user. However, we are going to design our function in a base of generalizaiton. If wanting to get more result, contact the Guardian Office.
    Instead of using and showing my api key, I use the "test" key here.
    This function requests data about COVID-19 from Guardian REST API v1
    
    ----------
    Parameters:
    key word q: coivd
    api key: can acquire a key by registering an account

    """
    r = requests.get('https://content.guardianapis.com/search?from-date=2019-12-31&to-date=2020-12-01&q=covid&api-key=test')
    if r.status_code != 200:
        print("fail to access to API")
        sys.exit()
    elif r.status_code == 200:
        print("successful!")
    data_json = r.json()
    return(data_json)


# In[3]:


#Example code:
datainjson = access_data_from_guardian()
datainjson


# In[4]:


def transform_format(value):
    """
    This function is used to transform the data into pd.DataFrame
    ---------
    Input:
    value = data
    
    ----------
    Output:
    data in the form of pd.DataFrame
    
    ----------
    Example:
    data_dataframe = transform_format(datainjson)
    data_dataframe
    
    		response
	currentPage	1
	orderBy	relevance
	pageSize	10
	pages	2690
	results	[{'id': 'society/2020/nov/26/covid-vaccine-tri...
	startIndex	1
	status	ok
	total	26891
	userTier	external
    
    """
    data_dataframe = pd.DataFrame(value)
    return data_dataframe


# In[5]:


#Example code:
data_dataframe = transform_format(datainjson)
data_dataframe


# In[6]:


def show_the_keys():
    """
    This function is used to show the headtitles of the data we got in the form of pd.DataFrame
    
    ---------
    Example:
    show_the_keys()
    
    Index(['currentPage', 'orderBy', 'pageSize', 'pages', 'results', 'startIndex',
       'status', 'total', 'userTier'],
      dtype='object')
    
    """
    data_keys = data_dataframe['response'].keys()
    return data_keys


# In[7]:


#Example code:
show_the_keys()


# In[8]:


def focus_on_results(value):  
    """
    This function is designed to focus on the results we got from the original data, where there is the most valuable information from the API.
    Of course, for the purpose of generalization, the user can focus their attension on any of the subtitle we want. This is why I set the value as a input.
    ----------
    Input:
    value = the subtitle you want to focus (results)
   
    --------- 
    Output:
    detailed information in that input.
    
    ----------
    Example:
    results = focus_on_results('results')
    results[0:3]
    
    id	type	sectionId	sectionName	webPublicationDate	webTitle	webUrl	apiUrl	isHosted	pillarId	pillarName
	0	society/2020/nov/26/covid-vaccine-trials-shoul...	article	society	Society	2020-11-26T17:49:27Z	Covid vaccine trials should continue | Letters	https://www.theguardian.com/society/2020/nov/2...	https://content.guardianapis.com/society/2020/...	False	pillar/news	News
	1	australia-news/2020/oct/06/us-election-briefin...	article	australia-news	Australia news	2020-10-06T06:31:18Z	US election briefing for Australia: Trump clai...	https://www.theguardian.com/australia-news/202...	https://content.guardianapis.com/australia-new...	False	pillar/news	News
	2	world/2020/nov/15/covid-deaths-and-learning-di...	article	world	World news	2020-11-15T18:26:26Z	Covid deaths and learning disabilities	https://www.theguardian.com/world/2020/nov/15/...	https://content.guardianapis.com/world/2020/no...	False	pillar/news	News
    
    """
    the_results = pd.DataFrame(data_dataframe['response'][value])
    return the_results


# In[9]:


#Example code:
results = focus_on_results('results')
results[0:3]


# In[10]:


def focus_on_a_topic(value):
    """
    This function helps the user to search for the news according to their interest. 
    Since each newes has its belonging section Id, we use it as the input.
    -------
    Input:
    value = the topic you are interested in
    
    -------
    Output:
    alll the relevant news based on the name of the topic
    
    -------
    Example:
    If users want to know how the covid situation around the world, they can put "world" in the value.
    
    focus_on_a_topic('world')
    
    id	type	sectionId	sectionName	webPublicationDate	webTitle	webUrl	apiUrl	isHosted	pillarId	pillarName
	2	world/2020/nov/15/covid-deaths-and-learning-di...	article	world	World news	2020-11-15T18:26:26Z	Covid deaths and learning disabilities	https://www.theguardian.com/world/2020/nov/15/...	https://content.guardianapis.com/world/2020/no...	False	pillar/news	News
	4	world/2020/nov/29/eleanor-morgan-is-still-stru...	article	world	World news	2020-11-29T11:00:25Z	Long Covid: ‘Is this now me forever?’	https://www.theguardian.com/world/2020/nov/29/...	https://content.guardianapis.com/world/2020/no...	False	pillar/news	News
	7	world/2020/dec/01/making-a-meal-of-covid-restr...	article	world	World news	2020-12-01T17:34:09Z	Making a meal of Covid restrictions | Brief le...	https://www.theguardian.com/world/2020/dec/01/...	https://content.guardianapis.com/world/2020/de...	False	pillar/news	News
	8	world/2020/dec/01/how-to-get-covid-deniers-to-...	article	world	World news	2020-12-01T17:34:55Z	How to get Covid deniers to vaccinate | Letters	https://www.theguardian.com/world/2020/dec/01/...	https://content.guardianapis.com/world/2020/de...	False	pillar/news	News
	9	world/2020/nov/06/how-uk-government-misreprese...	article	world	World news	2020-11-06T14:43:29Z	How UK government misrepresented Covid project...	https://www.theguardian.com/world/2020/nov/06/...	https://content.guardianapis.com/world/2020/no...	False	pillar/news	News
    
    """
    topic_interestd = results[results['sectionId']==value]
    return topic_interestd


# In[11]:


#Example code:
focus_on_a_topic('world')


# In[12]:


def news_type(value):
    """
    Some people might feel tired in reading but love watch video, it is helpful to just leave the news in video form.
    This function helps the user to search for the news with some types of form. 
    Since each newes has its belonging type, we use it as the input.
    ---------
    Input:
    value = the form you want
    
    --------
    Output:
    Only leave the news in the form you want
    
    --------
    Example:
    news_type('video')
    
    id	type	sectionId	sectionName	webPublicationDate	webTitle	webUrl	apiUrl	isHosted	pillarId	pillarName
	9	australia-news/video/2020/nov/23/112-days-insi...	video	australia-news	Australia news	2020-11-22T16:30:26Z	112 Days: inside Melbourne's Covid lockdown – ...	https://www.theguardian.com/australia-news/vid...	https://content.guardianapis.com/australia-new...	False	pillar/news	News

    """
    type_interestd = results[results['type']==value]
    return type_interestd


# In[13]:


#Example1 code:
news_type('video')
#Noted: there are lots of type of news, including article, video and so on. The 9 reuslts we got are not exhausted all the types.



