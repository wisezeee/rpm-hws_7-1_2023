import http.server
from jinja2 import Template
from api_handler.covid_api import country, deaths


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('templates/index.html', 'r') as f:
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

        elif self.path == '/covid':
            with open('templates/covid_usa.html', 'r') as f:
                template = Template(f.read())

            variables = {
                'title': 'Covid INFO',
                'heading': "Covid is bad",
                'country': country,
                'deaths': deaths
            }

            html = template.render(variables)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(html.encode())
