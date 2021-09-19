---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "有名なtwitterアカウントのtweetを社内チャットに投稿するアプリを作成"
subtitle: 社内の技術キャッチアップに対するハードルを下げたいっす

# Summary for listings and search engines
summary: 社内の技術キャッチアップに対するハードルを下げたいっす

# Link this post with a project
projects: []

# Date published
date: 2021-09-02T00:00:00+09:00

# Date updated
lastmod: 2021-09-02T00:00:00+09:00

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
- お知らせ

categories:
- お知らせ
---

## 概要
### 背景
- どうも論文を読むまでして技術のキャッチアップするということに対し、躊躇う気持ちを持っている人を見かける
- 技術キャッチアップをする時間がないとの意見をチラホラ
- そもそも論文や最新技術に対して気軽に意見を言い合う環境が整っていない希ガス
- 技術力を上げたいという人が存分に技術力を上げられる環境作りに少しでも貢献したい
- 上記の全ての事柄において改善に向かった世界は私にとっての楽しい世界である

### 実施内容
ロケチャの #curation_bot チャンネルにてネタを流し続けるbot的なアプリをひっそりデプロイしました。

論文のまとめとか、ライブラリの公式アカウントとか、有用そうなtwitterアカウントのtweetをひたすら投げ続けます。

ピックアップしたアカウントリスト: [ml_chatbot/user_list.yaml at main · yucho147/ml_chatbot](https://github.com/yucho147/ml_chatbot/blob/main/user_list.yaml) 

| app         | example fig                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------------|
| slack       | ![slack](https://raw.githubusercontent.com/yucho147/ml_chatbot/main/figs/slack_example.png)           |
| Rocket.Chat | ![rocketchat](https://raw.githubusercontent.com/yucho147/ml_chatbot/main/figs/rocketchat_example.png) |

↑twitterの書き込みが綺麗に表示されるようにattachmentsをパースしています。

### 利用方法
- ロケチャの #curation_bot チャンネルに参加して、自由に議論してください。
- チャンネル上でなくても構いませんので会話・議論のためのネタに使ってください。
- このチャンネルに議論のネタを投稿しても一向に構いません。
- 本チャンネルの個々の投稿の「リンクを取得」して他のチャンネルに投げるのも良い利用方法と思います。
- 本チャンネルの個々の投稿の「メッセージのフォロー」をすることで他の人の反応を見れます。
  - 未検証

とにかく目的は __**論文や最新技術に対する精神的ハードルを極限まで下げること**__ です。

### 実装内容
[GitHub - yucho147/ml_chatbot](https://github.com/yucho147/ml_chatbot) 

twitter APIを利用して特定のアカウントのtweetをStreamingします。

野良slackとrocketchatに同時に投げ続けます。

HEROKUの無料枠でデプロイしています。

### その他
#### 募集内容
rocketchatでもtwitterでもgithubにissue挙げてもなんでも良いので、興味があれば私にコンタクトを取ってください。
- 全て野良活動なので、一緒に開発したい人募集中。
- 「この人も入れた方が面白いよ」ってtwitterアカウントを募集中。
  - 多すぎても埋もれるだけなので、独断と偏見で判断します。
- その他改善案や要望募集中。
  - やる気になったらやります。

#### 課題
- なぜか私のrocketchatアカウントからだとaliasが使えず、私自身からの投稿になってしまう。
  - 権限の問題(?)
- rocketchatのattachmentsはスマホからだと綺麗に表示されない
  - rocketchatの問題(?)
- ディスカッションしやすい仕組みづくり
  - 1日1回「返信」のあった投稿を再度表示する仕組み
    - 優先度高めな課題
    - → おそらくRocket.Chatはできたと思う。
    - ~~(うまくいっていれば)毎日16:00に反応のあった投稿をピックアップして再投稿します。~~
    - ~~UTCからの時差を算数できないアホなので17:00になりました。~~
    - 16:00に投稿する仕組み戻しました
  - スタンプ押したユーザーにはその投稿に対して返信があった場合に通知するシステムとか考えられる(が、面倒でやっていない)
  - 「メッセージのフォロー」が想定する利用方法(?)
- twitter以外のサービス連携
  - qiitaとか個人ブログとか?
- そもそもこのチャンネル名が適しているか?
- そもそも数日で作ったコードのため汚い。

#### メッセージ
- 「Publish or Perish」とまでは言いませんが、学ばないと死にます。
  - [Learn or Die 死ぬ気で学べ　プリファードネットワークスの挑戦 - Google 検索](https://g.co/kgs/5a9S85)
- 社内でのインターナルな環境であればアホみたいなこと言っても問題ないと思います。むしろアホなことでも自由に発言することで意味があると思います。また精神的ハードルも全世界に発信するよりは低いと考えています。
-  キャッチアップするための時間がない方に関しては私にはどうしようもありません。一方その働き方が悪いのは明白です。上司に文句を言ってください。様々な機会を失っています。
- 上の実装をパクれば他の野良slackとかでも運用できます。実装上、わからないことがあれば私に聞いて下さい。
- 徐々にアウトプットをできるように進みましょう。
