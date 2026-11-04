# creator-agent

[![CI](https://github.com/Eleven1111/creator-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Eleven1111/creator-agent/actions/workflows/ci.yml)

**English** · [简体中文](README.zh-CN.md)

A command-line creative agent for newsletter and social writers. It helps with choosing topics, research, outlining, editorial review, fact checking, adapting one piece for several platforms, and monthly retrospectives.

It is a research assistant and editor, **not a ghostwriter**. By default you write the body yourself. And **it never publishes anything on your behalf**: it produces drafts and a publish kit, and you post them yourself in the Substack, X and Medium apps.

> **Language note.** The CLI messages, the model prompts and the generated review files are in Simplified Chinese, as are the [tutorial](TUTORIAL.md) and the research handbook in [`docs/`](docs/README.md). The tool targets Chinese-language writers who publish on Substack and X, with optional English rewrites for Medium.

## Why it exists

The design comes from researching how top creators on Substack, X and Medium actually work (Lenny Rachitsky, Heather Cox Richardson, Packy McCormick, Dan Koe, Paul Graham, Morgan Housel, David Perell, Tim Denning and others), and from verifying each platform's current rules against primary sources. The result is a handbook ([`docs/handbook/`](docs/handbook/)) whose roadmap this tool implements, phases P0 through P4.

A few principles run through everything:

- **Workflow, not an autonomous agent.** Each stage makes one or a few well-defined model calls and writes markdown for you to review. Nothing moves forward until you approve it at a human gate.
- **No fabrication.** Facts must cite research findings; your experiences can only come from a stories file you confirmed; anything missing is marked `[TK: ...]` and blocks review.
- **Humans publish.** No platform write API is called anywhere. All interactions on X (replies, likes, follows, quotes) stay with you.

## Pipeline

```
S1 angles ─H1→ S2 research ─H2→ S3 outline ─H3→ S4 draft → S5 review ─H4→
S6 adapt (x_post / substack_note / x_thread / x_article / medium_story + Substack package)
   → review queue (edit variants/<id>.md) ─H5 (re-check)→ publish_kit.md → you publish → ca published
   → S8 read-only metrics → monthly retro ─H7→ R1 ideas back into the backlog
```

| Stage | What it does |
|---|---|
| S1 Angles | Checks your archive for overlap and proposes 3–5 angles, each with an edge, a falsifiable thesis, one big idea, and the evidence you would need to supply. **H1** requires you to rate your own excitement (1–5) and state your edge in one sentence. |
| S2 Research | Splits the thesis into sub-questions, researches with `web_search` and `web_fetch`, then binds every finding to a URL, a verbatim quote, a speaker, an attribution type and an access path. Snippet-only, aggregator and AI-distilled sources are flagged as weak. |
| S3 Outline | A top-of-page brief (context, questions, one-sentence answer), one sentence per section with source ids, off-topic branches to cut, and a core image for promotion. |
| S4 Draft | Mode **A** (default): material cards only, you write. Mode **B**: the agent drafts from the approved outline and leaves `[TK]` for every experience, number or stance. Mode **I**: you talk, it organizes your transcript without adding content. |
| S5 Review | Deterministic lint (TK, banned words, AI-tell density, hedges, summary endings, intro length); a stranger re-read; usefulness and honesty checks; Harry Dry's sentence tests; CRIBS-style reader reactions; briars sampled three times; anchored anti-flattery scoring; SAFE-style claim-by-claim fact checking with verbatim quote re-fetch; and style drift against your archive. **H4** requires you to confirm how many quotes and numbers you re-checked by hand. |
| S6 Adapt | Platform-native variants with per-platform gates: X weighted length (CJK counts as 2), no link in the root post, no hashtags or mentions, no numbers that are absent from the final draft, a reply hook; threads with the link only in the last post; X Articles with a Proof → Promise → Plan opening; Medium packaging only for an English rewrite you wrote yourself. Every variant gets UTM parameters. |
| H5 Approve | Re-runs the checks on your edited text, records your edits as edit diffs, and writes a time-ordered `publish_kit.md` with copy-ready text and manual steps per platform. |
| S8 Learn | Read-only metrics (X public metrics via `GET /2/tweets`, manual or CSV entry for Substack and Medium), a channel report, and a monthly retro with top/bottom 20% patterns, recurring edits, proposals, short-to-long (R1) and evergreen-recycle (R2) candidates. Proposals are never applied automatically. |

## Install

Requires Python 3.10+ and an Anthropic API key.

```bash
git clone https://github.com/Eleven1111/creator-agent.git
```

```bash
cd creator-agent
```

```bash
pip install -e '.[dev,graph]'
```

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Optional local transcription for voice interviews (audio never leaves your machine):

```bash
pip install -e '.[voice]'
```

The default model is `claude-opus-5-5`; change it in your vault's `agent.yaml`.

## Use it from your agent app

**Claude Desktop, one click:** download `creator-agent-<version>.mcpb` from [Releases](https://github.com/Eleven1111/creator-agent/releases) (or run `ca build-mcpb`), double-click it, and pick a vault folder. Python and dependencies are installed by Claude Desktop via uv. The Anthropic API key is optional: without it the extension runs in **host-model mode**, where the Claude you are chatting with completes each model step and hands it back through `submit_model_output`, so it runs on your Claude plan instead of separate API billing.

For other apps, creator-agent runs as an **MCP server** and ships a portable **`SKILL.md`**, so you can drive it from Claude Desktop, ChatGPT, OpenClaw, Hermes Agent, WorkBuddy or any other MCP client instead of the terminal:

```bash
pip install -e '.[mcp]'
```

```bash
creator-agent-mcp --vault ~/creator-vault
```

```bash
ca install-skill openclaw
```

The server exposes 27 tools (status, every pipeline stage, gate approval, draft and variant editing, publish logging, metrics, audit) and no publishing or engagement tools. Gate approvals over MCP must carry the user's verbatim statement and are listed by `ca audit`. Per-app setup, HTTP mode with a token for ChatGPT, and the security model are in [docs/integrations.md](docs/integrations.md).

## Quick start

Create a vault (a folder of markdown and YAML that holds your voice, ideas and drafts):

```bash
ca init ~/creator-vault
```

```bash
export CA_VAULT=~/creator-vault
```

Fill in `voice/profile.yaml`, `never.md`, `stances.md`, `stories.md` and a few exemplars, add at least two good and two bad anchor posts under `evals/anchors/`, then import your back catalogue and add an idea:

```bash
ca import-rss https://yourname.substack.com/feed
```

```bash
ca idea add "Should small teams run customer interviews?" --edge "Everyone runs them per project; I suspect a fixed cadence matters more"
```

Run the whole pipeline with the LangGraph flow. It stops at each gate, tells you which file to read and how to continue, and persists progress in SQLite so you can resume tomorrow:

```bash
ca flow start idea_0001
```

```bash
ca flow resume <hub_id> --set angle=2 excitement=4 edge="..."
```

Or drive each stage yourself with `ca angles`, `ca research`, `ca outline`, `ca draft`, `ca review`, `ca adapt` and `ca approve <hub_id> H1…H5`. The two styles can be mixed: gates approved with `ca approve` are skipped by the flow.

The [tutorial](TUTORIAL.md) walks through every step from an empty machine to a monthly retro.

## Command overview

| Area | Commands |
|---|---|
| Setup | `init`, `import-rss`, `idea add/list`, `eval` |
| One piece, step by step | `new`, `angles`, `research`, `outline`, `draft`, `interview`, `review`, `adapt`, `approve`, `status`, `log-edit` |
| One piece, orchestrated | `flow start/resume/status` |
| Publishing (manual) | `kit`, `due`, `published` |
| Learning loop | `metrics add/pull-x/import`, `report`, `retro`, `retro-approve`, `promote`, `recycle`, `progress` |
| Extras | `survey design/analyze`, `blind prepare/score`, `audit` |
| Agent apps | `mcp` (same as `creator-agent-mcp`), `install-skill`, `build-mcpb` |

Run `ca <command> --help` for flags.

## Configuration

`agent.yaml` in your vault controls the model, effort per stage, the review pass threshold, fact checking and quote re-fetch, briar samples, style-drift sensitivity, and the research mode (`single` by default; `multi` runs parallel sub-agents at roughly 15× the tokens and should only be turned on once an offline test shows the single agent misses things).

`platforms/*.yaml` hold the platform rules the gates use, each with a `verified_at` date. Commands warn you when a rule file is older than 90 days, because these rules change often.

## What it deliberately does not do

- Call any platform write API, scheduler API or unofficial cookie-based endpoint.
- Reply, like, follow or quote on your behalf.
- Invent experiences, numbers, quotes or stances.
- Apply retro proposals to your voice profile without you.

`ca audit` checks published variants for manual publishing after H5 approval, no automated interaction, and platform rules verified within 90 days.

## Status

All phases P0–P4 of the handbook roadmap are implemented, plus the MCP server, the skill, the Claude Desktop extension and host-model mode. `pytest -q` runs 65 tests against a fake model client, a fake page fetcher and a fake Whisper module (LangGraph, SQLite and the MCP SDK, including a real stdio subprocess, are real). The extension launch was simulated with the same `uv run` command on Linux; the extension and the per-app configuration paths for ChatGPT, OpenClaw, Hermes and WorkBuddy have not been tested inside those apps. **It has not yet been run end to end against the live Anthropic API**, so watch the structured outputs of each stage on your first real run. Thresholds such as the review pass score, the style-drift sigma and the R1 "2× median" rule are handbook defaults and should be tuned on your own data.

## Development

```bash
pytest -q
```

## License

[MIT](LICENSE)
