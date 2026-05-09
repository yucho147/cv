# yucho147/cv — 個人サイト運用ガイド

Hugo + Wowchemy (HugoBlox) で構築した個人サイトです。
公開先: https://yuyakaneta.page

---

## ブログ記事の作り方

### 1. 記事フォルダを作成する

ブログ記事は `content/post/<記事スラッグ>/` ディレクトリで管理します。

```bash
# hugo コマンドで雛形を生成（archetypes/default.md が使われる）
hugo new content/post/<記事スラッグ>/index.md

# 例
hugo new content/post/vast-ai/index.md
```

または既存記事をコピーして編集しても構いません。

### 2. Front matter（メタデータ）の書き方

`index.md` の冒頭に以下のような Front matter を記述します：

```yaml
---
title: "記事タイトル"
subtitle: "サブタイトル（省略可）"
summary: "検索結果や一覧に表示される要約文"
projects: []
date: 2026-05-09T00:00:00+09:00      # 公開日
lastmod: 2026-05-09T00:00:00+09:00   # 最終更新日
draft: true        # 執筆中は true、公開時は false に変更
featured: false    # トップページの Featured に載せるか
image:
  caption: ''
  focal_point: ""
  placement: 2
  preview_only: false
authors:
- admin
tags:
- Post
categories:
- Post
---
```

`draft: false` にしないと本番サイトに公開されません。

### 3. スクリーンショット・画像の置き方

**このプロジェクトの慣例：`static/img/` 方式**

```
static/img/<記事スラッグ>/
  image_1.png
  image_2.png
```

記事内での参照：

```markdown
![説明テキスト](/img/<記事スラッグ>/image_1.png)
```

例（vast-ai記事の場合）：

```
static/img/vast-ai/
  sign-in.png
  billing.png
```

```markdown
![Vast.aiのConsole画面](/img/vast-ai/sign-in.png)
```

**Page Bundle方式（記事フォルダ内に直接置く）** も Hugo としては有効ですが、このプロジェクトでは `static/img/` 方式で統一しています。`featured.png`（サムネイル）だけは例外的に記事フォルダに置きます。

```
content/post/<記事スラッグ>/
  index.md
  featured.png   ← サムネイルのみここに置く
```

### 4. ローカルプレビュー

```bash
hugo server -D   # draft: true の記事も含めてプレビュー
```

ブラウザで http://localhost:1313 を開く。

### 5. 公開（デプロイ）

```bash
git add .
git commit -m "Add post: <記事タイトル>"
git push
```

GitHub Push 後、Netlify が自動ビルド・デプロイします。

---

## 他のコンテンツタイプの追加方法

ブログ記事（`post/`）と同様に、他のセクションも `content/<タイプ>/<スラッグ>/index.md` の構造で作成します。

### publication（論文・発表資料）

```bash
mkdir -p content/publication/<スラッグ>
```

```yaml
---
title: "論文タイトル"
authors:
- admin
publishDate: "2024-01-01T00:00:00Z"

# 種別: 0=未分類 1=会議論文 2=学術誌 3=プレプリント 4=レポート 5=本 6=本の一章 7=論文 8=特許
publication_types: ["1"]

publication: "掲載誌・会議名"
abstract: "要旨"
featured: false
projects: []   # 紐付けるプロジェクトのスラッグ
slides: ""
---
```

- PDFを同フォルダに置き、`links:` で参照できる（例：`url: 'publication/<スラッグ>/paper.pdf'`）
- 引用用 BibTeX は `cite.bib` という名前で同フォルダに置く

### event（発表・講演）

```bash
mkdir -p content/event/<スラッグ>
```

```yaml
---
title: "発表タイトル"
event: "イベント名"
event_url: "https://example.com/event"
location: "開催場所"
summary: "一言要約"
abstract: "発表概要"
date: "2026-03-05T18:30:00+09:00"
date_end: "2026-03-05T21:40:00+09:00"
all_day: false
publishDate: "2026-01-01T00:00:00Z"
authors: []
tags: []
featured: false
image:
  caption: ''
  focal_point: Right
links: []       # 資料URLなどを列挙
slides: ""
projects: []
---
```

- スライドURL等は `links:` に `- name: Slides\n  url: https://...` の形式で追記

### project（プロジェクト紹介）

```bash
mkdir -p content/project/<スラッグ>
```

```yaml
---
title: "プロジェクト名"
summary: "概要説明"
tags: []
date: "2025-01-01T00:00:00Z"
image:
  caption: ""
  focal_point: Smart
links: []   # 外部URL等
---

本文をここに書く（Markdown）
```

- 外部URLをリンクとして出すだけなら本文なしでも可

### 各タイプの比較

| タイプ | ディレクトリ | 主な用途 | 画像 |
|--------|-------------|----------|------|
| post | `content/post/` | ブログ記事・技術記事 | Page Bundle 推奨 |
| publication | `content/publication/` | 論文・arXiv・学会誌 | PDF + cite.bib を同梱 |
| event | `content/event/` | 発表・講演・登壇 | featured.png をサムネに |
| project | `content/project/` | OSS・ツール紹介 | featured.png をサムネに |

---

## ディレクトリ構成

```
content/
  post/          # ブログ記事
  publication/   # 論文・発表資料
  event/         # 登壇・講演
  project/       # プロジェクト紹介
  authors/       # 著者プロフィール（通常は編集不要）
static/
  img/           # 旧来の画像置き場（static配信）
archetypes/
  default.md     # hugo new で使われる雛形
config/
  _default/      # Hugo 設定ファイル
```

---

## 参考リンク

- [HugoBlox (旧 Wowchemy) ドキュメント](https://docs.hugoblox.com/)
- [Hugo ドキュメント](https://gohugo.io/documentation/)

---

## Original Template

Academic Template for [Hugo](https://github.com/gohugoio/hugo)

## Crowd-funded open-source software

To help us develop this template and software sustainably under the MIT license, we ask all individuals and businesses that use it to help support its ongoing maintenance and development via sponsorship.

### [❤️ Click here to unlock rewards with sponsorship](https://wowchemy.com/plans/)

## Ecosystem

* **[Hugo Academic CLI](https://github.com/wowchemy/hugo-academic-cli):** Automatically import publications from BibTeX

[![Screenshot](https://raw.githubusercontent.com/wowchemy/wowchemy-hugo-modules/master/academic.png)](https://wowchemy.com)

## Demo image credits

- [Open book](https://unsplash.com/photos/J4kK8b9Fgj8)
- [Course](https://unsplash.com/photos/JKUTrJ4vK00)

[![Analytics](https://ga-beacon.appspot.com/UA-78646709-2/starter-academic/readme?pixel)](https://github.com/igrigorik/ga-beacon)
