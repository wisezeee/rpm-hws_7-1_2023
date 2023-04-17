from http.server import BaseHTTPRequestHandler
from db_utils import DbHandler
from config import *
from json import loads
from views import covid, population, main_page
from dotenv import load_dotenv
from os import getenv
from covid import get_covid
from db_utils import InvalidQuery


load_dotenv()

RAPID_API_URL = getenv('RAPID_API_KEY')


class CustomHandler(BaseHTTPRequestHandler):
    def page(self, query: dict):
        if self.path.startswith(POPULATION):
            return population(DbHandler.get_data(query))
        elif self.path.startswith(COVID):
            return covid(get_covid(query))

    def get_template(self) -> tuple:
        if self.path.startswith((POPULATION, COVID)):
            try:
                query = self.parse_query()
            except Exception:
                return BAD_REQUEST
            return OK, self.page(query)
        return OK, main_page()

    def parse_query(self) -> dict:
        if self.path.startswith(POPULATION):
            possible_attrs = POPULATION_ALL_ATTRS
        else:
            possible_attrs = None
        qm_ind = self.path.find('?')
        if '?' in self.path and qm_ind != len(self.path) - 1:
            query_data = self.path[qm_ind + 1:].split('&')
            attrs_values = [line.split('=') for line in query_data]
            query = {key: int(value) if value.isdigit() else value for key, value in attrs_values}
            if possible_attrs:
                attrs = list(filter(lambda attr: attr not in possible_attrs, query.keys()))
                if attrs:
                    raise InvalidQuery(f'{__name__} unknown attributes: {attrs}')
            return query
        return None

    def get(self):
        self.respond(*self.get_template())

    def respond(self, http_code: int, msg: str):
        self.send_response(http_code)
        self.send_header(*CONTENT_TYPE)
        self.end_headers()
        self.wfile.write(msg.encode(CODING))

    def read_content_json(self) -> dict:
        content_length = int(self.headers.get(CONTENT_LENGTH, 0))
        if content_length:
            return loads(self.rfile.read(content_length).decode())
        return {}

    def delete(self):
        if self.path.startswith(POPULATION):
            query = self.parse_query()
            if not query:
                return BAD_REQUEST, 'DELETE FAILED'
            if DbHandler.delete(query):
                return OK, 'Content has been deleted'
        return NOT_FOUND, 'Content not found'

    def post(self, data_from_put=None, msg='') -> tuple:
        if self.path.startswith(POPULATION):
            request_data = self.read_content_json() if not data_from_put else data_from_put
            if not request_data:
                return BAD_REQUEST, f'{msg}No request data provided by {self.command}'
            for attr in request_data.keys():
                if attr not in POPULATION_ALL_ATTRS:
                    return NOT_IMPLEMENTED, f'{msg}Examples do not have attribute: {attr}'
            if all([req_attr in request_data for req_attr in POPULATION_REQUIRED_ATTRS]):

                return CREATED, f'{msg}{self.command} OK'
            return BAD_REQUEST, f'{msg}Required keys to add: {POPULATION_REQUIRED_ATTRS}'
        return NO_CONTENT, f'{msg}Request data for {self.command} not found'

    def put(self) -> tuple:
            if self.path.startswith(POPULATION):
                request_data = self.read_content_json()
                if not request_data:
                    return BAD_REQUEST, f'No request data provided by {self.command}'
                query = self.parse_query()
                if query:
                    not_possible = list(filter(lambda attr: attr not in POPULATION_ALL_ATTRS, query.keys()))
                    if not_possible:
                        return NOT_IMPLEMENTED, f'countries do not have attributes: {not_possible}'
                try:
                    update_res = DbHandler.update(where=query, data=request_data)
                except Exception as error:
                    return BAD_REQUEST, f'{self.command} error: {error}'
                if not update_res:
                    msg = 'Could not find data to change. '
                    request_data.update(query)
                    return self.post(request_data, msg)
                return OK, f'{self.command} OK.'
            return NO_CONTENT, f'Request data for {self.command} not found'

    def check_auth(self):
        auth = self.headers.get(AUTH, '').split()
        if len(auth) == 2:
            return DbHandler.is_valid_token(auth[0], auth[1][1:-1])
        return False

    def process_request(self):
        methods = {
            'PUT': self.put,
            'POST': self.post,
            'DELETE': self.delete
        }
        if self.command == 'GET':
            self.get()
            return
        if self.command in methods.keys():
            process = methods[self.command]
        else:
            self.respond(NOT_IMPLEMENTED, 'Unknown request method')
            return
        if self.check_auth():
            self.respond(*process())
            return
        self.respond(FORBIDDEN, 'Auth Fail')

    def do_PUT(self):
        self.process_request()

    def do_DELETE(self):
        self.process_request()

    def do_POST(self):
        self.process_request()

    def do_GET(self):
        self.process_request()
