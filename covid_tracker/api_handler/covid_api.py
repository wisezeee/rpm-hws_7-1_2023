import requests
from pprint import pprint

url = "https://covid-19-tracking.p.rapidapi.com/v1/usa"

headers = {
    "X-RapidAPI-Key": "d8a2b24394msh530522f623e5ebcp1dff13jsn3401538088fc",
    "X-RapidAPI-Host": "covid-19-tracking.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

country = response.json()['Country_text']
deaths = response.json()['Total Deaths_text']