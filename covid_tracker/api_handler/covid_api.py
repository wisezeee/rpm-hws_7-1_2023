import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()


url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
	"X-RapidAPI-Key": f'{getenv("RAPID_API_KEY")}',
	"X-RapidAPI-Host": f'{getenv("RAPID_API_HOST")}'
}

response = requests.request("GET", url, headers=headers)

txt = response.json()['response'][0]
country = txt['continent']
north_america = txt['deaths']
today = north_america['total']
