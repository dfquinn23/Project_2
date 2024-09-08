import os
from dotenv import load_dotenv

load_dotenv()

sorare_api_key = os.getenv('SORARE_API')

url = "https://api.sorare.com/graphql"
headers = {
    "Content-Type": "application/json",
    "APIKEY": sorare_api_key
}


def get_url():
    return url
def get_header():
    return headers
def get_query(cursor):
    return f"""
            {{ football {{
                    allCards(
                            first: 79, after: "{cursor}",
                            rarities: [custom_series, limited, rare, super_rare, unique],
                            sport: FOOTBALL) {{
                        nodes {{
                            shirtNumber
                            rarity
                            player {{
                                firstName
                                lastName
                                displayName
                                position
                                age
                                activeClub {{
                                    domesticLeague {{
                                    name
                                    }}
                                    domesticLeagueRanking
                                    name
                                }}
                                activeInjuries {{
                                    active
                                }}
                                activeSuspensions {{
                                    active
                                }}
                            }}
                            ownershipHistory {{
                                from
                                amounts {{
                                    usd
                                }}
                            }}
                            so5Scores(last: 10) {{
                                playerGameStats {{
                                    accuratePass
                                    assistPenaltyWon
                                    bigChanceCreated
                                    cleanSheet
                                    cleanSheet60
                                    crossAccuracy
                                    duelWon
                                    effectiveClearance
                                    errorLeadToGoal
                                    fouls
                                    gameStarted
                                    goalAssist
                                    goals
                                    interceptionWon
                                    lastManTackle
                                    minsPlayed
                                    ownGoals
                                    passAccuracy
                                    penaltiesSaved
                                    penaltyConceded
                                    penaltyKickMissed
                                    penaltySave
                                    redCard
                                    saves
                                    shotAccuracy
                                    totalClearance
                                    totalPass
                                    wonTackle
                                    yellowCard
                                }}
                                score
                            }}
                        }}
                        pageInfo {{
                            hasNextPage
                            endCursor
                        }}
                    }}
                }}
            }}
            """





    # return f"""
    #         {{
    #             allCards(first: 250, after: "{cursor}") {{
    #             nodes {{
    #                 slug
    #                 name
    #                 age
    #                 shirtNumber
    #                 player {{
    #                 firstName
    #                 lastName
    #                 displayName
    #                 position
    #                 age
    #                 activeClub {{
    #                     domesticLeague {{
    #                     name
    #                     }}
    #                     name
    #                 }}
    #                 activeInjuries {{
    #                 active
    #                 }}
    #                 activeSuspensions {{
    #                 active
    #                 }}
    #                 so5Scores(last:5) {{
    #                 score
    #                 }}
    #                 }}
    #                 rarity
    #                 token {{
    #                 ownershipHistory {{
    #                     from
    #                     price{{
    #                     usd
    #                     }}
    #                 }}
    #                 }}
    #             }}
    #             pageInfo {{
    #                 hasNextPage
    #                 endCursor
    #             }}
    #             }}
    #         }}
    #         """