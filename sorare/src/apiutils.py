import requests
import pandas as pd
import time

from apidata import get_url, get_header, get_query

# External Funtions

def fetch_market_data():
    market_data = []
    has_next_page = True
    cursor = ""
    counter = 0
    max_counter = 250

    while has_next_page:
        query = get_query(cursor)
        
        response = requests.post(get_url(), json={'query': query}, headers=get_header())
        print(f"\033[92m---------------- {counter + 1} / {max_counter} ----------------\033[0m")
        print(f"\033[92m                  {response.status_code}                    \033[0m")
        if response.status_code != 200:
            print(response)
        time.sleep(1)
        if response.status_code == 200:
            data = response.json()['data']['allCards']['nodes']
            for card in data:
                    
                card_data = process_card_data(card)

                market_data.append(card_data)
            
            # Update pagination variables
            has_next_page = response.json()['data']['allCards']['pageInfo']['hasNextPage']
            # print(data['pageInfo']['hasNextPage'])
            # print(f'Counter: {counter}')
            counter += 1
            if counter > max_counter: has_next_page = False
            time.sleep(3) if has_next_page == True else time.sleep(1)
            cursor = response.json()['data']['allCards']['pageInfo']['endCursor']
        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text)
            break

    return market_data


def extract_hisotry(price_history):
    price_dict = {}
    if(len(price_history) > 0):
        for index, price in enumerate(price_history):
            price_dict[f'Price_{(index+1)}'] = price['price_usd']
    else:
        price_dict['Price_1'] = 0
    return pd.Series(price_dict)

def filter_dataframe(df):
    df_filtered = df[df['Rarity'].isin(['limited', 'rare', 'super_rare', 'unique'])]
    df_filtered = df[df['Domestic_League'] == 'Premier League']
    df_filtered = df_filtered.drop(columns=['Active_Injuries', 'Active_Suspensions', 'Slug'])
    return df_filtered


## Internal functions

def process_card_data(card):
    league, club = process_league_club(card['player']['activeClub'])
    score_one, score_two, score_three, score_four, score_five = process_scores(card['player']['so5Scores'])
    return {
        'Slug': card['slug'],
        'Rarity': card['rarity'],
        'First_Name': card['player']['firstName'],
        'Last_Name': card['player']['lastName'],
        'Display_Name': card['player']['displayName'],
        'Age': card['player']['age'],
        'Player_Number': card['shirtNumber'],

        'Domestic_League': league,
        'Current_Club': club,
        'Active_Injuries_Bool': 1 if len(card['player']['activeInjuries']) > 0 else 0,
        'Active_Injuries': card['player']['activeInjuries'],
        'Active_Suspensions_Bool': 1 if len(card['player']['activeSuspensions']) > 0 else 0,
        'Active_Suspensions': card['player']['activeSuspensions'],

        'So_5_Scores_One': score_one,
        'So_5_Scores_Two': score_two,
        'So_5_Scores_Three': score_three,
        'So_5_Scores_Four': score_four,
        'So_5_Scores_Five': score_five,
        'Position': card['player']['position'],
        
        'Num_Of_Owners': process_number_of_owners(card['token']['ownershipHistory']) if card['token'] != None else 0,
        'Average_Price': process_average_price(card['token']['ownershipHistory']) if card['token'] != None else 0,
        'Ownership_History': process_ownership_history(card['token']['ownershipHistory']) if card['token'] != None else []
    }

def process_league_club(active_club):
    
    try:
        league = active_club['domesticLeague']['name']
    except:
        league = 'None'
    try:
        club = active_club['name']
    except:
        club = 'None'
    return league, club

def process_scores(scores):
    try:
        score_one = scores[0]['score']
    except:
        score_one = 0.0
    try:
        score_two =  scores[1]['score']
    except:
        score_two = 0.0
    try:
        score_three = scores[2]['score']
    except:
        score_three = 0.0
    try:
        score_four = scores[3]['score']
    except:
        score_four = 0.0
    try:
        score_five = scores[4]['score']
    except:
        score_five = 0.0
    return score_one, score_two, score_three, score_four, score_five

def process_ownership_history(price_history):
    if price_history != None:
        return [{'from': entry['from'], 'price_usd': entry['price']['usd']} for entry in price_history]
    else:
        return []

def process_number_of_owners(price_history):
    if price_history != None:
        # print(price_history)
        # print(len(price_history))
        return len(price_history)
    else:
        return 0
def process_average_price(price_history):
    if price_history != None:
        total_price = 0
        if len(price_history) > 0:
            for entry in price_history:
                total_price += entry['price']['usd']
            return total_price / len(price_history)
    else:
        return 0
