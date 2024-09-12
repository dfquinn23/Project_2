import requests
import pandas as pd
import time

import json

from utils.api_data import get_url, get_header, get_query

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        total = end - start
        print(f'\033[95m api call time: {total} \033[0m')
        return res
    return wrapper

# External Funtions

# @timer
def fetch_market_data():
    """
    This function will query the sorare API for the query data found in utils/api_data.py
    until it has pulled all the available data.

    with each page query, it cleans the data and stored each card in the market_data array

    Once the query fully completes, it returns the market_data array
    """
    market_data = []
    has_next_page = True
    cursor = ""
    counter = 0
    max_counter = 1250000

    while has_next_page:
        query = get_query(cursor)
        
        response = requests.post(get_url(), json={'query': query}, headers=get_header())
        print(f"\033[92m---------------- {counter + 1} / {max_counter} ----------------\033[0m")
        print(f"\033[92m---------------- {counter + 1} ----------------\033[0m")
        print(f"\033[92m               {response.status_code}                    \033[0m")
        # if response.status_code != 200:
            # print(response.json())
        if response.status_code == 200:
            data = response.json()['data']['football']['allCards']['nodes']
            for card in data:
                
                card_data = process_card_data(card)

                market_data.append(card_data)
            
            # Update pagination variables
            has_next_page = response.json()['data']['football']['allCards']['pageInfo']['hasNextPage']
            # print(data['pageInfo']['hasNextPage'])
            # print(f'Counter: {counter}')
            counter += 1
            if counter >= max_counter: has_next_page = False
            time.sleep(0.15) if has_next_page == True else time.sleep(0.5)
            cursor = response.json()['data']['football']['allCards']['pageInfo']['endCursor']
        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text)
            break

    return market_data


def extract_hisotry(price_history):
    """
    called on the ownership column, filters the price action for the card by price
    creates columns for each price
    Work in progress.
    """
    price_dict = {}
    if(len(price_history) > 0):
        for index, price in enumerate(price_history):
            price_dict[f'Price_{(index+1)}'] = price['price_usd']
    else:
        price_dict['Price_1'] = 0
    return pd.Series(price_dict)

def filter_dataframe(df):
    """
    Filters out all clubs where their 'Domestic_League does not equal Premier League

    This includes ALL premier leagues across the world.
    """
    # df_filtered = df[df['Rarity'].isin(['limited', 'rare', 'super_rare', 'unique'])]
    df_filtered = df[df['Domestic_League'] == 'Premier League']
    df_filtered = df_filtered.drop(columns=['Active_Injuries', 'Active_Suspensions'])
    return df_filtered


## Internal functions

def process_card_data(card):
    """
    param: player card data that will be filtered and organize, then returned as a completed card for the prediction models
    """
    league, club, domesticLeagueRanking = process_league_club(card['player']['activeClub'])
    processing_card =  {
        'Rarity': card['rarity'],
        'First_Name': card['player']['firstName'],
        'Last_Name': card['player']['lastName'],
        'Display_Name': card['player']['displayName'],
        'Age': card['player']['age'],
        'Player_Number': card['shirtNumber'],
        'Domestic_League': league,
        'Domestic_League_Ranking': domesticLeagueRanking,
        'Current_Club': club,
        'Active_Injuries_Bool': 1 if len(card['player']['activeInjuries']) > 0 else 0,
        'Active_Injuries': card['player']['activeInjuries'],
        'Active_Suspensions_Bool': 1 if len(card['player']['activeSuspensions']) > 0 else 0,
        'Active_Suspensions': card['player']['activeSuspensions'],
        
        'Position': card['player']['position'],
        
        'Num_Of_Owners': process_number_of_owners(card['ownershipHistory']) if len(card['ownershipHistory']) > 0 else 0,
        'Average_Price': process_average_price(card['ownershipHistory']) if len(card['ownershipHistory']) > 0 else 0,
        'Ownership_History': process_ownership_history(card['ownershipHistory']) if len(card['ownershipHistory']) > 0 else []
    }

    for index, value in enumerate(process_scores(card['so5Scores'])):
        processing_card[f'So_5_Scores_{index}'] = value
        # print(index)
        # print(value)

    for index, so5Score in enumerate(card['so5Scores']):
        for key, value in so5Score["playerGameStats"].items():
            processing_card[f'{key}_{index}'] = value if value != 'null' and value != None else 0.0
    return processing_card

def process_league_club(active_club):
    """"
    Takes in the active_club of the returned data and returns the league, club and domestic league 
    the player card belongs to
    """
    
    try:
        league = active_club['domesticLeague']['name']
    except:
        league = 'None'
    try:
        club = active_club['name']
    except:
        club = 'None'
    try:
        domesticLeagueRanking = active_club['domesticLeagueRanking']
    except:
        domesticLeagueRanking = 'None'
    return league, club, domesticLeagueRanking

def process_scores(scores):
    """
    Processes so 5 scores
    """
    score_list = []
    for index in range(0, len(scores)):
        try:
            score_list.append(scores[index]['score'])
        except:
            score_list.append(0.0)
    return score_list


def process_ownership_history(price_history):
    """
    Takes in the ownership history and returns array with from and price data
    """
    if price_history is not None and len(price_history) > 0:
        return [
            {
                'from': entry.get('from', None),
                'price_usd': entry['amounts']['usd'] if entry.get('amounts') and entry['amounts'].get('usd') is not None else None
            }
            for entry in price_history if entry is not None
        ]
    else:
        return []

def process_number_of_owners(price_history):
    """
    returns the number of owners
    """
    if price_history is not None and len(price_history) > 0:
        # print(price_history)
        # print(len(price_history))
        return len(price_history)
    else:
        return 0
def process_average_price(price_history):
    """"
    returns the average traded price for the card
    """
    # print(price_history)
    if price_history is not None and len(price_history) > 0:
        total_price = 0
        if len(price_history) > 0:
            for entry in price_history:
                # print(entry)
                if entry is not None and 'amounts' in entry and entry['amounts'] is not None:
                    usd_amount = entry['amounts'].get('usd', 0)
                    total_price += 0 if usd_amount is None else usd_amount
            return total_price / len(price_history)
    else:
        return 0

class Timer_Class:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self):
        self.end = time.time()
        self.total = self.end - self.start
        print(f'\033[95m api call time: {self.total} \033[0m')

# with Timer_Class() as tc:
    #function call