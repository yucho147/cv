---
title: "KaggleコンペやPoC調査をCoding Agentと進めるためのワークフローテンプレートを作った"
subtitle: "AI-DLC的な対話フローで、情報収集から実装開始まで繋げる"

# Summary for listings and search engines
summary: "Kaggle CLI v2でDiscussionも取得できるようになったことを機に、コンペ参加・上位解法調査・業務PoCを Coding Agent と進めるための GitHub Template Repository を作った話。"

# Link this post with a project
projects: []

# Date published
date: 2026-05-31T00:00:00+09:00

# Date updated
lastmod: 2026-05-31T00:00:00+09:00

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: false

# Featured image
image:
  caption: ''
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin

tags:
- Post
- Kaggle
- MCP
- GitHub Copilot
- Claude
- AI-DLC

categories:
- Post
---

## はじめに

[Kaggle CLI がバージョン2系にアップデート](https://github.com/Kaggle/kaggle-cli)され、Competition / Dataset / Notebook に加えて Discussion の内容も CLI から取得できるようになりました。

```bash
# トピック一覧の取得
kaggle competitions topics list -c titanic

# トピック本文とコメントツリーの取得
kaggle competitions topics show <TOPIC_REF>
```

これにより、Discussion や Notebook の内容を Coding Agent から直接参照して、コンペ参加の初動や上位解法の調査を自動化できる可能性が出てきました。

同時に、GitHub Copilot CLI や Claude Code などの Coding Agent が実用的になってきたこともあり、情報収集から baseline 実装方針の決定まで、対話形式で進められるテンプレートを作ってみました。

- リポジトリ: https://github.com/yucho147/kaggle-ai-dlc-workflow-template

## 作った動機

コンペや調査ってケースバイケースなことが非常に多く、一般化しにくいと思っています。

新しいコンペに参加するたびに、「評価指標は何か」「データの構造はどうなっているか」「Discussionでどんな知見が共有されているか」といった情報収集から始めることになります。この初動部分はある程度パターン化できるはずなのに、毎回ゼロから始めているのがもったいないと感じていました。

また、調査内容がドキュメントとして残らないことも課題でした。調査で得た知見が個人の頭の中にしかなく、後から参照できなかったり、チームで共有しにくかったりします。

そこで、AI DLC（AI Deep Learning Cycle）の考え方を参考に、対話形式で docs を埋めていきながら、設計が揃ったら実装に入るという流れを作りました。

## どんな場面で使えるか

以下の5つの用途を想定しています。

| 用途 | 使う場面 |
| --- | --- |
| `competition-starter` | 新しい Kaggle コンペに参加するとき |
| `competition-winning` | Discussion / Notebook から上位解法を調べるとき |
| `technical-research` | 業務 PoC・技術調査を整理して実装まで持っていきたいとき |
| `implementation-only` | 既に方針が固まっていて実装だけ進めたいとき |
| `knowledge-reuse` | 過去の調査・コンペ知見を再利用可能な形に整理するとき |

**competition-starter**

`kaggle-starter` スキルを使うと、コンペ概要・評価指標・データ構造の整理から、baseline と validation の方針決定まで Agent が docs を埋めてくれます。

**competition-winning**

`kaggle-winning-research` スキルを使うと、Discussion や Notebook から CV設計・特徴量・モデル・アンサンブルといった勝ち筋を抽出して整理します。LB shakeup リスクや失敗例、再利用できる実装候補の整理まで行います。

**technical-research**

`technical-research` スキルを使うと、問題設定・既存手法・論文・GitHub実装・適用リスク・PoC スコープの整理から、baseline 実装計画まで構造化します。Kaggle MCP で類似コンペの Discussion / Notebook を参照して、関連知見を手法比較に活かす手順も含まれています。

## 使い方

このリポジトリは GitHub Template Repository として公開しています。

### 1. リポジトリを作成する

GitHub の **「Use this template」** ボタンから、プロジェクトごとに新しいリポジトリを作成します。テンプレートリポジトリ自体を直接の作業場として使わず、プロジェクトごとに別リポジトリを作るのが想定の使い方です。

### 2. セットアップ

```bash
git clone https://github.com/<your-org>/<your-project>.git
cd <your-project>
uv sync
```

依存関係の管理には `uv` を使っています。`aidlc-docs/` はプレースホルダーが入った状態で含まれており、初期化スクリプトの実行は不要です。

### 3. Coding Agent を起動して話しかける

GitHub Copilot CLI、Claude Code、Codex などの Coding Agent を起動して、やりたいことを日本語で話しかけるだけです。

```
titanic コンペの参加準備をしたい
異常検知の PoC を始めたい
```

迷ったときのために `docs/03_prompt_templates.md` に用途別の日本語プロンプト集を用意しています。起動直後に貼り付けて使う「共通開始プロンプト」もここにまとめています。

Agent が `aidlc-docs/` 配下のドキュメントを埋めながら、設計が揃ったら実装に入る流れになっています。

## スキルの仕組み

このテンプレートには `.agents/skills/` 配下に3つのスキルが定義されています。

| スキル | 用途 |
| --- | --- |
| `kaggle-starter` | 新規コンペ参加時の初動整理 |
| `kaggle-winning-research` | Discussion / Notebook からの勝ち筋調査 |
| `technical-research` | 業務PoC・技術調査の構造化と実装計画 |

各スキルは `SKILL.md` に手順・入力・出力・完了条件が記述されており、Coding Agent がこれを読んで実行します。スキルを明示的に呼び出すこともできますし、ユーザーの入力内容から Agent が適切なスキルを選んで動くことも想定しています。

## MCP サーバー

`.mcp.json` にデフォルトで3つの MCP サーバーが設定されています。

| サーバー | 用途 |
| --- | --- |
| `kaggle` | Competition / Discussion / Notebook / Dataset 取得 |
| `arxiv` | 論文検索・取得 |
| `huggingface` | モデル・Dataset・Spaces 検索 |

### Claude Code

プロジェクトルートの `.mcp.json` が自動で読み込まれます。追加設定は不要です。

### GitHub Copilot CLI

Copilot CLI はプロジェクトレベルの設定ファイルに対応していないため、ユーザーレベルの設定ファイルに追記が必要です。

```bash
~/.copilot/mcp-config.json
```

```json
{
  "mcpServers": {
    "kaggle": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--group", "mcp", "python", "<project-root>/tools/kaggle-mcp/server.py"],
      "tools": ["*"]
    },
    "arxiv": {
      "type": "stdio",
      "command": "uvx",
      "args": ["arxiv-mcp-server"],
      "tools": ["*"]
    },
    "huggingface": {
      "type": "http",
      "url": "https://huggingface.co/mcp",
      "tools": ["*"]
    }
  }
}
```

`<project-root>` はリポジトリの絶対パスに置き換えてください。詳しいセットアップ手順は `docs/05_mcp_setup.md` を参照してください。

### Kaggle MCP サーバーについて

Kaggle の MCP サーバーは `tools/kaggle-mcp/server.py` にカスタム実装しています。Kaggle CLI をそのまま Agent に叩かせるのではなく、MCP tool 経由で抽象化することで、training code や feature code が CLI に直接依存しない構造にしています。

主なツールは以下のとおりです。

| Tool | 用途 |
| --- | --- |
| `kaggle_competitions_list` | 類似コンペの検索 |
| `kaggle_competition_overview` | コンペ概要・メタデータ取得 |
| `kaggle_competition_files` | データファイル一覧 |
| `kaggle_competition_download` | データダウンロード |
| `kaggle_discussions_list` | Discussion トピック一覧 |
| `kaggle_discussion_get` | Discussion 本文・コメント取得 |
| `kaggle_notebooks_search` | Notebook 検索 |
| `kaggle_notebook_pull` | Notebook ソース取得 |
| `kaggle_datasets_list` | Dataset 検索 |
| `kaggle_dataset_download` | Dataset ダウンロード |
| `kaggle_submissions_list` | 提出履歴取得 |

MCP が使えない場合は CLI adapter fallback として `uv run kaggle ...` を使います。

```bash
# MCP が使えない場合のフォールバック
uv run scripts/download_kaggle_competition.sh titanic
```

## AI-DLC的なワークフロー

### aidlc-docs の構造

`aidlc-docs/` はプロジェクト固有のドキュメントを書く場所で、3つのフェーズに分かれています。

```text
aidlc-docs/
├── audit.md                         # 外部情報源・実行コマンド・判断の記録
├── inception/                       # 問題理解・調査フェーズ
│   ├── problem-overview.md
│   ├── kaggle-starter.md
│   ├── winning-research.md
│   ├── technical-research.md
│   ├── risk-assessment.md
│   └── strategy.md
├── construction/                    # 設計・実装フェーズ
│   ├── implementation-questionnaire.md
│   ├── architecture.md
│   ├── experiment-plan.md
│   ├── code-generation-plan.md
│   ├── implementation-candidates.md
│   ├── kaggle-data-access.md
│   └── build-and-test/
└── operations/                      # 実験・運用フェーズ
    ├── experiment-log.md
    ├── cv-lb-tracking.md
    ├── lessons-learned.md
    └── reusable-patterns.md
```

外部情報を調査した場合は、取得元・実行コマンド・日時・判断を `audit.md` に記録することをルールにしています。後から「なぜこの手法を採用したか」が追えるようにするためです。

### 実装開始条件

実装開始の前に、少なくとも以下のドキュメントが揃うことを条件にしています。

- `aidlc-docs/inception/problem-overview.md`
- `aidlc-docs/construction/experiment-plan.md` または `code-generation-plan.md`
- 新規コードを生成する場合は `aidlc-docs/construction/implementation-questionnaire.md` と `architecture.md`

ドキュメントが揃う前に実装に走らないよう、`AGENTS.md` / `COPILOT.md` / `CLAUDE.md` のインストラクションで Agent に制御をかけています。

### 新規コードの標準構成

既存コードの制約がない場合、新規 baseline は以下を標準にしています。

- 設定管理: Hydra
- Logging: loguru
- 実験管理: MLflow
- Kaggle access: MCP / Gateway 優先、CLI は adapter fallback
- Notebook: EDA / orchestration として使い、core logic は `src` から import

## おわりに

調査フェーズから実装フェーズへの橋渡し部分を、Coding Agent との対話で埋めていくという試みです。コンペや調査はケースバイケースなことが多いので完全な自動化は難しいですが、決まったパターンの部分を Agent に任せることで、本質的な判断に集中しやすくなると思っています。

「Use this template」で新しいリポジトリを作って、Agent にやりたいことを話しかけるだけで試せます。ぜひ使ってみてください。

- リポジトリ: https://github.com/yucho147/kaggle-ai-dlc-workflow-template
