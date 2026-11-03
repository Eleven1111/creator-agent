# 接入 agent 终端

[English summary](#english-summary)

creator-agent 提供两样东西，几个终端通用：

| 组件 | 作用 | 用在哪 |
|---|---|---|
| **MCP 服务器** `creator-agent-mcp` | 25 个工具：查看状态、跑各阶段、记录闸口、改稿、记录发布、录入指标、审计 | 所有支持 MCP 的终端 |
| **技能包** `SKILL.md` | 告诉终端里的 agent 按什么顺序用这些工具，以及不能做什么（替作者批闸口、编造、发布） | 支持 SKILL.md 的终端：Claude、OpenClaw、Hermes、WorkBuddy |

**建议两样都装。** 只装 MCP，agent 也能调用工具，但未必知道要先把稿子给你看、等你同意再批闸口。技能包就是把这些规矩写给它看的。

> **关于准确性。** 下面的配置格式，Claude 桌面端和通用 MCP 部分依据的是 MCP 官方约定，比较可靠。OpenClaw、Hermes、WorkBuddy、ChatGPT 的配置路径和菜单位置来自 2026 年 11 月的检索，其中不少是第三方文档，已标注【待核实】。这些产品更新很快，请以你安装的版本为准。

---

## 0. 先装好服务器

```bash
pip install -e '.[mcp]'
```

```bash
ca init ~/creator-vault
```

确认能启动（按 Ctrl+C 退出）：

```bash
creator-agent-mcp --vault ~/creator-vault
```

找到命令的绝对路径，下面的配置里要用。终端启动子进程时通常不读你的 shell 配置，写绝对路径最稳：

```bash
which creator-agent-mcp
```

服务器需要的环境变量：

| 变量 | 必须？ | 说明 |
|---|---|---|
| `CA_VAULT` | 必须（或用 `--vault` 参数） | 知识库目录 |
| `ANTHROPIC_API_KEY` | 跑模型阶段时必须 | angles / research / outline / draft B / review / adapt / interview / retro 需要；查看状态、lint、记录闸口、改稿、审计等不需要 |
| `X_BEARER_TOKEN` | 可选 | 只用于 `pull_x_metrics` 读取公开指标 |
| `CA_MCP_TOKEN` | HTTP 模式对外暴露时必须 | 见第 2 节 |

> **为什么终端自己有模型，还要 Anthropic API key？** 研究、评审、改编这些阶段需要联网搜索、结构化输出和带锚点的评分，是在服务器里调用 Anthropic API 完成的，不依赖终端用的是哪个模型。如果不想配 key，终端里的模型照样能用不调模型的那些工具：状态查看、lint、X 规则检查、闸口记录、改稿、发布记录、指标、审计。

---

## 1. Claude 桌面端

**MCP。** 编辑配置文件，没有就新建：

- macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "creator-agent": {
      "command": "/绝对路径/creator-agent-mcp",
      "args": ["--vault", "/Users/你/creator-vault"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "X_BEARER_TOKEN": ""
      }
    }
  }
}
```

保存后**完全退出**并重启 Claude 桌面端。在对话的工具菜单里能看到 creator-agent 的工具就说明连上了。

**技能包。** 生成 zip：

```bash
ca install-skill zip
```

在 Claude 的设置里找到 Skills（技能）上传 `creator-agent-skill.zip`。菜单位置以当前版本为准【待核实】。用 Claude Code 的话，直接装到 `~/.claude/skills`：

```bash
ca install-skill claude-code
```

---

## 2. ChatGPT 桌面端

ChatGPT 接 MCP 走的是“开发者模式 / 自定义连接器”。检索到的资料大多说**只支持远程 HTTPS 服务器**，也有一篇说桌面端可以跑本地 stdio，说法互相矛盾【待核实】。下面按远程方式写，这种方式在网页端和桌面端都适用。

**第 1 步：用 HTTP 模式启动，并设一个长随机 Token。**

```bash
export CA_MCP_TOKEN=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
```

```bash
creator-agent-mcp --vault ~/creator-vault --http --port 8765 --allowed-host 你的隧道域名
```

**第 2 步：用隧道把本机端口暴露成 HTTPS。** 以 Cloudflare Tunnel 为例：

```bash
cloudflared tunnel --url http://127.0.0.1:8765
```

它会给出一个 `https://xxxx.trycloudflare.com` 地址。把这个域名填进上一步的 `--allowed-host`（不带 `https://`），然后重启服务器。

