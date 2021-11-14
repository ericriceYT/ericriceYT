# Fantasy Football Python
This project scrapes fantasy football player data from multiple sources to assemble stats databases as spreadsheets.
The original intent of this project was to determine the most valuable position in fantasy football statistically. To this end, an advanced metric Wins Above Replacement (WAR) is used. Fantasy Football WAR is based on the same metric in Baseball: if a player is on a team is replaced by a "replacement level" player (aka average), how much does this hurt their team? The full explanation can be found in the paper "Analyzing the Conventional Wisdom of the Two-RB Draft Strategy in Fantasy Football Using Wins Above Replacement"

# Using the script
main_analyzeData.py is the main python script to pull in fantasy data football from internet and convert to spreadsheets. 
If spreadsheets exist, the script will load spreadsheets instead. Scraping data takes 2-3 hrs, loading spreadsheets takes a few seconds.
