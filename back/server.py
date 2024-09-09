from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8000


class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(MyHttpRequestHandler, self).end_headers()


    def do_GET(self):
        print(f"Got a GET request on path: {self.path}")
        if self.path == '/2012_Earthquakes_Mag5.kml':
            self.path = 'data/2012_Earthquakes_Mag5.kml'
        return SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, MyHttpRequestHandler)
    print(f"Local server listening on port: {PORT}")
    httpd.serve_forever()