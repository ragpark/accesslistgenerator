from __future__ import annotations

import html
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

from code_generator import generate_codes


def render_page(*, count: str = "100", seed: str = "", codes: str | None = None, error: str | None = None) -> str:
    safe_count = html.escape(str(count))
    safe_seed = html.escape(seed)
    safe_error = f'<div class="error">{html.escape(error)}</div>' if error else ""
    safe_codes = (
        f"""
      <section class=\"result\">
        <h2>Generated codes</h2>
        <textarea readonly>{html.escape(codes)}</textarea>
      </section>
      """
        if codes
        else ""
    )

    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Access Code Generator</title>
    <style>
      :root {{ font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
      body {{ background: #f4f6f8; margin: 0; padding: 2rem; }}
      .card {{ max-width: 720px; margin: 0 auto; background: #fff; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); padding: 1.5rem; }}
      h1 {{ margin-top: 0; }}
      form {{ display: grid; grid-template-columns: 1fr 1fr auto; gap: .75rem; align-items: end; }}
      label {{ display: grid; gap: .35rem; font-weight: 600; }}
      input, textarea, button {{ font: inherit; }}
      input, textarea {{ border: 1px solid #d0d7de; border-radius: 8px; padding: .6rem; }}
      button {{ background: #1f6feb; color: #fff; border: none; border-radius: 8px; padding: .7rem 1rem; cursor: pointer; }}
      .error {{ margin-top: 1rem; color: #b42318; font-weight: 600; }}
      .result {{ margin-top: 1rem; }}
      textarea {{ width: 100%; min-height: 280px; white-space: pre; }}
      @media (max-width: 700px) {{ form {{ grid-template-columns: 1fr; }} }}
    </style>
  </head>
  <body>
    <main class=\"card\">
      <h1>Access Code Generator</h1>
      <p>Generate unique 5-character non-word access codes suitable for datasheets.</p>
      <form method=\"post\" action=\"/generate\">
        <label>Number of codes<input type=\"number\" min=\"1\" step=\"1\" name=\"count\" value=\"{safe_count}\" required /></label>
        <label>Seed (optional)<input type=\"number\" step=\"1\" name=\"seed\" value=\"{safe_seed}\" placeholder=\"e.g. 1234\" /></label>
        <button type=\"submit\">Generate</button>
      </form>
      {safe_error}
      {safe_codes}
    </main>
  </body>
</html>
"""


class AppHandler(BaseHTTPRequestHandler):
    def _send_html(self, body: str, status: int = HTTPStatus.OK) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/":
            self._send_html(render_page(error="Page not found."), status=HTTPStatus.NOT_FOUND)
            return
        self._send_html(render_page())

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/generate":
            self._send_html(render_page(error="Page not found."), status=HTTPStatus.NOT_FOUND)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(body)

        count_raw = form.get("count", ["100"])[0]
        seed_raw = form.get("seed", [""])[0].strip()

        try:
            count = int(count_raw)
        except ValueError:
            self._send_html(render_page(count=count_raw, seed=seed_raw, error="Count must be a whole number."))
            return

        seed = int(seed_raw) if seed_raw else None

        try:
            codes = generate_codes(count, seed=seed)
        except ValueError as exc:
            self._send_html(render_page(count=str(count), seed=seed_raw, error=str(exc)))
            return

        self._send_html(render_page(count=str(count), seed=seed_raw, codes="\n".join(codes)))


def run() -> None:
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), AppHandler)
    print(f"Serving on http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
