from requests import request
from config import *


def get_covid(query: dict) -> dict:
    covid_data = {
        'country': 'USA',
        'population': None,
        'deaths': None
        }
    try:
        country = query.get('country')
    except Exception:
        print(f'{RAPID_MSG} failed to get country from query, defaults to USA')
        params = {'country': 'USA'}
    else:
        params = {'country': country}
        covid_data['country'] = country
    response = request("GET", RAPID_API_URL, headers= RAPID_API_HEADERS, params=params)

    if response.status_code != OK:
        print(f'{RAPID_MSG} failed with status code: {response.status_code}')
        return covid_data
    response_data = response.json()

    if not response_data:
        print(f'{RAPID_MSG} api did respond with empty content')
        return covid_data
    response_data_response = response_data['response'][0]
    population = response_data_response['population']
    deaths = response_data_response['deaths']['total']
    covid_data['population'] = population
    covid_data['deaths'] = deaths
    return covid_data
