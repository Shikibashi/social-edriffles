#!/usr/bin/env python3
"""Serve the production Social export with SPA history fallback."""

from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


class SpaHandler(SimpleHTTPRequestHandler):
    """Serve existing assets normally and route application paths to index.html."""

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        request_path = urlsplit(self.path).path
        candidate = Path(self.directory) / request_path.lstrip("/")
        if not candidate.exists() and "." not in Path(request_path).name:
            self.path = "/index.html"
        super().do_GET()

    def do_HEAD(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        request_path = urlsplit(self.path).path
        candidate = Path(self.directory) / request_path.lstrip("/")
        if not candidate.exists() and "." not in Path(request_path).name:
            self.path = "/index.html"
        super().do_HEAD()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=19008, type=int)
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not (directory / "index.html").is_file():
        raise SystemExit(f"production export is missing: {directory / 'index.html'}")

    handler = lambda *handler_args, **handler_kwargs: SpaHandler(  # noqa: E731
        *handler_args,
        directory=str(directory),
        **handler_kwargs,
    )
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Social static export: http://{args.host}:{args.port} -> {directory}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
