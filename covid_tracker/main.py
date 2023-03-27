import http.server
from http_handler import Handler


def run():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Handler)

    httpd.serve_forever()


if __name__ == '__main__':
    run()
