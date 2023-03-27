import base64
import http.server
from jinja2 import Template
from os import getenv
from api_handler.covid_api import today, country
from db_utils import pop_en, pop_all, pop_ru
from dotenv import load_dotenv

load_dotenv()

USERNAME = getenv("AUTH_NAME")
PASSWORD = getenv("AUTH_PASSWORD")


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            auth_header = self.headers.get("Authorization")
            if auth_header is None or auth_header != f"Basic {base64.b64encode(f'{USERNAME}:{PASSWORD}'.encode()).decode()}":
                self.do_AUTHHEAD()
                self.wfile.write(b'Unauthorized')
            else:
                try:
                    file_path = 'templates/index.html'
                    with open(file_path, 'r') as f:
                        template = Template(f.read())
                        variables = {
                            'title': 'main page',
                            'heading': 'On this site you can check COVID info.'

                        }
                        html = template.render(variables)
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()

                        self.wfile.write(html.encode())
                except:
                    self.send_error(404)

        elif self.path == '/covid_usa':
            with open('templates/covid_usa.html', 'r') as f:
                template = Template(f.read())

            variables = {
                'title': 'Covid INFO',
                'heading': "Covid is bad",
                'country': country,
                'deaths': today
            }

            html = template.render(variables)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(html.encode())

        elif self.path == "/population":
            with open('templates/population.html', 'r') as f:
                template = Template(f.read())

            variables = {
                'title': 'Population',
                'heading': "Planet population",
                'pop_ru': pop_ru,
                'pop_en': pop_en,
                'pop_all': pop_all
            }

            html = template.render(variables)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(html.encode())