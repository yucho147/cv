---
title: "ローカルからGoogle Earth Engineを使ってみる"
subtitle: ローカルからGoogle Earth Engineを使ってみる

# Summary for listings and search engines
summary: ローカルからGoogle Earth Engineを使ってみる

# Link this post with a project
projects: []

# Date published
date: 2024-06-18T23:42:44+09:00

# Date updated
lastmod: 2024-06-18T23:42:44+09:00

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: false

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  caption: ''
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin

tags:
- post
- 宇宙開発

categories:
- post
- 宇宙開発
---

本ページではGoogle Earth Engine(GEE)をローカルのpythonから利用してみます。

### 環境構築

pythonからGEEを用いるために `earthengine-api` をインストールしましょう

```bash
pip install earthengine-api
```

### GEEへのアクセス許可

Google Cloud上でGEEと紐づいているProjectにアクセスできるgoogleアカウントの認証をします。
[前ページ](../gee-setup/)で紐づけた `Project-ID` をあらかじめ用意しておいてください(前ページにおける `ee-yucho147` のことです)。

```python
import ee

project = "your_project_id"  # 前ページにおける `ee-yucho147`
ee.Authenticate()
ee.Initialize(project=project)
```

### 正常に稼働しているかのチェック

続けて

```python
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())
```

を実行し、

```python
NASADEM: NASA NASADEM Digital Elevation 30m
```

が出力された場合、正常にGEEと接続しており、情報が取得できています。

#### うまくいかないパターン

GEEとの接続初期化の際(`ee.Initialize`)に `Project-ID` をせずに実行する記事も多くみられます。
この場合にもブラウザでの認証を通して、対応するprojectと接続することができます。
一方、私などは複数のgoogleアカウントを併用しており、googleアカウントの切り替えがうまくいきませんでした(単純に私がGCPに慣れていないだけで、適切に切り替える方法はあると思います)。
このような場合には `Project-ID` を明示することで解消しました(とりあえずうまく動いた)。

お疲れ様でした。
