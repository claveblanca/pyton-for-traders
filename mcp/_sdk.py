"""Import the official MCP Python SDK without shadowing by this repo's mcp/ folder."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

_LOCAL_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _LOCAL_DIR.parent


def load_mcpserver():
    """Return MCPServer class from the PyPI `mcp` package (v2+)."""
    to_drop = {_PROJECT_ROOT.resolve(), _LOCAL_DIR.resolve()}
    new_path = [p for p in sys.path if Path(p).resolve() not in to_drop]
    for name in list(sys.modules):
        if name == "mcp" or name.startswith("mcp."):
            mod = sys.modules.get(name)
            mod_file = getattr(mod, "__file__", None)
            if mod_file and Path(mod_file).resolve().is_relative_to(_PROJECT_ROOT):
                del sys.modules[name]

    old_path = sys.path
    try:
        sys.path = new_path
        from mcp.server.mcpserver import MCPServer

        return MCPServer
    finally:
        sys.path = old_path


if TYPE_CHECKING:
    from mcp.server.mcpserver import MCPServer as MCPServerType
