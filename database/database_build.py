# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:28:54 2022

@author: Jacqueline Kelly
"""
import sys
from readurl import *

# Get full list of ncaa team ids
team_ids = get_team_id("https://stats.ncaa.org/selection_rankings/nitty_gritties/27163")
# Get full list of urls to each team page
urls = get_url_from_id(team_ids)
# Extract all the strings on each team's page
team_pages = get_team_page(urls)
# Build a dictionary that maps ncaa ids to team names
dict_team_names = get_team_names(team_ids, True, True, **team_pages)
# Get all of the stats present on each team's page
all_team_stats = get_team_page(urls, strings=False)
# This is a 'training' team from which the names for statitsics are extracted
stats = get_team_page("https://stats.ncaa.org/teams/525692", strings=False)

## Using a sample team for extracting all the possible team stats reported. 
## Some teams do not have all of these stats listed on their page.Team '525683'
## has all statistic categories.
index_col = []
for i in range(1,19):
    index_col.append(i*3+1)

columns = [all_team_stats['525683'][i] for i in index_col]
dictionary = dict()

## Building a nested dictionary of team stats. Outer key is ncaa team id,
## and value is a dictionary that maps the statistic category (inner keys) to 
## statistic value (inner value)
for team in all_team_stats:
    dictionary[team] = dict()
    for stat in range(len(columns)):
        if columns[stat] in all_team_stats[team]:
            dictionary[team][columns[stat]] = all_team_stats[team][all_team_stats[team].index(columns[stat])+2]
        else: 
            dictionary[team][columns[stat]] = np.nan
            
        
season_df = pd.DataFrame.from_dict(dictionary, orient='index')

season_df['team_name'] = pd.Series(dict_team_names)




