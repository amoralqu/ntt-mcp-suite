from __future__ import annotations

from ntt_jadx_mcp.server.app import create_app


def main() -> None:
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
