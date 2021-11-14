# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 11:17:19 2021

@author: ericr
"""
import pandas as pd
import numpy as np
import os
import re
import requests
from helpFunctions import *
from constants import *

def getStats(years):
    ##############################################################################
    # Flags - do not scrape/overwrite data by default
    overwrite_enabled = False
    scrape_base = False
    
    ##############################################################################
    # Load player data
    weekly_combined = []
    annual_combined = []
    
    if not os.path.isdir('Stats'):
        response = input("*/Stats* directory not found.\nWould you like to get the data from the web?\n (WARNING: This takes a couple hours)\n (y/n)")
        if response.lower() == 'y':
            overwrite_enabled = True
            scrape_base = True
            os.mkdir('Stats')
        elif not response.lower() == 'n':
            raise ValueError("Please enter either y or n")
    
    # Year to get data
    # 2013 is the earliest ADP data available
    for year in years:
        print("********************\nYear: " + str(year))
                
        # Weekly output file format, only write header on first line of file
        weekly_outfile = 'Stats/WeeklyStats_' + str(year) + '.csv'
        if os.path.isfile(weekly_outfile) and overwrite_enabled:
            os.remove(weekly_outfile)
        annual_outfile = 'Stats/AnnualStats_' + str(year) + '.csv'
        if os.path.isfile(annual_outfile) and overwrite_enabled:
            os.remove(annual_outfile)
        writeHeader = True
        
    ##############################################################################
        # Scrape data for ADP and game stats
        if scrape_base:
           
            # Get ADP data for year's player list
            df = scrapeADP(year, overwrite_enabled)
            
            scrapePlayerStats(year, df, writeHeader, weekly_outfile, annual_outfile, overwrite_enabled)
    ##############################################################################
        # End player load. Load these stats to make appended list and add year
        temp = pd.read_csv(weekly_outfile)
        temp['Year'] = year
        weekly_combined.append(temp)
        
        temp = pd.read_csv(annual_outfile)
        temp['Year'] = year
        annual_combined.append(temp)
    
    # Combine all stats to save to file
    weekly_combined = pd.concat(weekly_combined)
    annual_combined = pd.concat(annual_combined)
    
    if overwrite_enabled:
        weekly_combined.to_csv("Stats/WeeklyCombined.csv")
        annual_combined.to_csv("Stats/AnnualCombined.csv")
    
    
    
    return weekly_combined, annual_combined