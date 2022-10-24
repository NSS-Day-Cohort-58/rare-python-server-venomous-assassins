from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from urllib.parse import urlparse, parse_qs
from views.categories_request import create_category, get_all_categories
from views.comment_requests import get_comments_by_post_id
from views.post_tags_requests import create_post_tag, get_all_post_tags
from views.posts_requests import get_all_posts, create_post, get_single_post, delete_post, update_post
from views.categories_request import get_all_categories, create_category
from views.tag_requests import create_tag, delete_tag, get_all_tags, update_tag
from views import create_user, login_user, get_all_users, create_subscription, get_all_subscriptions,delete_subscription
from views.user_requests import get_single_user
from views import create_comment


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        '''parses url'''
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

            if resource =='post_tags':
                self._set_headers(200)
                response = get_all_post_tags()


            if resource == 'posts':
                if id is None:
                    self._set_headers(200)
                    response = get_all_posts()
                else:
                    self._set_headers(200)
                    response = get_single_post(id)

            if resource == 'tags':
                self._set_headers(200)
                response = get_all_tags()
                
            if resource == 'users':
                if id is None:
                    self._set_headers(200)
                    response = get_all_users()
                else:
                    self._set_headers(200)
                    response = get_single_user(id)
            if resource == 'subscriptions':
                if id is None:
                    self._set_headers(200)
                    response = get_all_subscriptions()
            if resource == 'comments':
                if id is None:
                    self._set_headers(200)
                else:
                    self._set_headers(200)
                    response = get_comments_by_post_id(id)

        else:
            parsed = self.parse_url(self.path)
            (resource, id, query_params) = parsed

            if resource == 'categories':
                self._set_headers(200)
                response = get_all_categories(query_params)
            if resource == 'post_tags':
                self._set_headers(200)
                response = get_all_post_tags(query_params)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))

        parsed = self.parse_url(self.path)
        (resource, id, query_params) = parsed

        response = None
        if resource == 'post_tags':
            response = create_post_tag(post_body)
        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'tags':
            response = create_tag(post_body)
        if resource == 'posts':
            response = create_post(post_body)
        if resource == 'categories':
            response = create_category(post_body)
        if resource == 'subscriptions':
            response = create_subscription(post_body)
        if resource == 'comments':
            if id is None:
                self._set_headers(404)
            else:
                self._set_headers(200)
                response = create_comment(post_body)

        self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""

        # self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        parsed = self.parse_url(self.path)
        (resource, id, query_params) = parsed

        success = False

        if resource == "tags":
            success = update_tag(id, post_body)
        if resource == "posts":
            success = update_post(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        (resource, id, query_params) = self.parse_url(self.path)

        if resource == "tags":
            delete_tag(id)
            self._set_headers(204)

        if resource == "posts":
            delete_post(id)
            self._set_headers(204)

        if resource == "subscriptions":
            delete_subscription(id)
            self._set_headers(204)

        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
