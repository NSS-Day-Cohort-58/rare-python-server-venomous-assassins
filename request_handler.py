from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from urllib.parse import urlparse, parse_qs
from views.categories_request import get_all_categories
from views.posts_requests import get_all_posts
from views.tag_requests import get_all_tags
from views import create_user, login_user, get_all_users


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")

        query_params = []

        if url_components.query != '':
            query_params = url_components.query.split("&")

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id, query_params)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        response = {}

        if '?' not in self.path:
            parsed = self.parse_url(self.path)
            (resource, id, query_params) = parsed

            if resource == 'posts':
                self._set_headers(200)
                response = get_all_posts()

            if resource == 'tags':
                self._set_headers(200)
                response = get_all_tags()
            if resource == 'users':
                self._set_headers(200)
                response = get_all_users()

        else:
            parsed = self.parse_url(self.path)
            (resource, id, query_params) = parsed

            if resource == 'categories':
                self._set_headers(200)
                response = get_all_categories(query_params)

        self.wfile.write(json.dumps(response).encode())

    # def do_POST(self):
       # """Make a post request to the server"""
       # self._set_headers(201)
       # content_len = int(self.headers.get('content-length', 0))
       # post_body = json.loads(self.rfile.read(content_len))
       # response = ''
       # resource, _ = self.parse_url()#

       # if resource == 'login':
       #     response = login_user(post_body)
       # if resource == 'register':
       #     response = create_user(post_body)#

       # self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        pass

    def do_DELETE(self):
        """Handle DELETE Requests"""
        pass


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
