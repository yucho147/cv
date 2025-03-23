---
title: "streamlit cloudの初期設定"
subtitle: "streamlit cloudでappを公開するまでの覚書"

# Summary for listings and search engines
summary: "streamlit cloudでappを公開するまでの覚書"

# Link this post with a project
projects: []

# Date published
date: 2025-04-01T00:00:00+09:00

# Date updated
lastmod: 2024-04-01T00:00:00+09:00

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
- streamlit

categories:
- post
- streamlit
---

# はじめに
Streamlitは、PythonコードからインタラクティブなWebアプリケーションを手軽に構築できるオープンソースのフレームワークです。特にデータ分析や機械学習の分野において、分析結果やモデルを可視化し、関係者と共有する手段として有用です。

データサイエンティストは、モデルの構築や分析には精通していても、フロントエンドやWebシステムの実装には不慣れなことが少なくありません。Streamlitはそうした背景を踏まえて設計されており、HTMLやJavaScriptの知識がなくても、Pythonだけで直感的なUIを実装できます。さらに、アプリの構築からデプロイまでの流れも非常にシンプルで、試作ツールや社内向けダッシュボードの作成にも適しています。

業務とは別に、個人で作成したアプリケーションについても、Streamlit Community Cloud を使えば誰でも簡単に無料でインターネット上に公開することができ、自作のアイデアをすばやく世界に発信することが可能です。
そんなお遊びのアプリを作ったので、公開までの流れを記しておきます。

# Streamlit Community Cloudでのアプリの公開までの流れ
[公式ページ](https://streamlit.io/cloud)でも記載されていますが、下記の流れを踏むだけで公開できます。

1. GithubでSign up(Sign in)
2. リポジトリ、ブランチ、ファイルを選択する
3. 「デプロイ」をクリック

より詳細のチュートリアルは[こちら](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started)にあります。

## Streamlit Community Cloudのアカウントを作成
下記のページにアクセスし、アカウントを作成します。
https://share.streamlit.io/

![](/img/streamlit_cloud/step1.png)

Sign inの画面になりますが、Sign upのボタンもあるので、Sign upを通してアカウントを作成します。
![](/img/streamlit_cloud/step2.png)

いくつかのSign upの方法がありますが、どのみちGitHubのアカウントと連携するので、GitHubでSign upしてしまうことがスムーズで便利かと思います。
![](/img/streamlit_cloud/step3.png)

遷移先でStreamlitのアプリのコードがあるリポジトリを所有しているGitHubアカウントとAuthorize streamiltをします。あらかじめ指定している認証を問われるので、画面に従い紐付けを完了させてください。
![](/img/streamlit_cloud/step4.png)
![](/img/streamlit_cloud/step5.png)

適切にユーザー情報を入力してSet upを完了させましょう
![](/img/streamlit_cloud/step6.png)

アカウントの作成は完了です。

## アプリのデプロイ
あらかじめStreamlitの動くコードを用意しておき、リポジトリにpushしておきます。
今回デプロイするコードは[こちら](https://github.com/yucho147/bosu-police)になります。リポジトリはpublicリポジトリに設定しておいてください。おそらくpublicでないとStreamlit Community Cloudに公開できないかと思います(実験はしていない)。
Streamlitのコードの説明などは省略します。

前ステップで正しくSign upが完了しSign inが完了していると、[こちら](https://share.streamlit.io/)のリンクへアクセスするとご自身のアカウント画面に飛ぶと思います。
![](/img/streamlit_cloud/step7.png)
めちゃくちゃ主張強く「Create your first app now」と誘導されるので、「Create app」をクリックしデプロイに進んでみます。

![](/img/streamlit_cloud/step8.png)
今回はGitHubにあるコードを連携し、デプロイするので「Deploy a public app from GitHub」を選択します。

![](/img/streamlit_cloud/step9.png)
適切に必要な項目を入力していきます。GitHubと連携しているので、基本的にプルダウンメニューでリポジトリやファイルを選択することができます(便利)。
また、Advanced settingsからpythonのバージョンなども設定できます。
適切に項目を埋めたらDeployで終了です。

![](/img/streamlit_cloud/step10.png)
適切にデプロイできました👏

### 補足
追加設定をすることで、限定公開もできるようです。
![](/img/streamlit_cloud/step11.png)
試していないですが、招待したメールアドレスの人にだけ公開ができるんすかね。
当然のことですが、Streamlit Community Cloudにホスティングされているので、データなどは先方にも共有されるので、機密情報などはStreamlit Community Cloudを用いてホスティングしないよう気をつけてください。

お疲れ様でした。
