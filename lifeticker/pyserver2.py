
#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# !! machine that takes ur deepest darkests thoughts and puts them on display for all to see !!


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if (self.path == "/"):
            message = ""
            with open("thoughts.txt") as f:
                for key in f.readlines():
                    message += key + '<br>'
             # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
        else:
            print(self.path)
            finalthought = self.path[1:][:-1].replace("_", " ")
            finalthought += "\n";
            with open("thoughts.txt", "a") as f:
                if (self.path[1:] == "favicon.ico"):
                    return
                if self.path[1:] not in thoughts:
                    f.write(finalthought)
                    thoughts.append(finalthought)

        return

with open("thoughts.txt") as f:
    thoughts = f.readlines()

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('198.110.204.9', 21103)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
