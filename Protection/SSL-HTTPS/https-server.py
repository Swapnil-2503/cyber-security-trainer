from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set response status code
        self.send_response(200)
        # Set headers
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SSL Certificate/TLS Certificate Experiment</title>
        </head>
        <body>
            <h1>SSL Certificate/ TLS Certificate Experiment</h1>
        </body>
        </html>
        """
        # Write the HTML content to the response
        self.wfile.write(html_content.encode("utf-8"))


# Define server address and port
server_address = ('', 8080)  # '' means all available interfaces
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# Create an SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Wrap the HTTPServer's socket with the SSL context
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

httpd.serve_forever()
