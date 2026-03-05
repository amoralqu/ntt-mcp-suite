# src/ntt_objection_mcp/server/main.py
from .app import mcp


def main() -> None:
    """Run the MCP server over STDIO."""
    mcp.run()


if __name__ == "__main__":
    main()
