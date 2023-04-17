from config import *


def list_to_view(iterable: list):
    return ''.join([f'<ul>{item}</ul>' for item in iterable]) if iterable else '<p>No data given.</p>'


def covid(covid_data: dict) -> str:
    with open(COVID_TEMPLATE, 'r') as template:
        return template.read().format(**covid_data)


def population(population_data: dict) -> str:
    with open(POPULATION_TEMPLATE, 'r') as template:
        page = template.read()
        return page.format(**population_data)


def main_page() -> str:
    with open(MAIN_PAGE, 'r') as template:
        return template.read()