**第 3 步：在 ChatGPT 里添加自定义连接器。** 路径大致是 设置 → Apps / Connectors → 高级设置 → 开发者模式 → 新建【待核实】。URL 填：

```
https://xxxx.trycloudflare.com/mcp?token=你的CA_MCP_TOKEN
```

- 如果连接器支持自定义请求头，优先用 `Authorization: Bearer 你的Token`，URL 里不带 token。
- **Token 放在 URL 里会出现在隧道和服务端日志里。** 只在自己用、用完关掉隧道的场景下这样做。
- 开发者模式据报道是 beta，只对部分付费方案开放【待核实】。

**技能包。** ChatGPT 不读 SKILL.md。把 `creator_agent/skill/creator-agent/SKILL.md` 的正文粘贴进 Project 的 Instructions，或者对话开头，效果相同。

---

## 3. OpenClaw

**MCP。** OpenClaw 的 MCP 客户端配置在 `openclaw.json` 的 `mcp.servers` 下，可以用 `openclaw mcp list / show / set / unset` 管理；每个服务器支持 `enabled`、`toolFilter.include/exclude`、`requestTimeoutMs`【待核实，来自 docs2.openclaw.ai 与第三方指南】。示例：

```json
{
  "mcp": {
    "servers": {
      "creator-agent": {
        "command": "/绝对路径/creator-agent-mcp",
        "args": ["--vault", "/Users/你/creator-vault"],
        "env": { "ANTHROPIC_API_KEY": "sk-ant-..." },
        "requestTimeoutMs": 600000
      }
    }
  }
}
```

研究和评审单次可能要几分钟，建议把超时调大。

**技能包。** 装到 `~/.openclaw/skills/creator-agent/` 【待核实】：

```bash
ca install-skill openclaw
```

---

## 4. Hermes Agent（Nous Research）

**MCP。** 写在 `~/.hermes/config.yaml` 的 `mcp_servers` 下，按服务器名区分；本地服务器用 `command`，远程用 `url`。**Hermes 默认不把你 shell 里的密钥传给 MCP 服务器，必须在 `env` 里显式写出**【待核实，来自 Hermes 文档与第三方指南】。

```yaml
mcp_servers:
  creator-agent:
    command: /绝对路径/creator-agent-mcp
    args: ["--vault", "/Users/你/creator-vault"]
    env:
      ANTHROPIC_API_KEY: sk-ant-...
```

改完在对话里执行 `/reload-mcp`【待核实】。

**技能包。** Hermes 的技能遵循 agentskills.io 标准，位于 `~/.hermes/skills/<name>/SKILL.md`：

```bash
ca install-skill hermes
```

---

## 5. WorkBuddy（腾讯）

据报道 WorkBuddy 支持 MCP 和 SKILL.md 技能包。有文章说 Skills 安装和 MCP 配置需要企业版，未核实【待核实】。

**MCP。** 在 WorkBuddy 的连接器 / MCP 设置里添加本地服务器：命令填 `creator-agent-mcp` 的绝对路径，参数填 `--vault 你的知识库目录`，环境变量填 `ANTHROPIC_API_KEY`。如果它要求粘贴 JSON，用第 1 节 Claude 桌面端的 `mcpServers` 格式（大多数 MCP 客户端通用）。

**技能包。** 据第三方文章，手动加载的路径是用户目录下的 `.workbuddy/skills`，放好后重启【待核实】：

```bash
ca install-skill workbuddy
```

也可以用 `ca install-skill zip` 生成压缩包，在技能市场里本地导入。

---

## 6. 其他终端

- **只支持 stdio**：命令是 `creator-agent-mcp`，参数 `--vault <目录>`，环境变量见第 0 节。
- **只支持 HTTP**：`creator-agent-mcp --http`，地址 `http://127.0.0.1:8765/mcp`。
- **技能目录不在上面的列表里**：`ca install-skill dir --dir <技能目录>`，或者 `ca install-skill agents` 装到项目里的 `.agents/skills/`。
- **完全不支持 MCP，但能执行命令行**：只装技能包。SKILL.md 里写了每个工具对应的 `ca` 命令。

