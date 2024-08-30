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
            {{
                allCards(first: 250, after: "{cursor}") {{
                nodes {{
                    slug
                    name
                    age
                    shirtNumber
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
                        name
                    }}
                    activeInjuries {{
                    active
                    }}
                    activeSuspensions {{
                    active
                    }}
                    so5Scores(last:5) {{
                    score
                    }}
                    }}
                    rarity
                    token {{
                    ownershipHistory {{
                        from
                        price{{
                        usd
                        }}
                    }}
                    }}
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
                }}
            }}
            """