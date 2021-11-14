# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 17:32:41 2021

@author: ericr
"""
##############################################################################
# Constants
weekly_stat_cols = ['Player', 'Pos', 'Week', 'ADP',
    'Pass Comp', 'Pass Att', 'Pass Yds', 'Pass Yds Avg', 'Pass TD', 'Int',
    'Rush Att', 'Rush Yds', 'Rush Avg', 'Rush TD',
    'Rec', 'Rec Yds', 'Rec Avg', 'Rec TD', 
    'Fumbles Lost', 
    'Fantasy Points', 'UID']


annual_stat_cols = ['Player', 'Pos', 'Games', 'ADP',
    'Pass Comp', 'Pass Att', 'Pass Yds', 'Pass Yds Per Game', 'Pass Yds Avg', 'Pass TD', 'Pass TD Per Game', 'Int',
    'Rush Att', 'Rush Yds', 'Rush Yds Per Game', 'Rush Yds Avg', 'Rush TD', 'Rush TD Per Game',
    'Rec', 'Rec Yds', 'Rec Yds Per Game', 'Rec Yds Avg', 'Rec TD', 'Rec TD Per Game', 
    'Fumbles Lost', 
    'Fantasy Total', 'Fantasy Avg', 'UID']

adp_url_opts = '/reports?R=ADP&POS=Coach+QB+TMQB+TMRB+RB+FB+WR+TMWR+TE+TMTE+WR+TE+RB+WR+TE+KR+PK+TMPK+PN+TMPN+Def+ST+Off&PERIOD=ALL&CUTOFF=5&FCOUNT=0&ROOKIES=0&INJURED=0&IS_PPR=3&IS_KEEPER=N&IS_MOCK=1&PAGE=ALL'

##############################################################################