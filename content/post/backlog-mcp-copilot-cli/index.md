---
title: "GitHub Copilot CLIにBacklog MCPを登録する"
subtitle: "backlog-mcp-serverをnpxで動かしてCopilot CLIと接続する"

# Summary for listings and search engines
summary: "GitHub Copilot CLIにBacklog MCP Serverを登録することで、チャットから自然言語でBacklogを操作できるようにする手順をまとめます。"

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
- Backlog
- MCP
- GitHub Copilot
- CLI

categories:
- Post
---

## はじめに

GitHub Copilot CLI に [Backlog MCP Server](https://github.com/nulab/backlog-mcp-server) を登録すると、チャットから自然言語でBacklogの課題・プロジェクト・Wikiなどを操作できるようになります。

「課題を検索して」「コメントを追加して」といった会話でBacklogの操作が完結するので、ブラウザを開く手間がなくなります。

本記事では、`npx` を使って手軽に登録する手順をまとめます。

## 前提条件

- GitHub Copilot CLI がインストール済み（`copilot` コマンドが使えること）
- Node.js / npm がインストール済み（`npx` コマンドが使えること）
- BacklogのAPIキーを取得済み

### BacklogのAPIキー取得方法

1. Backlogにログイン
2. 右上のアイコン → **個人設定** を開く
3. **API** タブ → メモを入力して **登録** をクリック
4. 発行されたAPIキーをコピーして控えておく

## 設定手順

登録方法は3つあります。**方法1のインタラクティブ操作が一番わかりやすい**のでおすすめです。

### 方法1：`/mcp add` でインタラクティブに登録（おすすめ）

#### 1. ターミナルで Copilot CLI を起動

```bash
copilot
```

#### 2. 対話画面で `/mcp add` を入力

起動後のチャット画面で以下を入力します：

```
/mcp add
```

#### 3. フォームに入力する

フォームが表示されるので、以下のように入力します：

| 項目 | 入力値 |
| --- | --- |
| Server Name | `backlog` |
| Server Type | `STDIO`（ローカルプロセスを起動して通信する方式） |
| Command | `npx -y backlog-mcp-server` |
| Environment Variables | 下記のJSON |
| Tools | `*`（すべて許可） |

**Environment Variables** には以下のJSONを入力します：

```json
{
  "BACKLOG_DOMAIN": "your-domain.backlog.jp",
  "BACKLOG_API_KEY": "your-api-key",
  "ENABLE_TOOLSETS": "space,project,issue,wiki,document",
  "OPTIMIZE_RESPONSE": "1",
  "MAX_TOKENS": "10000",
  "PREFIX": "backlog_"
}
```

`BACKLOG_DOMAIN` と `BACKLOG_API_KEY` は自分のものに置き換えてください。

#### 4. `Ctrl + S` で保存

保存すると CLI を再起動しなくてもすぐ使えるようになります。
設定内容は `~/.copilot/mcp-config.json` に書き込まれます。

---

### 方法2：コマンドで一括登録

フォームを使わず、ターミナルから1コマンドで登録する方法です：

```bash
copilot mcp add backlog \
  --env BACKLOG_DOMAIN=your-domain.backlog.jp \
  --env BACKLOG_API_KEY=your-api-key \
  --env ENABLE_TOOLSETS=space,project,issue,wiki,document \
  --env OPTIMIZE_RESPONSE=1 \
  --env MAX_TOKENS=10000 \
  --env PREFIX=backlog_ \
  -- npx -y backlog-mcp-server
```

>  APIキーがシェルの履歴に残ります。気になる場合は方法1か方法3を使ってください。

---

### 方法3：設定ファイルを直接編集

`~/.copilot/mcp-config.json` を直接編集する方法です：

```json
{
  "mcpServers": {
    "backlog": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "backlog-mcp-server"],
      "env": {
        "BACKLOG_DOMAIN": "your-domain.backlog.jp",
        "BACKLOG_API_KEY": "your-api-key",
        "ENABLE_TOOLSETS": "space,project,issue,wiki,document",
        "OPTIMIZE_RESPONSE": "1",
        "MAX_TOKENS": "10000",
        "PREFIX": "backlog_"
      }
    }
  }
}
```

---

### 登録の確認・管理

```bash
# 登録済みのMCPサーバー一覧を確認
copilot mcp list

# 設定内容を確認
copilot mcp get backlog

# 削除したいとき
copilot mcp remove backlog
```

## 動作確認

Copilot CLI を起動して、以下のように話しかけてみましょう：

```
Backlogのプロジェクト一覧を教えて
```

プロジェクト一覧が返ってきたら設定完了です

## 設定パラメータの説明

| 環境変数 | 説明 |
| --- | --- |
| `BACKLOG_DOMAIN` | BacklogのスペースURL（例：`yourteam.backlog.jp`） |
| `BACKLOG_API_KEY` | BacklogのAPIキー |
| `ENABLE_TOOLSETS` | 有効にするツールセット（カンマ区切り） |
| `OPTIMIZE_RESPONSE` | `1` にするとレスポンスを最適化（推奨） |
| `MAX_TOKENS` | レスポンスの最大トークン数（デフォルト50,000） |
| `PREFIX` | ツール名のプレフィックス（他MCPとの名前衝突回避） |

`ENABLE_TOOLSETS` には使うものだけ指定すると、AIに渡すツール数が減って動作が安定します。利用可能なツールセットは以下の通りです：

| ツールセット | 内容 |
| --- | --- |
| `space` | スペース情報の取得 |
| `project` | プロジェクト管理（他ツールが依存するため推奨） |
| `issue` | 課題・コメント・マイルストーン管理 |
| `wiki` | Wikiページ管理 |
| `git` | Gitリポジトリ・PRの管理 |
| `notifications` | 通知管理 |
| `document` | ドキュメント閲覧 |

## 使用例

設定が完了するとこんな感じで使えます：

```
# プロジェクト一覧を見る
Backlogのプロジェクト一覧を表示して

# 課題を作成する
〇〇プロジェクトに「△△の調査」という課題を作成して

# 自分の課題を確認する
自分にアサインされている未完了の課題を一覧表示して

# コメントを追加する
PROJ-123に「対応完了しました」とコメントして
```

チャットから課題の作成・更新・検索が一通りできるので、日々の進捗管理がだいぶ楽になります。

## 参考リンク

- [backlog-mcp-server GitHub（日本語README）](https://github.com/nulab/backlog-mcp-server/blob/main/README.ja.md)
- [BacklogのAPIキー管理](https://support-ja.backlog.com/hc/ja/articles/360035641754)
