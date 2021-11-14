# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 19:30:33 2021

@author: ericr
"""
from LoadPlayerStats import *
import matplotlib.pyplot as plt
import numpy as np
from  math import *
from scipy.stats import gaussian_kde
import scipy.stats
##############################################################################
# Use flag to enable/disble plot display
show_plots = True

# Years to analyze
years = [ii for ii in range(2017, 2020+1)]

# Load in player stats
weekly_combined, annual_combined = getStats(years)


##############################################################################
# Need to get averages for each week. Take top players from positions for year
#  and average/STD their scores. This will determine average score and deviation for WAR.
# NOTE: For Kickers/DST use average = 10.0pts/game, std=3.0pts/game
k_avg = 10.0
k_std = 3.5
dst_avg = 12.0
dst_std = 6.0

cntr=1


##############################################################################
for year in years:
    print("*"*80 + "\nYear: " + str(year))
    stats_week      = weekly_combined[weekly_combined['Year'] == year]
    stats_annual    = annual_combined[annual_combined['Year'] == year]
    
    qb_annual, rb_annual, wr_annual, te_annual, qb1, qb2, qb3, rb1, rb2, rb3, rb4, wr1, wr2, wr3, wr4, te1, te2, te3, flex = get_positional_breakdown(stats_annual, 'Fantasy Total')
    qb_replacement_value = np.mean(qb_annual[12:18]['Fantasy Total']/16)
    rb_replacement_value = np.mean(rb_annual[25:31]['Fantasy Total']/16)
    wr_replacement_value = np.mean(wr_annual[25:31]['Fantasy Total']/16)
    te_replacement_value = np.mean(te_annual[12:18]['Fantasy Total']/16)
    
    
    # Fantasy Team Average and Standard Deviation
    team_pos_avg = np.array([(qb1['Fantasy Total'].mean()/16),\
                (rb1['Fantasy Total']/16).mean(), (rb2['Fantasy Total']/16).mean(), \
                (wr1['Fantasy Total']/16).mean(), (wr2['Fantasy Total']/16).mean(),\
                (te1['Fantasy Total']/16).mean(), (flex['Fantasy Total']/16).mean(), \
                k_avg, dst_avg])
        
    team_pos_std = np.array([(qb1['Fantasy Total']/16).std(),\
                (rb1['Fantasy Total']/16).std(), (rb2['Fantasy Total']/16).std(), \
                (wr1['Fantasy Total']/16).std(), (wr2['Fantasy Total']/16).std(),\
                (te1['Fantasy Total']/16).std(), (flex['Fantasy Total']/16).std(), \
                k_std, dst_std])
    
    
    # Formula for standard deviaton of team (sum of variances)
    team_tot_avg = team_pos_avg.sum()
    team_tot_std = np.sqrt((team_pos_std**2).sum())
    
    # Maps position strings to values in starter/replacement
    pos_map = { 'QB': 0, 'RB': 1, 'WR' : 2, 'TE':3}
    starter_values = np.array(((qb1['Fantasy Total']/16).mean(), (rb1['Fantasy Total']/16).mean(), (wr1['Fantasy Total']/16).mean(), (te1['Fantasy Total']/16).mean()))
    replacement_values = np.array((qb_replacement_value, rb_replacement_value, wr_replacement_value, te_replacement_value))
    temp = -(replacement_values-starter_values)/team_tot_std
    replacement_wins = scipy.stats.norm.sf(temp)
    
    
##############################################################################
    # Need to get WAR for each player for each week, add to file and save it
    # For weekly
    player_wars = np.array([])
    
    # For annual
    cur_player = stats_annual['Player'][0]
    player_cntr = 0
    total_wars = np.array([])
    cum_wars = 0
    
    for idx, row in stats_week.iterrows():
        player = row['Player']
        if not(cur_player == player):
            total_wars = np.append(total_wars, cum_wars)
            #print('\t\t total war: ' + str(cum_wars))
            cum_wars = 0
            player_cntr +=1
            cur_player = player
        week = row['Week']
        pos = row['Pos']
        # Get WAR
        score = np.clip(scipy.stats.norm.sf(-(row['Fantasy Points']-starter_values[pos_map[pos]])/team_tot_std)-replacement_wins[pos_map[pos]], -1.0, 1.0)
        # add to list
        player_wars = np.append(player_wars, score)
        cum_wars += score
        #print(player + '\t wk: ' + str(week) + '\t scr: ' + str(score) + '\t cum: ' + str(cum_wars))
        
    total_wars = np.append(total_wars, cum_wars)
    stats_week['WAR'] = player_wars.tolist()
    stats_annual['WAR'] = total_wars.tolist()
    
    # Reset stats so that WAR is included
    qb_annual, rb_annual, wr_annual, te_annual, qb1, qb2, qb3, rb1, rb2, rb3, rb4, wr1, wr2, wr3, wr4, te1, te2, te3, flex = get_positional_breakdown(stats_annual, 'Fantasy Total')
    
    replacement_team_wins_per_year = scipy.stats.norm.sf(-sum(replacement_values - starter_values)/team_tot_std)*16
##############################################################################
    print("Pos Avg:" + str(team_pos_avg))
    print("\nPos Starter Values: " + str(starter_values))
    print("\nPos Replacement Values: " + str(replacement_values))
    print("\nWins by Replacement Team per Year: " + str(replacement_team_wins_per_year))
    print("\nWins by Replacement Players: " + str(replacement_wins))
    
    print("\nTeam AVG: " + str(team_tot_avg))
    print("Team STD: " + str(team_tot_std))
    
    print("\n")
    
    if show_plots:
##############################################################################
            # Plotting
            figSize = (5,4)
            
            labs = ['QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'FLEX','K', 'DST']
            colors = ['blue', 'orange', 'orange', 'green', 'green', 'red', 'magenta', 'grey', 'grey']
            fig0 = plt.figure(num=999, figsize=(11,5))
            ax0 = fig0.add_subplot(111)
            
            bot=0
            for idx, dat in enumerate(team_pos_avg):
                if idx > 0:
                    bot+= team_pos_avg[idx-1]
                ax0.bar(year, dat, 0.5, label=labs[idx], bottom=bot, color=colors[idx], edgecolor='white', alpha=0.8)
                if idx < 6:
                    repl = replacement_values[pos_map[labs[idx]]]
                    ax0.bar(year+0.33, repl, 0.125, label=labs[idx], bottom=bot, color=colors[idx], edgecolor='white', alpha=0.5)
                    plt.annotate(str(f"{repl:.1f}"), xytext=(year+.29, bot+repl-3), xy=(year+0.29, bot+repl-3), color='white', fontsize=7)
                    
                plt.annotate(str(f"{dat:.1f}"), xytext=(year-.22, bot+dat-4), xy=(year-.22, bot+dat-4), color='white', fontsize=7)
            plt.annotate(str(f"{sum(team_pos_avg):.1f}"), xytext=(year-.22, sum(team_pos_avg)), xy=(year-.22, sum(team_pos_avg)+4), color='black', fontsize=8, fontweight='bold')
            ax0.set_ylabel('Average Team Score')
            ax0.set_title('Average Weekly Team Scores', fontweight='bold')
            ax0.legend(labs, bbox_to_anchor=(1.1,1), fontsize='small')
            ax0.spines['top'].set_visible(False)
            ax0.spines['right'].set_visible(False)
            ax0.spines['left'].set_visible(False)
            ax0.set_ylabel('')
            ax0.set_yticklabels('')
            ax0.set_xticks(range(2017, 2020+1))
            ax0.set_axis_on()
            
            
            
            fig=plt.figure(num=cntr, figsize=figSize)
            ax=fig.add_subplot(111)
            bp = ax.boxplot([qb1['Fantasy Total']/16, rb1['Fantasy Total']/16, rb2['Fantasy Total']/16, wr1['Fantasy Total']/16, wr2['Fantasy Total']/16, te1['Fantasy Total']/16, flex['Fantasy Total']/16], widths=0.33)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.title('Average Pts per Week for Starting Team - ' + str(year), fontsize=12)
            ax.set_xticklabels(['QB1', 'RB1', 'RB2', 'WR1', 'WR2', 'TE1', 'FLEX'])
            ax.set_ylim(bottom=0, top=30)
            plt.ylabel('Average Points Per Week')
            fig.show()
            
            # ADP Box Plots per starting position
            fig_adp_box=plt.figure(num=cntr+100, figsize=figSize)
            ax=fig_adp_box.add_subplot(111)
            bp = ax.boxplot([qb1['ADP'], rb1['ADP'], rb2['ADP'], wr1['ADP'], wr2['ADP'], te1['ADP'], flex['ADP']], widths=0.33)
            
            plt.title('Average Draft Position for Starting Team - ' + str(year), fontsize=12)
            ax.set_xticklabels(['QB1', 'RB1', 'RB2', 'WR1', 'WR2', 'TE1', 'FLEX'])
            plt.ylabel('Average Draft Position')
            ax.set_ylim(bottom=0, top=250)
            fig_adp_box.show()
            
            # Histogram for position
            """
            fig2 = plt.figure(num=cntr+10, figsize=figSize)
            ax2=fig.add_subplot(111)
            
            plt.hist(rb4['Fantasy Total']/16, bins=range(int(floor(min(rb4['Fantasy Total']/16))), int(ceil(max(rb4['Fantasy Total']/16))) + 1, 1), facecolor='green',  alpha=0.2, edgecolor='green')
            plt.hist(rb3['Fantasy Total']/16, bins=range(int(floor(min(rb3['Fantasy Total']/16))), int(ceil(max(rb3['Fantasy Total']/16))) + 1, 1), facecolor='red',    alpha=0.3, edgecolor='red')
            plt.hist(rb2['Fantasy Total']/16, bins=range(int(floor(min(rb2['Fantasy Total']/16))), int(ceil(max(rb2['Fantasy Total']/16))) + 1, 1), facecolor='orange', alpha=0.4, edgecolor='orange')
            plt.hist(rb1['Fantasy Total']/16, bins=range(int(floor(min(rb1['Fantasy Total']/16))), int(ceil(max(rb1['Fantasy Total']/16))) + 1, 1), facecolor='blue',   alpha=0.5, edgecolor='blue')
            plt.xlim([0, 30])
            
            plt.xlabel('Average Points per Week')
            plt.ylabel('Player Counts')
            plt.title('RB Average Pts per Week - ' + str(year), fontsize=12)
            fig2.show()
            
            
            # For density function
            if False:
                data = np.concatenate((rb1['Fantasy Total']/16, rb2['Fantasy Total']/16, rb3['Fantasy Total']/16, rb4['Fantasy Total']/16))
                density = gaussian_kde(data)
                xs = linspace(min(data), max(data), 100)
                density.covariance_factor = lambda : 0.25
                density._compute_covariance()
                plt.plot(xs, density(xs), color='black')
            """
                
            # Scatter plots
            fig3 = plt.figure(num=cntr+20, figsize=figSize)
            
            plt.scatter(rb_annual['ADP'], rb_annual['Fantasy Total']/16, color='blue', s=30)
            plt.scatter(wr_annual['ADP'], wr_annual['Fantasy Total']/16, color='orange', s=30)
            plt.scatter(qb_annual['ADP'], qb_annual['Fantasy Total']/16, color='grey', alpha=0.65, s=15)
            plt.scatter(te_annual['ADP'], te_annual['Fantasy Total']/16, color='gray', alpha=0.25, s=15)
            plt.legend(['RB', 'WR', 'QB', 'TE'], fontsize='x-small')
            plt.ylabel('Average Points per Week')
            plt.xlabel('Average Draft Position')    
            plt.xlim([0, 250])
            plt.ylim([0, 30])
            plt.title('Average Pts per Week vs ADP - ' + str(year), fontsize=12)
            
            
            # Pts per week vs position rank
            fig4 = plt.figure(num=cntr+30, figsize=figSize)
            
            plt.title('Average Pts per Week vs Position Ranking - ' + str(year), fontsize=12)
            plt.scatter(qb_annual.index, qb_annual['Fantasy Total']/16, s=20)
            plt.scatter(rb_annual.index, rb_annual['Fantasy Total']/16, s=20)
            plt.scatter(wr_annual.index, wr_annual['Fantasy Total']/16, s=20)
            plt.scatter(te_annual.index, te_annual['Fantasy Total']/16, s=20)
            plt.legend(['QB', 'RB', 'WR', 'TE'], fontsize='x-small')
            plt.xlabel('Positon Ranking')
            plt.ylabel('Average Points per Week')  
            plt.ylim(0, 30)
            plt.xlim([0, 50])
            plt.plot([12, 12], [0, 30], color='grey', alpha=0.5)
            plt.plot([24, 24], [0, 30], color='grey', alpha=0.5)
            plt.plot([36, 36], [0, 30], color='grey', alpha=0.5)
            
            # ADP vs adp
            # RB
            fig5 = plt.figure(num=cntr+50, figsize=figSize)
            # Lines separating RB/WR expected, sleepers, busts
            if True:
                plt.plot([0, 50], [60, 60], color='grey')
                plt.plot([20, 20], [0, 200], color='grey')
                plt.annotate('Sleeper', xytext=(1, 200-10), xy=(1, 200-10), color='green')
                plt.annotate('Bust', xytext=(50-4, 0+4), xy=(50-4, 0), color='red')
            
            
            plt.title('Average Draft Position vs RB Ranking - ' + str(year), fontsize=12)
            #plt.scatter(qb_annual.index, qb_annual['ADP'])
            h_rb = plt.scatter(rb_annual.index, rb_annual['ADP'], color='orange', alpha=0.75, s=20)
            #plt.scatter(wr_annual.index, wr_annual['ADP'])
            #plt.scatter(te_annual.index, te_annual['ADP'])
            #plt.legend(['QB', 'RB', 'WR', 'TE'])
            plt.xlabel('RB Ranking')
            plt.ylabel('Average Draft Position')  
            plt.ylim(0, 200)
            plt.xlim([0, 50])
            
                
            #fig6 = plt.figure(num=cntr+60, figsize=figSize)
            
            # Lines separating RB/WR expected, sleepers, busts
            if False:
                plt.plot([0, 50], [60, 60], color='grey')
                plt.plot([20, 20], [0, 200], color='grey')
                plt.annotate('Sleeper', xytext=(1, 200-10), xy=(1, 200-10))
                plt.annotate('Bust', xytext=(50-4, 0+4), xy=(50-4, 0))
            
            plt.title('Average Draft Position vs RB/WR Ranking - ' + str(year), fontsize=12)
            h_wr = plt.scatter(wr_annual.index, wr_annual['ADP'], color='green', alpha=0.75, s=20)
            plt.xlabel('RB/WR Ranking')
            plt.ylabel('Average Draft Position')  
            plt.ylim(0, 200)
            plt.xlim([0, 50])
            plt.legend((h_rb, h_wr), ('RB', 'WR'), loc=6, fontsize='x-small')
            
            
            # Pts per week vs position rank
            fig7 = plt.figure(num=cntr+200, figsize=figSize)
            
            plt.title('WAR vs Position Ranking - ' + str(year), fontsize=12)
            plt.scatter(qb_annual.index, qb_annual['WAR'])
            plt.scatter(rb_annual.index, rb_annual['WAR'])
            plt.scatter(wr_annual.index, wr_annual['WAR'])
            plt.scatter(te_annual.index, te_annual['WAR'])
            plt.legend(['QB', 'RB', 'WR', 'TE'])
            plt.xlabel('Positon Ranking')
            plt.ylabel('WAR')  
            plt.ylim(-5, 10)
            plt.xlim([0, 50])
            plt.plot([12, 12], [-5, 30], color='grey', alpha=0.5)
            plt.plot([24, 24], [-5, 30], color='grey', alpha=0.5)
            plt.plot([36, 36], [-5, 30], color='grey', alpha=0.5)
            
            
            
            # WAR Box Plots per starting position
            fig_war_box=plt.figure(num=cntr+110, figsize=figSize)
            ax=fig_war_box.add_subplot(111)
            bp = ax.boxplot([qb1['WAR'], rb1['WAR'], rb2['WAR'], wr1['WAR'], wr2['WAR'], te1['WAR'], flex['WAR']], widths=0.33)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.title('WAR for Top Starting Positions - ' + str(year), fontsize=12)
            ax.set_xticklabels(['QB1', 'RB1', 'RB2', 'WR1', 'WR2', 'TE1', 'FLEX'])
            plt.ylabel('WAR')
            ax.set_ylim(bottom=-5, top=10)
            fig_adp_box.show()
            
            
            # WAR Box Plots per ADP
            qb_annual, rb_annual, wr_annual, te_annual, qb1, qb2, qb3, rb1, rb2, rb3, rb4, wr1, wr2, wr3, wr4, te1, te2, te3, flex = get_positional_breakdown(stats_annual, 'ADP', True)
            fig_war_box=plt.figure(num=cntr+1100, figsize=figSize)
            ax=fig_war_box.add_subplot(111)
            bp = ax.boxplot([qb1['WAR'], rb1['WAR'], rb2['WAR'], wr1['WAR'], wr2['WAR'], te1['WAR'], flex['WAR']], widths=0.33)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.title('WAR for Top Drafted Players - ' + str(year), fontsize=12)
            ax.set_xticklabels(['QB1', 'RB1', 'RB2', 'WR1', 'WR2', 'TE1', 'FLEX'])
            plt.ylabel('WAR')
            ax.set_ylim(bottom=-5, top=10)
            fig_adp_box.show()
            
            
            # Pts per week vs position rank - qb, rb, wr, te
            alpha = 1-(2021-year)/5
            # QB
            fig8 = plt.figure(num=301, figsize=figSize)
            plt.title('WAR vs Position Draft Ranking - QB', fontsize=12)
            plt.scatter(qb_annual.index, qb_annual['WAR'], color='blue', alpha=alpha)
            plt.xlabel('Draft Positon Ranking')
            plt.ylabel('WAR')  
            plt.ylim(-5, 10)
            plt.xlim([0, 36])
            plt.plot([12, 12], [-5, 10], color='grey', alpha=0.25)
            plt.plot([24, 24], [-5, 10], color='grey', alpha=0.25)
            plt.xticks([0, 6, 12, 18, 24, 30, 36])
            
            # RB
            fig9 = plt.figure(num=302, figsize=figSize)
            plt.title('WAR vs Position Draft Ranking - RB', fontsize=12)
            plt.scatter(rb_annual.index, rb_annual['WAR'], color='orange', alpha=alpha)
            plt.xlabel('Draft Positon Ranking')
            plt.ylabel('WAR')  
            plt.ylim(-5, 10)
            plt.xlim([0, 36])
            plt.plot([12, 12], [-5, 10], color='grey', alpha=0.25)
            plt.plot([24, 24], [-5, 10], color='grey', alpha=0.25)
            plt.xticks([0, 6, 12, 18, 24, 30, 36])
            
            # WR
            fig10 = plt.figure(num=303, figsize=figSize)
            plt.title('WAR vs Position Draft Ranking - WR', fontsize=12)
            plt.scatter(wr_annual.index, wr_annual['WAR'], color='green', alpha=alpha)
            plt.xlabel('Draft Positon Ranking')
            plt.ylabel('WAR')  
            plt.ylim(-5, 10)
            plt.xlim([0, 36])
            plt.plot([12, 12], [-5, 10], color='grey', alpha=0.25)
            plt.plot([24, 24], [-5, 10], color='grey', alpha=0.25)
            plt.xticks([0, 6, 12, 18, 24, 30, 36])
            
            # TE
            fig11 = plt.figure(num=304, figsize=figSize)
            plt.title('WAR vs Position Draft Ranking - TE', fontsize=12)
            plt.scatter(te_annual.index, te_annual['WAR'], color='red', alpha=alpha)
            plt.xlabel('Draft Positon Ranking')
            plt.ylabel('WAR')  
            plt.ylim(-5, 10)
            plt.xlim([0, 36])
            plt.plot([12, 12], [-5, 10], color='grey', alpha=0.25)
            plt.plot([24, 24], [-5, 10], color='grey', alpha=0.25)
            plt.xticks([0, 6, 12, 18, 24, 30, 36])
            
            # Sort by WAR
            qb_annual, rb_annual, wr_annual, te_annual, qb1, qb2, qb3, rb1, rb2, rb3, rb4, wr1, wr2, wr3, wr4, te1, te2, te3, flex = get_positional_breakdown(stats_annual, 'WAR', False)
        
            # QB
            fig12 = plt.figure(num=305, figsize=figSize)
            plt.title('ADP VS WAR Position Rank - QB', fontsize=12)
            plt.scatter(qb_annual.index, qb_annual['ADP'], color='blue', alpha=alpha)
            plt.xlabel('WAR')
            plt.ylabel('ADP')  
            plt.ylim(0, 250)
            plt.xlim([0, 36])
            #plt.plot([12, 12], [0, 150], color='grey', alpha=0.25)
            #plt.plot([24, 24], [0, 150], color='grey', alpha=0.25)
            plt.xticks([0, 6, 12, 18, 24, 30, 36])
            # Lines separating RB/WR expected, sleepers, busts
            if True:
                plt.plot([0, 36], [60, 60], color='grey')
                plt.plot([20, 20], [0, 250], color='grey')
                plt.annotate('Sleeper', xytext=(1, 250-10), xy=(1, 250-10), color='green')
                plt.annotate('Bust', xytext=(36-4, 0+4), xy=(36-4, 0), color='red')
            
            
            # RB
            fig9 = plt.figure(num=306, figsize=figSize)
            plt.title('ADP VS WAR Position Rank - RB', fontsize=12)
            plt.scatter(rb_annual.index, rb_annual['ADP'], color='orange', alpha=alpha)
            plt.xlabel('WAR Position Ranking')
            plt.ylabel('ADP')  
            plt.ylim(0, 250)
            plt.xlim([0, 36])
            #plt.plot([12, 12], [0, 150], color='grey', alpha=0.25)
            #plt.plot([24, 24], [0, 150], color='grey', alpha=0.25)
            plt.xticks([0, 6, 12, 18, 24, 30, 36])
            if True:
                plt.plot([0, 36], [60, 60], color='grey')
                plt.plot([20, 20], [0, 250], color='grey')
                plt.annotate('Sleeper', xytext=(1, 250-10), xy=(1, 250-10), color='green')
                plt.annotate('Bust', xytext=(36-4, 0+4), xy=(36-4, 0), color='red')
            
            # WR
            fig10 = plt.figure(num=307, figsize=figSize)
            plt.title('ADP VS WAR Position Rank - WR', fontsize=12)
            plt.scatter(wr_annual.index, wr_annual['ADP'], color='green', alpha=alpha)
            plt.xlabel('WAR Position Ranking')
            plt.ylabel('ADP')  
            plt.ylim(0, 250)
            plt.xlim([0, 36])
            #plt.plot([12, 12], [0, 250], color='grey', alpha=0.25)
            #plt.plot([24, 24], [0, 250], color='grey', alpha=0.25)
            plt.xticks([0, 6, 12, 18, 24, 30, 36])
            if True:
                plt.plot([0, 36], [60, 60], color='grey')
                plt.plot([20, 20], [0, 250], color='grey')
                plt.annotate('Sleeper', xytext=(1, 250-10), xy=(1, 250-10), color='green')
                plt.annotate('Bust', xytext=(36-4, 0+4), xy=(36-4, 0), color='red')
            
            # TE
            fig11 = plt.figure(num=308, figsize=figSize)
            plt.title('ADP VS WAR Position Rank - TE', fontsize=12)
            plt.scatter(te_annual.index, te_annual['ADP'], color='red', alpha=alpha)
            plt.xlabel('WAR Position Ranking')
            plt.ylabel('ADP')  
            plt.ylim(0, 250)
            plt.xlim([0, 36])
            #plt.plot([12, 12], [0, 250], color='grey', alpha=0.25)
            #plt.plot([24, 24], [0, 250], color='grey', alpha=0.25)
            plt.xticks([0, 6, 12, 18, 24, 30, 36])
            if True:
                plt.plot([0, 36], [60, 60], color='grey')
                plt.plot([20, 20], [0, 250], color='grey')
                plt.annotate('Sleeper', xytext=(1, 250-10), xy=(1, 250-10), color='green')
                plt.annotate('Bust', xytext=(36-4, 0+4), xy=(36-4, 0), color='red')
            
            cntr+=1