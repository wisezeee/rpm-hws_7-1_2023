HOST = '127.0.0.1'
PORT = 8001

COVID = "/covid"     
POPULATION = '/population' 
PAGES = (COVID, POPULATION)


MAIN_PAGE = 'index.html'
COVID_TEMPLATE = 'covid.html'
POPULATION_TEMPLATE = 'population.html'

CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = ('Content-Type', 'text/html')
AUTH = 'Authorization'

NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400

OK = 200
CREATED = 201
NO_CONTENT = 204
NOT_IMPLEMENTED = 501
INTERNAL_ERROR = 500

SELECTOR = 'SELECT * FROM country'
GET_TOKEN = "SELECT token FROM token WHERE username='{username}'"
INSERT = "INSERT INTO country ({keys}) VALUES ({values}) RETURNING id"
UPDATE = "UPDATE country SET {request}"
DELETE = 'DELETE FROM country '
POPULATION_REQUIRED_ATTRS = ['name', 'continent']
POPULATION_ALL_ATTRS = ['id', 'name', 'continent', 'date', 'population']

CODING = 'KOI8-R'

RAPID_API_URL = "https://covid-193.p.rapidapi.com/statistics"
RAPID_API_HOST = "covid-193.p.rapidapi.com"
RAPID_API_HEADERS = {
	"X-RapidAPI-Key": "b385c1c208mshba131d96fd1f2f7p1b985bjsn8bb4df59657f",
	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
}

RAPID_MSG = 'API get_covid'

