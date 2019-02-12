#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        if self.path != "":
            #ignore favicon
            if self.path == "/favicon.ico":
                return

            #write value of data[path]
            if self.path[1:] in data:
                self.wfile.write(bytes(data[self.path[1:]], "utf8"))

            #or 404
            else:
                self.wfile.write(bytes(thoughts[0], "utf8"))

        #if no path specified return list of keys
        else:
            message = '<h1>List of Keys</h1>'

            for key in thoughts:
                message += key + '<br>'

            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))

        return

    def do_PUT(self):
        #adds or updates an item to the database, using the path as the key.
        path = self.path[1:]

        #retrieve content length of request
        request_headers = self.headers
        content_length = request_headers.get('content-length')

        #send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        #read and decode contents of PUT request
        param = self.rfile.read(int(content_length)).decode("utf-8")

        #save the contents of the request using path as the key
        data[path] = param
        print(data)
        return

    def do_DELETE(self):
        path = self.path[1:]

        #delete key if path is specified
        if path != "":
            if path in data:
                del data[path]

        #otherwise delete every key!
        else:
            data.clear()

        return

with open("thoughts.txt") as f:
	thoughts = f.readlines()
data = {}

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('198.110.204.9', 11021)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
