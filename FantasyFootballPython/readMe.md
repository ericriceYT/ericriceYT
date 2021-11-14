# Fantasy Football Python
This project scrapes fantasy football player data from multiple sources to assemble stats databases as spreadsheets.
The original intent of this project was to determine the most valuable position in fantasy football statistically. To this end, an advanced metric Wins Above Replacement (WAR) is used. Fantasy Football WAR is based on the same metric in Baseball: if a player is on a team is replaced by a "replacement level" player (aka average), how much does this hurt their team? The full explanation can be found in the paper "Analyzing the Conventional Wisdom of the Two-RB Draft Strategy in Fantasy Football Using Wins Above Replacement"

# Using the script
main_analyzeData.py is the main python script to pull in fantasy data football from internet and convert to spreadsheets. 
If spreadsheets exist, the script will load spreadsheets instead. Scraping data takes 2-3 hrs, loading spreadsheets takes a few seconds.

# The spreadsheets:
These spreadsheets have player data for all fantasy-football relevant players between 2013-2020.
Player data for each week is available as well as season totals.
Data Sources:
  Average Draft Position (ADP): MyFantasyLeague.com
  Player Statistics: NFL.com
  
# Other Papers to Read:
  Stathole, Jeff. “Fantasy Football Wins Above Replacement: The Theory.” Dynasty Nerds. March 18, 2020. Accessed July 08, 2021.
https://www.dynastynerds.com/fantasy-football-wins-above-replacement-the-theory/
  Henderson, Jeff. “Fantasy WAR Part 1: Theory.” Fantasy Points. Accessed July 08, 2021.
https://www.fantasypoints.com/nfl/articles/season/2021/fantasy-war-part-1-theory
  Morgan, Christopher D.; Rodriguez, Caroll; MacVittie, Korey; Slater, Robert; and Engels, Daniel W. (2019) "Identifying Undervalued Players in
Fantasy Football," SMU Data Science Review: Vol. 2 : No. 2 , Article 14. https://scholar.smu.edu/datasciencereview/vol2/iss2/14
  Steenkiste, P. “Finding the Optimal Fantasy Football Team.” December 11, 2015
  Florio, M. “Forget Zero RB, Grab Two RBs ASAP.” RotoBaller. Accessed July 08, 2021. https://www.rotoballer.com/fantasy-draft-strategy-startingwith-two-rbs/739016