---

## 安全设计

| 风险 | 做法 |
|---|---|
| agent 替你批闸口 | `approve_gate` 要求 `user_statement` 逐字写入你同意的那句话，记录里标明 `channel: mcp`，`ca audit` 会列出所有经 MCP 批准的闸口。不放心的话，在 `agent.yaml` 设 `mcp.allow_gate_approval: false`，闸口就只能在命令行批 |
| agent 编造你的经历和数字 | 与命令行相同：经历只能来自 `stories.md`，数字和引语要有来源，S5 会拦截；agent 代写的正文要用 `written_by: agent_assisted` 标注 |
| agent 替你发布或互动 | 服务器里**没有任何发布或互动工具**。`mark_published` 只是在你发完后记下链接 |
| 读到不该读的文件 | `read_hub_file` 只允许白名单里的文件名，路径穿越会被拒绝 |
| HTTP 暴露到公网 | 默认只监听 127.0.0.1；监听非本机地址或允许外部 Host 时，必须设置 `CA_MCP_TOKEN`，否则拒绝启动；校验 Host 头防 DNS 重绑定；Token 用恒定时间比较 |
| 密钥泄露 | 密钥只放在终端配置的 `env` 里，不写进知识库；Hermes 默认不透传环境变量，正好避免误传 |

---

## English summary

creator-agent ships an **MCP server** (`creator-agent-mcp`, stdio by default, Streamable HTTP with `--http`) and a portable **`SKILL.md`** (`ca install-skill claude-code | openclaw | hermes | workbuddy | agents | zip | dir`).

- **Claude Desktop:** add an `mcpServers.creator-agent` entry with the absolute path to `creator-agent-mcp`, `--vault <dir>` and `ANTHROPIC_API_KEY` in `env`; upload the skill zip under Skills.
- **ChatGPT:** run `--http` with `CA_MCP_TOKEN`, expose it through an HTTPS tunnel, pass `--allowed-host <tunnel host>`, and add a custom connector pointing at `https://<host>/mcp?token=<token>` (prefer an `Authorization: Bearer` header if the connector supports one). Paste the SKILL.md body into project instructions.
- **OpenClaw:** `mcp.servers.creator-agent` in `openclaw.json`; skills in `~/.openclaw/skills`.
- **Hermes Agent:** `mcp_servers.creator-agent` in `~/.hermes/config.yaml`, with secrets listed explicitly under `env`; skills in `~/.hermes/skills`.
- **WorkBuddy:** add a local MCP server in its connector settings; skills in `~/.workbuddy/skills`.

Paths and menus for ChatGPT, OpenClaw, Hermes and WorkBuddy come from November 2026 searches, partly third-party sources, and may differ in your version. Model-backed stages need `ANTHROPIC_API_KEY` on the server; deterministic tools work without it. The server exposes no publishing or engagement tools, gate approvals require the user's verbatim statement and are listed by `ca audit`, and `mcp.allow_gate_approval: false` restricts approvals to the CLI.

### Sources

- OpenClaw MCP and skills: [docs2.openclaw.ai – mcp and skills](https://docs2.openclaw.ai/nodes/mcp-and-skills), [config extensions](https://docs2.openclaw.ai/gateway/config-extensions.md), [fast.io guide](https://www.fast.io/resources/mcp-skills-openclaw-development-guide/)
- Hermes Agent: [Hermes docs – native MCP](https://hermes-agent.nousresearch.com/docs/ko/user-guide/skills/bundled/mcp/mcp-native-mcp), [fast.io guide](https://fast.io/resources/hermes-agent-mcp-server/), [Microsoft APM – Hermes](https://microsoft.github.io/apm/integrations/hermes/)
- WorkBuddy: [awesome-workbuddy](https://github.com/semlinker/awesome-workbuddy), [腾讯云开发者社区](https://cloud.tencent.com/developer/article/2656859), [AIbase](https://www.aibase.com/zh/news/26048)
- ChatGPT MCP: [hjarni.com](https://hjarni.com/blog/how-to-use-mcp-with-chatgpt), [contextbolt.com](https://contextbolt.com/blog/ai-tools-mcp-support/), [mcpbundles.com](https://www.mcpbundles.com/guides/mcp-clients)
