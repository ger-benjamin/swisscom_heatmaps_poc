from http.server import HTTPServer, BaseHTTPRequestHandler
from swisscom.entry import Entry
from json import dumps

PORT = 8000
PATHS = {
    'kml': '/2012_Earthquakes_Mag5.kml',
    'dwell-density': '/dwell-density.json'
}
entry = None


class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server_class):
        self.server_class = server_class
        super().__init__(request, client_address, server_class)

    def set_common_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()

    def set_json_response(self, response):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", len(response))
        self.set_common_headers()


    def set_kml_response(self, response):
        self.send_response(200)
        self.send_header("Content-type", "application/vnd.google-earth.kml+xml")
        self.send_header("Content-Length", len(response))
        self.set_common_headers()


    def do_GET(self):
        print(f"Got a GET request on path: {self.path}")
        if self.path == PATHS['dwell-density']:
            response = entry.get_dwell_density()
            self.set_json_response(response)
            self.wfile.write(response.encode('utf-8'))
        if self.path == PATHS['kml']:
            file_path = 'data/2012_Earthquakes_Mag5.kml'
            with open(file_path, 'r') as file:
                content = file.read()
            self.set_kml_response(content)
            self.wfile.write(content.encode('utf-8'))


if __name__ == '__main__':
    entry = Entry()
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, MyHttpRequestHandler)
    print(f"Local server listening on port: {PORT}")
    print(f"Try path: {', '.join(PATHS.values())}")
    httpd.serve_forever()