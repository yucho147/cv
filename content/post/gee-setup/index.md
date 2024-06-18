---
title: "Google Earth Engine(GEE)のセットアップ"
subtitle: "Google Earth Engine(GEE)の初期設定"
summary: "Google Earth Engine(GEE)の初期設定"
projects: []
date: 2024-06-17T14:13:16+09:00
lastmod: 2024-06-17T14:13:16+09:00

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
- Post
- 宇宙開発

categories:
- Post
- 宇宙開発
---

本ページではGoogle Earth Engine(GEE)の初期設定とアカウントの登録を完了し、GEEを使える状態にします。

### Google Earth Engineにアクセス

まずは [Google Earth Engine](https://earthengine.google.com/) のWebページにアクセスします。
さらに赤枠で囲った `Get Started` をクリックします

![](/img/gee-setup/image_1.png)

次にGEEに登録するgoogleアカウントを選択します。

![](/img/gee-setup/image_2.png)

選択したgoogleアカウントへのログインを促されます。

![](/img/gee-setup/image_3.png)

### Google Cloud projectを作成
`Register a Noncommercial or Commercial Cloud project` を選択し、Google Earth Engine用のプロジェクトを作成します。

![](/img/gee-setup/image_4.png)

続いて、商用利用(Paid usage)または非商用利用(Unpaid usage)を目的に応じ選んで下さい。
今回は非商用利用を選択し、Project typeを指定します。
利用用途に応じて選択いただけると良いかと思います。今回は個人利用のため `No affiliation` を選択しました。

![](/img/gee-setup/image_5.png)

続く画面ではGoogle Cloudのプロジェクトを新規で作成するか、既存のプロジェクトと紐付けます。

今回は新規でプロジェクトを作成し、そのプロジェクトと紐づける形でGEEを利用しようと思います。 `Create a new Google Cloud Project` を選び、 `Project-ID` に任意のIDを入力して下さい(デフォルトで `ee-{googleアカウント名}` が入力されました)。
`Project Name` (任意)も入力しておきましょう(同様にデフォルトで画像のように `Earth Engine Default Project` が入力されました)。
自分はあらかじめGoogle Cloud Platform(GCP)の利用規約に同意をしていたので、 `CONTINUE TO SUMMARY` で次に進無ことができますが、GCPの利用規約に同意していない場合は、エラーが出るらしいです。
指示に従い利用規約に同意いただければと思います。

![](/img/gee-setup/image_6.png)

続く最終確認画面で、ここまでに入力した内容の確認がされます。
問題ないようでしたら、 `CONFIRM AND CONTINUE` をクリックです。
![](/img/gee-setup/image_7.png)

### Google Earth Engineへのアカウント登録完了
問題なく進めると前画面から数秒後、続く画面が表示されGEEが利用できるようになります。

![](/img/gee-setup/image_8.png)

お疲れ様でした。
