"""Claude 桌面端扩展（.mcpb，uv 类型）的入口：由 `uv run` 在扩展目录里启动。"""

import sys

from creator_agent.mcp_server import main

if __name__ == "__main__":
    sys.exit(main())
