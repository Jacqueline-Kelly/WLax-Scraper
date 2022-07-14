# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 23:47:01 2022

@author: Jacqueline Kelly

Functions for scraping webpages and obtaining & processing data.
"""

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import pandas as pd

def get_team_id(url="https://stats.ncaa.org/selection_rankings/nitty_gritties/27163", hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}):
    '''
    Obtain the ncaa id for each team from a page containing links to team. 
    Default url is the season stats page, which provides links to each team's page.
    The id is a unique identifier for each team and is a six digit number.
    The URL to each team site can be constructed solely from the team id.

    Parameters
    ----------
    url : str
        URL to page which contains links to all ncaa teams. Default link is the 
        season stats page.
    hdr : dict DEFAULT dictionary 
        Provides access to webpage.

    Returns
    -------
    team_ids_list : list
        Returns a list of all the team ids of teams referenced on the page 
        rendered from the input url.

    '''
    soup = get_soup(url, hdr)

    links = soup.findAll('a')
    finalLinks = list()
    for link in links:
        finalLinks.append(link.attrs['href'])
    
    #parsing based off the method ncaa creates links to team pages. Final value
    #is the team's id.
    team_ids_list = [team.removeprefix('/teams/') for team in finalLinks if ('/teams/' in team) & ('/team_sheet' not in team)]
     
    return team_ids_list


def get_soup(url, hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}):

        '''
        Obtain the response from the BeautifulSoup library which parses the 
        webpage into html, which can in turn be processed for python to read. 
        
        Parameters
        ----------
        url: str or list 
            A valid website link as a string or a list of valid website strings
            
        hdr: dict
           Submitted to the requests function to permit access to websites that
           may restrict traffic from the python requests library
        Returns
        -------
        soup: BeautifulSoup response 
            If a single url as string is provided in input 
        
        soup_list: list of BeautifulSoup responses
            If a list of url is provided in input
        
        '''
        if isinstance(url, str):
            html = requests.get(url, headers=hdr).content
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        
        elif isinstance(url, list):
            html_list = [requests.get(u, headers=hdr).content for u in url]
            soup_list = [BeautifulSoup(html_list[page], 'html.parser') for page in html_list]
            return soup_list
            
        else:
            raise Exception('''Data type error. You must either provide a valid website
                            link as a string or a list of valid website strings''')
        
        return
        
    

def get_team_page(url, strings=True):
    '''
    Obtain the stats from a team page.
    
    Parameters
    ----------
    soup : str or list
        Enter the url as a string or enter list of urls as strings
        
    strings: bool DEFAULT True
        If True, function returns all the strings present on the team page
        If False, function returns all the stats present on the team page
    Returns
    -------
    team_page_list : list or list of lists
        List of all strings from team page(strings=TRUE), or list of all stats 
        from team page (strings=FALSE)

    '''
    if isinstance(url, str):
        soup = get_soup(url)
        
        team_page_list = list()
        for string in soup.stripped_strings:
            team_page_list.append(string)
                
        if strings == True:
            return {url[-6:] : team_page_list}
        
        else:
            team_stat_index = [team_page_list.index(substring) for substring 
                                   in team_page_list if "Team Stats" in substring][0]
        return {url[-6:] : team_page_list[team_stat_index:-1]}
    
    elif isinstance(url, list):
        soup_list = [get_soup(u) for u in url]
        
        team_page_list = list()
        for soup in soup_list:
            single_team_page = list()
            for string in soup.stripped_strings:
                single_team_page.append(string)
            team_page_list.append(single_team_page)
            
        if strings == True:
            return {url[i][-6:] : team_page_list[i] for i in range((len(url)))}
        
        else: 
            team_stat_index = list()
            team_stats = list()
            for team in team_page_list:
                single_team_stat_index = [team.index(substring) for substring 
                                       in team if "Team Stats" in substring][0]
                team_stat_index.append(single_team_stat_index)
                team_stats.append(team[single_team_stat_index:-1])
            return {url[i][-6:] : team_stats[i] for i in range((len(url)))}

       

def get_team_names(team_ids, zipme=False, page=False, **kwargs):
    '''
    Obtain the team name used by the ncaa website from the ncaa team id or a 
    list of ncaa team ids. Can zip the team id with team name.

    Parameters
    ----------
    team_ids : str or list
        Either a string of the id for the team or a list of ids for the team.
        Id is obtained from get_team_id function.
        
    zipme : bool DEFAULT False
        If set to true, zips the team id with the team name. If set to false,
        returns the team name without connection to id
        
    page : bool DEFAULT False
        If id or list of ids is entered, set to False. Else, set to true.
        
    **kwargs : dict
        Alternatively, enter the return of the get_team_page function. If 
        return of get_team_page function is entered, set page = True. This will
        not require get_team_pages to run again and save on computation time.
        
    Returns
    -------
    team_name or team_name_list : str or list
        Depends on input. If input a single team id as a string, returns team
        string as team name. If input a list of team ids, returns a list of 
        team names. Zipme value alters whether the ncaa team id is returned 
        with the team name as a tuple.

    '''
    if page == False:
        if isinstance(team_ids, list):
            team_url_list = get_url_from_id(team_ids)
            team_page_list = [get_team_page(url) for url in team_url_list]
            team_name_list = [page[page.index('Team Search:')+1] for page in team_page_list.values()]
            if zipme == True:
                return dict(zip(team_ids, team_name_list))
            
            else:
                return team_name_list
        
        elif isinstance(team_ids, str):
            team_url = "https://stats.ncaa.org/teams/%s" % team_ids
            team_soup = get_soup(team_url)
            team_name = get_team_page(team_soup)[get_team_page(team_soup).index('Team Search:')+1]
            
            if zipme == True:
                return dict(zip(team_ids, team_name))
            
            else:
                return team_name
        
    else: #page==True
        team_name_list = [page[page.index('Team Search:')+1] for page in kwargs.values()]
        
        if zipme == True:
            return dict(zip(team_ids, team_name_list))
        
        else:
            return team_name_list
        
    


def get_url_from_id(team_id):
    '''
    Get URL for team website on stats.ncaa.org

    Parameters
    ----------
    team_id : str or list of str
        String of team ID or list of teams' ids.
        Get id from get_team_ids.

    Returns
    -------
    team_url : str or list of str
        Returns strings or list of strings of valid urls to ncaa stat website 
        for the team/teams entered in team_id.

    '''
    if isinstance(team_id, list):
        urls = [("https://stats.ncaa.org/teams/%s" % team) for team in team_id]
        return urls
        
    elif isinstance(team_id, str):
        url = "https://stats.ncaa.org/teams/%s" % team_id
        return url
    
    else:
        raise Exception('''Error in id provided, team_id must either be a string 
                        or a list of strings corresponding to team ids''')






