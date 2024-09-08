from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            if self.path.endswith(".html"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(self.path[1:], 'rb') as file:
                    self.wfile.write(file.read())
            elif self.path.startswith('/static/'):
                self.send_static(self.path[1:])
            else:
                self.send_error(404, "File Not Found")
        except Exception:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == '/send':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            # Відправлення даних через socket на сервер для обробки
            self.send_to_socket_server(data)
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(404, "File Not Found")

    def send_static(self, path):
        try:
            with open(path, 'rb') as file:
                self.send_response(200)
                if path.endswith(".css"):
                    self.send_header('Content-type', 'text/css')
                elif path.endswith(".png"):
                    self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found: {}".format(path))

    def send_to_socket_server(self, data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', 5000)
        message = str(data).encode('utf-8')
        client_socket.sendto(message, server_address)
        client_socket.close()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 3000)
    httpd = server_class(server_address, handler_class)
    print('Running server on port 3000...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
