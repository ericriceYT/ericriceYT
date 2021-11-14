# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 17:28:09 2021

@author: ericr
"""
import pandas as pd
from constants import *
import os
import re
import requests

from multiprocessing import Pool

##############################################################################
# helper functions
# Function takes in name from ADP website and returns players name, position, and team
def format_adp_name(pname):
    temp = pname.replace(',', '')
    temp = temp.split(' ')
    pos = temp.pop(-1)
    team = temp.pop(-1)
    name = temp.pop(-1)
    for s in temp:
        name = name + ' ' + s
    return name, pos, team


##############################################################################
# List of player name exceptions on NFL.com game logs
def name_exceptions(row, year):
        if (row['Player'] == 'Charles Johnson'):
            row['Player'] = 'Charles D Johnson'
        if (row['Player'] == 'Josh Robinson'):
            row['Player'] = 'Josh Robinson 2'
        if (row['Player'] == 'Michael Vick'):
            row['Player'] = 'Mike Vick'
        if (row['Player'] == 'Ben Watson'):
            row['Player'] = 'Benjamin Watson'
        if (row['Player'] == 'Tim Wright'):
            row['Player'] = 'Timothy Wright'
        if (row['Player'] == 'E.J. Manuel'):
            row['Player'] = 'EJ Manuel'
        if (row['Player'] == 'A.J. McCarron'):
            row['Player'] = 'AJ McCarron'
        if (row['Player'] == 'Robert Housler'):
            row['Player'] = 'Rob Housler'
        if (row['Player'] == 'Greg Little'):
            row['Player'] = 'Greg Little 2'
        if (row['Player'] == 'Stevie Johnson'):
            row['Player'] = 'Steve Johnson'
        if (row['Player'] == 'Ted Ginn Jr.'):
            row['Player'] = 'Ted Ginn'
        if (row['Player'] == 'Leonte Carroo'):
            row['Player'] = 'Leonte Q Carroo'
        if (row['Player'] == 'Ryan Griffin'):
            row['Player'] = 'Ryan Francis Griffin'
        if (row['Player'] == 'Mike Thomas'):
            row['Player'] = 'Mike Thomas 2'
        if (row['Player'] == 'Antonio Gibson'):
            row['Player'] = 'Antonio Gibson 2'
        if (row['Player'] == 'De\'Angelo Henderson'):
            row['Player'] = 'De\'Angelo Henderson Sr'
        if (row['Player'] == 'Josh Allen'):
            row['Player'] = 'Josh Allen 4'
        if (row['Player'] == 'DK Metcalf'):
            row['Player'] = 'D K Metcalf'
        if (row['Player'] == 'JJ Arcega-Whiteside'):
            row['Player'] = 'J J Arcega-Whiteside'
        if (row['Player'] == 'Irv Smith Jr.'):
            row['Player'] = 'Irv Smith'
        if (row['Player'] == 'Henry Ruggs'):
            row['Player'] = 'Henry Ruggs III'
        if (row['Player'] == 'AJ Dillon'):
            row['Player'] = 'A J Dillon' 
        if (row['Player'] == 'Laviska Shenault'):
            row['Player'] = 'Laviska Shenault Jr' 
        if (row['Player'] == 'Anthony McFarland'):
            row['Player'] = 'Anthony McFarland 2' 
        if (row['Player'] == 'KJ Hamler'):
            row['Player'] = 'K J Hamler' 
                        
        if (row['Player'] == 'Mike Williams' and year == '2013'):
            row['Player'] = 'Mike Williams 4'
        if (row['Player'] == 'Mike Williams' and row['Team'] == 'FA' and year == '2014'):
            row['Player'] = 'Mike Williams 4'
        return row['Player']


##############################################################################
# Creates path to NFL game stats for a given player in a given year
def format_nfl_stats_path(row, year):
    pname = name_exceptions(row, year)
    #removeSpecialChars = z.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
    temp = pname.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"})
    temp = temp.split(' ')
    pname='-'.join(temp)
    pname = pname.replace('--', '-')
    basePath = 'https://www.nfl.com/players/'
    statPath = '/stats/logs/'
    fullPath = basePath+pname+statPath+year
    
    return fullPath


##############################################################################
# Compare player to list of invalid players
def playerIsValid(row, year):
    if ((row['Player'] == 'Justin Blackmon' and not year == 2013) or \
        (row['Player'] == 'Ryan Williams') or \
        (row['Player'] == 'Tyler Gaffney') or \
        (row['Player'] == 'Derrius Guice') or \
        (row['Player'] == 'Damien Williams') or \
        (row['Player'] == 'Jalen Hurd' and year == 2020) or \
        (row['Player'] == 'Tyrell Williams' and year == 2020) or \
        (row['Player'] == 'Devin Funchess' and year == 2020) or \
        (row['Player'] == 'Thaddeus Moss' and year == 2020) or \
        (row['Player'] == 'Josh Oliver' and year == 2020) or \
        (row['Player'] == 'Rob Gronkowski' and year == 2019) or \
        (row['Player'] == 'Malcolm Mitchell')):
        
        return False
    else:
        return True
        
        


##############################################################################
# Formats data frame so that the output is consistent when written to CSV
# Need to reformat player data so all have same fields
        # WR and RB have rushing and receieing stats in opposite order
        # Fields should be as below:
        # Name, Position, Opponent
        # Pass Comp, Pass Att, Pass Yds, Pass Yds Avg, Pass TD, Int, 
        # Rush Att, Rush Yds, Rush Yds Avg, Rush TD, 
        # Rec, Rec Yds, Rec Avg, Rec TD
        # Fum Lost
        # Fantasy Pts
def format_output_data(player_info, stat_data):
    # Init frames
    weekly_data = pd.DataFrame(columns=weekly_stat_cols)
    temp_data = pd.DataFrame(columns=weekly_stat_cols)
    # Iterate through data for weekly data
    for idx, data in stat_data.iterrows():
        temp_data.loc[len(temp_data)]=0
        # Info Stats
        temp_data['Player']   = player_info['Player']
        temp_data['Pos']      = player_info['Pos']
        temp_data['Week']     = data['WK']
        temp_data['ADP']      = player_info['Avg Pick']
        temp_data['UID']      = player_info['UID']
        
        if not stat_data.empty:
            # QB Stats
            if (player_info['Pos'] == 'QB'):
                temp_data['Pass Comp']           = data['COMP']
                temp_data['Pass Att']            = data['ATT']
                temp_data['Pass Yds']            = data['YDS']
                temp_data['Pass Yds Avg']        = data['AVG']
                temp_data['Pass TD']             = data['TD']
                temp_data['Int']                 = data['INT']
                temp_data['Rush Att']            = data['ATT.1']
                temp_data['Rush Yds']            = data['YDS.1']
                temp_data['Rush Avg']            = data['AVG.1']
                temp_data['Rush TD']             = data['TD.1']
                temp_data['Fumbles Lost']        = data['LOST']
            
            # RB Stats
            if (player_info['Pos'] == 'RB'):
                temp_data['Rush Att']            = data['ATT']
                temp_data['Rush Yds']            = data['YDS']
                temp_data['Rush Avg']            = data['AVG']
                temp_data['Rush TD']             = data['TD']
                temp_data['Rec']                 = data['REC']
                temp_data['Rec Yds']             = data['YDS.1']
                temp_data['Rec Avg']             = data['AVG.1']
                temp_data['Rec TD']              = data['TD.1']
                temp_data['Fumbles Lost']        = data['LOST']
            
            # WR/TEW Stats
            if (player_info['Pos'] == 'WR' or player_info['Pos'] == 'TE'):
                temp_data['Rec']                 = data['REC']
                temp_data['Rec Yds']             = data['YDS']
                temp_data['Rec Avg']             = data['AVG']
                temp_data['Rec TD']              = data['TD']
                temp_data['Rush Att']            = data['ATT']
                temp_data['Rush Yds']            = data['YDS.1']
                temp_data['Rush Avg']            = data['AVG.1']
                temp_data['Rush TD']             = data['TD.1']
                temp_data['Fumbles Lost']        = data['LOST']
            
            temp_data = temp_data.fillna(0)
            # Fantasy Stats
            temp_data['Fantasy Points'] = calc_fantasy_pts(temp_data)
            
            weekly_data=weekly_data.append(temp_data)
            temp_data = temp_data.drop(0, axis=0)
        weekly_data = weekly_data.sort_values('Week')
        
    # Collect Annual Data
    annual_data = pd.DataFrame(columns=annual_stat_cols)
    annual_data.loc[len(annual_data)]=0
    
    # Info Stats
    annual_data['Player']   = player_info['Player']
    annual_data['Pos']      = player_info['Pos']
    annual_data['Games']     = len(weekly_data)
    annual_data['ADP']      = player_info['Avg Pick']
    annual_data['UID']      = player_info['UID']
    
    annual_data['Pass Comp']           = weekly_data['Pass Comp'].sum()
    annual_data['Pass Att']            = weekly_data['Pass Att'].sum() 
    annual_data['Pass Yds']            = weekly_data['Pass Yds'].sum()
    if annual_data['Pass Comp'][0] > 0:
        annual_data['Pass Yds Avg']        = annual_data['Pass Yds'][0] / annual_data['Pass Comp'][0]
    annual_data['Pass Yds Per Game']   = weekly_data['Pass Yds'].mean()
    annual_data['Pass TD']             = weekly_data['Pass TD'].sum()
    annual_data['Pass TD Per Game']    = weekly_data['Pass TD'].mean()
    annual_data['Int']                 = weekly_data['Int'].sum()      
    
    annual_data['Rush Att']            = weekly_data['Rush Att'].sum() 
    annual_data['Rush Yds']            = weekly_data['Rush Yds'].sum()
    annual_data['Rush Yds Per Game']   = weekly_data['Rush Yds'].mean()
    if annual_data['Rush Att'][0] > 0:
        annual_data['Rush Avg']            = annual_data['Rush Yds'][0] / annual_data['Rush Att'][0]
    annual_data['Rush TD']             = weekly_data['Rush TD'].sum()
    annual_data['Rush TD Per Game']    = weekly_data['Rush TD'].mean()
    
    annual_data['Rec']                 = weekly_data['Rec'].sum()
    annual_data['Rec Yds']             = weekly_data['Rec Yds'].sum()
    annual_data['Rec Yds Per Game']    = weekly_data['Rec Yds'].mean()
    if annual_data['Rec'][0] > 0:
        annual_data['Rec Avg']             = annual_data['Rec Yds'][0] / annual_data['Rec'][0]
    annual_data['Rec TD']              = weekly_data['Rec TD'].sum()
    annual_data['Rec TD Per Game']     = weekly_data['Rec TD'].mean()
    
    annual_data['Fumbles Lost']        = weekly_data['Fumbles Lost'].sum()
    
    annual_data['Fantasy Total']       = weekly_data['Fantasy Points'].sum()
    annual_data['Fantasy Avg']         = weekly_data['Fantasy Points'].mean()
        
    weekly_data = weekly_data.fillna(0)
    annual_data = annual_data.fillna(0)
    return weekly_data, annual_data

##############################################################################
# Calculates fantasy points earned
def calc_fantasy_pts(temp_data):
    temp =  (temp_data['Pass Yds'] / 25) + \
            (temp_data['Pass TD']) * 4 +    \
            (temp_data['Rush Yds'] + temp_data['Rec Yds']) * 0.10 + \
            (temp_data['Rush TD']+ temp_data['Rec TD'])    * 6 +  \
            (temp_data['Fumbles Lost'] + temp_data['Int']) * -2
    return temp

##############################################################################
# Get Data for player list and ADP of year

def scrapeADP(year, overwrite_enabled):
 # Load list of players for year 
        # Below goes back to 2013
        # or https://www71.myfantasyleague.com/2020/reports?R=ADP&POS=*&PERIOD=ALL&CUTOFF=5&FCOUNT=0&ROOKIES=0&INJURED=0&IS_PPR=1&IS_KEEPER=N&IS_MOCK=1&PAGE=ALL
        p='https://www71.myfantasyleague.com/' + str(year) + adp_url_opts
        df=pd.read_html(p, header=0)
        df = df[1]
        
        # Remove final index with irrelevant data (page number list)
        df=df.drop(index=len(df)-1)
        df=df.drop(columns=['Min Pick', 'Max Pick', '% Selected'])
        
        # Add columns for team and position
        df['Team']='na'
        df['Pos']='na'
        df['UID']='na'
        
        for idx, val in enumerate(df['Player']):
            df['Player'][idx], df['Pos'][idx], df['Team'][idx] = format_adp_name(val)
            df['UID'][idx] = df['Player'][idx].translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ '"})\
                + df['Rank'][idx]
        
        # Remove defenses and kickers from list of players
        df=df[df.Pos != 'PK']
        df=df[df.Pos != 'Def']
        
        # Write adp to file
        adp_file_name = 'Stats/ADP_' + str(year) + '.csv'
        
        if overwrite_enabled:
            df.to_csv(adp_file_name, sep=',', header=True, index=False)
        return df

##############################################################################
def scrapePlayerStats(year, player_frame, writeHeader, weekly_outfile, annual_outfile, overwrite_enabled):
    # Initialize dataframe for weekly stats output
    weekly_stat_df=pd.DataFrame(columns=weekly_stat_cols)
    weekly_stat_df.loc[len(weekly_stat_df)]=0
    
    # Initialize dataframe for annual stats output
    annual_stat_df=pd.DataFrame(columns=annual_stat_cols)
    annual_stat_df.loc[len(annual_stat_df)]=0
    
    # Try parallel processing to speed up
    #num_cores = multiprocessing.cpu_count()
    #processed_list = Parallel(n_jobs=num_cores)(delayed(my_function(i ,parameters) for i in inputs)
                                                
    # Iterate over each player
    for idx, row in player_frame.iterrows():
        stats = pd.DataFrame()
        
        fullPath = format_nfl_stats_path(row, str(year))
        print(str(idx) + ' ' + row['Player'] + ' of ' + str(len(player_frame)) + ' players \n\t--> ' + fullPath)
        
        # To load player data
        
        if playerIsValid(row, year):
            stats = pd.read_html(fullPath, header=0)
        
            # Determine if stats from Pre/Reg/Post Season games
            # We only want regular season games
            r = requests.get(fullPath)
            
            # Check web page for flags, only want regular season data
            found = []
            found.append(re.search('Preseason', r.text))
            found.append(re.search('Regular Season', r.text))
            found.append(re.search('Post Season', r.text))
            
            # Little bit of backflips for parsing web page
            if found[1] is not None:
                if found[0] is None:
                    format_idx = 0
                else:
                    format_idx = 1
            else:
                format_idx = -1
        
            # We now have regular season data for this player in this year    
            regSeason = stats[format_idx]
            
        # Reformat player data so all have same fields
        weekly_stat_df, annual_stat_df = format_output_data(row, regSeason)
        
        # Write data to csv files with header
        if overwrite_enabled:
            # Weekly
            weekly_stat_df.to_csv(weekly_outfile, mode='a', header=writeHeader)
            # Annual
            annual_stat_df.to_csv(annual_outfile, mode='a', header=writeHeader)
        
            # If header written to file, dont do it again
            if writeHeader:
                writeHeader = False
                
                
##############################################################################
def get_positional_breakdown(stats_annual, sortBy, order=False):        
    qb_annual = stats_annual[stats_annual['Pos']=='QB'].sort_values(sortBy, ascending=order)
    qb_annual = qb_annual.reset_index()
    rb_annual = stats_annual[stats_annual['Pos']=='RB'].sort_values(sortBy, ascending=order)
    rb_annual = rb_annual.reset_index()
    wr_annual = stats_annual[stats_annual['Pos']=='WR'].sort_values(sortBy, ascending=order)
    wr_annual = wr_annual.reset_index()
    te_annual = stats_annual[stats_annual['Pos']=='TE'].sort_values(sortBy, ascending=order)
    te_annual = te_annual.reset_index()
    
    # Deliniate position draft teirs
    # QB
    qb1 = qb_annual[0:12]
    qb2 = qb_annual[13:24]
    if len(qb_annual) > 24:
        qb3 = qb_annual[25:]
    
    # RB
    rb1 = rb_annual[0:12]
    rb2 = rb_annual[13:24]
    rb3 = rb_annual[25:36]
    rb4 = rb_annual[37:48]
    
    # WR
    wr1 = wr_annual[0:12]
    wr2 = wr_annual[13:24]
    wr3 = wr_annual[25:36]
    wr4 = wr_annual[37:48]
    
    # TE
    te1 = te_annual[0:12]
    te2 = te_annual[13:24]
    if len(te_annual) > 24:
        te3 = te_annual[25:]
        
    # Flex
    flex = pd.concat([rb3[0:6], wr3[0:6]]).sort_values(sortBy, ascending=False)
    
    return qb_annual, rb_annual, wr_annual, te_annual, qb1, qb2, qb3, rb1, rb2, rb3, rb4, wr1, wr2, wr3, wr4, te1, te2, te3, flex