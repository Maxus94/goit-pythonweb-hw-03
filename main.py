import urllib.parse
import mimetypes
import pathlib
import json

from pathlib import Path

from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            data_path = Path("storage") / "data.json"
            with open(data_path, "r+") as fh:
                # with open("storage\data.json", "r+") as fh:
                logs = json.load(fh)
                print(logs)
                BASE_DIR = Path(__file__).resolve().parent
                env = Environment(loader=FileSystemLoader(BASE_DIR))
                # env = Environment(loader=FileSystemLoader("."))
                template = env.get_template("read.html")
                output = template.render(
                    logs=logs,
                )
                with open("new_read.html", "w", encoding="utf-8") as fh:
                    fh.write(output)
                self.send_html_file("new_read.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        now = datetime.now()
        print(now)
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        print(data_dict)
        data_path = Path("storage") / "data.json"
        with open(data_path, "r+") as fh:
            # with open("storage\data.json", "r+") as fh:
            logs = json.load(fh)
            print(logs)
        with open(data_path, "w") as fh:
            # with open("storage\data.json", "w") as fh:
            logs[str(now)] = data_dict
            print(logs)
            fh.write(json.dumps(logs))
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
