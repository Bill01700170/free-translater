import os
import json
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from google import genai

PORT = int(os.environ.get("PORT", 8000))

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found.")
    exit()

client = genai.Client(api_key=api_key)


class TranslatorHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/translate":
            self.send_error(404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)

            text = data.get("text", "")
            from_language = data.get("fromLanguage", "English")
            to_language = data.get("toLanguage", "Italian")

            prompt = f"""
Translate the following text from {from_language} to {to_language}.

Only give me the translation.
Do not explain it.

Text:
{text}
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            result = {"translation": response.text}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(result).encode("utf-8"))

        except Exception as error:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            result = {"error": str(error)}
            self.wfile.write(json.dumps(result).encode("utf-8"))


server = TCPServer(("0.0.0.0", PORT), TranslatorHandler)

print(f"Server running at http://localhost:{PORT}")

server.serve_forever()