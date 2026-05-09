---
title: "Vast.aiでGPUを借りてCLIからSSH接続するまで"
subtitle:

# Summary for listings and search engines
summary: "Vast.aiでGPUインスタンスを借りて、CLIからSSH接続するまでの手順を紹介します。"

# Link this post with a project
projects: []

# Date published
date: 2026-05-09T22:55:39+09:00

# Date updated
lastmod: 2026-05-09T22:55:39+09:00

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
- Vast.ai
- GPU
- SSH
- uv
- CLI

categories:
- Post
---

## はじめに

GPUを使う機械学習やKaggleの実験をしたいとき、手元にGPUマシンがないと少し困ります。

[Vast.ai](https://vast.ai/) を使うと、GPU付きのインスタンスを時間単位で借りられます。
本ページでは、Vast.aiにsign inしてから、CLIでGPUインスタンスを作成し、SSHでログインして、最後に `nvidia-smi` でGPUが見えるところまでをまとめます。
Python環境は `uv` を使います。

前提として、ローカルPCで `uv` と `ssh` が使える状態を想定します。`uv` が未インストールの場合は先にインストールしておいてください。

## Vast.aiにsign inする

まず、[Vast.ai Console](https://cloud.vast.ai/) にアクセスしてsign inします。
Google / GitHub / メールアドレスなどでアカウントを作成して、Consoleに入れることを確認しておいてください。

![Vast.aiのConsoleダッシュボード](/img/vast-ai/dashboard.png)

右上のLoginボタンを押せば、アカウントの作成画面になりました。

![Vast.aiのSign in画面](/img/vast-ai/sign-in.png)

Googleアカウントで登録した場合も、メールアドレス確認のメールが届くので、リンクをクリックして認証を済ませておきます。

![メール認証メール](/img/vast-ai/email-verification.png)

## Billingからクレジットを追加する

GPUインスタンスを作成するには、事前にクレジットを追加する必要があります。
BillingページはConsole左上のハンバーガーメニュー（☰）から「Billing」を選択すると移動できます。

![Vast.aiのBilling画面](/img/vast-ai/billing.png)

支払い方法はクレジットカードを登録して自動請求にする方法と、「Add credit」から都度クレジットを追加する方法があります。
自動請求が気になる場合は、「Add credit」から使いたい分だけ先払いしておく方が安心です。
お試しであれば $5 程度で十分です（RTX 4090 は安いもので $0.3〜0.5/時間程度なので、接続確認だけなら $1 も使いません）。
なお、クレジットカードを登録していない場合、残高がなくなってもインスタンスが自動削除されないことがあるようです。使い終わったら必ず手動で削除しましょう。

一点注意したいのは、インスタンスを「停止」しただけではディスク料金が残る場合があることです。
使い終わったインスタンスは、不要なら削除するようにしましょう。

## uvでVast.ai CLIをインストールする

Vast.aiはCLIから操作できます。ここではグローバルに `pip install` するのではなく、`uv` を使います。

CLIをその場で実行するだけなら、`uvx` が一番手軽です。

```bash
uvx vastai --help
```

毎回 `uvx vastai ...` と打てば、仮想環境を意識せずにVast.ai CLIを実行できます。以降のコマンドはすべて `uvx vastai` で実行します。

もしプロジェクトディレクトリ内に明示的に環境を作りたい場合は以下のようにしてもよく、この場合は `uv run vastai ...` として実行することになります。

```bash
uv init
uv add vastai
uv run vastai --help
```

## API keyを発行・設定する

CLIからVast.aiを操作するにはAPI keyが必要です。ConsoleのハンバーガーメニューからBillingと並列に「Keys」があるので選択します。「Manage Keys」ページの「API Keys」タブを開き、API keyを新規作成します。作成したAPI keyは後で再表示できない場合があるので、作成直後にコピーしておきましょう。

![Vast.aiのAPI key作成画面](/img/vast-ai/api-key.png)

作成ダイアログではNameと権限設定が求められますが、CLIからインスタンスを操作するだけであればStandardのデフォルト設定のままで問題ありません。

コピーしたAPI keyをCLIに設定します。

```bash
uvx vastai set api-key YOUR_API_KEY
```

ファイルに保存してある場合は以下のように読み込むこともできます。

```bash
uvx vastai set api-key $(cat ~/vast-ai_apikey.txt)
```

設定したAPI keyは `~/.config/vastai/vast_api_key` に平文で保存されます。以降の `uvx vastai` コマンドはここから自動的に読み込まれます。

認証できているか確認します。ユーザーID、メールアドレス、残高などが表示されればOKです。

```bash
uvx vastai show user
```

![uvx vastai show userの実行結果](/img/vast-ai/show-user.png)

API keyはパスワードと同じように扱ってください。GitHubにコミットしたり、ブログに貼ったりしないように注意です。

## SSH keyを作ってVast.aiに登録する

次に、インスタンスへSSH接続するためのSSH keyを作ります。
既存の `~/.ssh/id_ed25519` を使ってもよいですが、Vast.ai用の鍵だと分かるようにファイル名を明示しておくと後々管理が楽です。

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_vastai -C "vastai"
```

`.pub` が付いた公開鍵をVast.aiに登録します。秘密鍵（`.pub` なし）は他人に渡してはいけません。

```bash
uvx vastai create ssh-key "$(cat ~/.ssh/id_ed25519_vastai.pub)"
```

ファイルパスをそのまま渡すと、パスが文字列として登録されてしまうことがあります。`$(cat ...)` で中身を展開して渡すのが確実です。

**SSH keyはインスタンスを作成する前に登録しておくのが重要です。**
インスタンス作成後にSSH keyを追加しても、すでに作成済みのインスタンスには反映されない場合があります。

## GPUインスタンスを検索する

借りたいGPUインスタンスを検索します。ここではRTX 4090を1枚使うインスタンスを探してみます。

```bash
uvx vastai search offers 'gpu_name=RTX_4090 num_gpus=1 verified=true direct_port_count>=1 rentable=true' -o 'dlperf_usd-'
```

条件の意味は以下の通りです。

| 条件                     | 意味                                           |
| ---------------------- | -------------------------------------------- |
| `gpu_name=RTX_4090`    | RTX 4090を対象にする                               |
| `num_gpus=1`           | GPU 1枚のインスタンスを探す                             |
| `verified=true`        | verifiedなマシンを対象にする                           |
| `direct_port_count>=1` | direct SSHに使えるportがあるものを対象にする                |
| `rentable=true`        | 現在レンタル可能なものを対象にする                            |
| `-o 'dlperf_usd-'`     | deep learning performance per dollarが良い順に並べる |

検索結果には、offerごとの `ID` が表示されます。インスタンス作成時にこの `ID` を使います。

![vastai search offersの実行結果](/img/vast-ai/search-offers.png)

条件が厳しすぎて何も出ない場合は、GPU名を変えるか指定を外してみてください。

```bash
uvx vastai search offers 'num_gpus=1 verified=true direct_port_count>=1 rentable=true' -o 'dlperf_usd-'
```

## GPUインスタンスを作成する

使いたいofferの `ID` が決まったら、インスタンスを作成します。`OFFER_ID` を検索結果のIDに置き換えて実行します。

```bash
uvx vastai create instance OFFER_ID \
  --image nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 \
  --disk 20 \
  --onstart-cmd "nvidia-smi" \
  --ssh
```

各オプションの意味は以下の通りです。

| オプション           | 意味                         |
| --------------- | -------------------------- |
| `--image`       | 起動するDocker image           |
| `--disk 20`     | ディスク容量を20GBにする             |
| `--onstart-cmd` | インスタンス起動時に実行するコマンド         |
| `--ssh`         | SSH接続用のインスタンスとして起動する       |

作成に成功すると以下のようなレスポンスが返ります。`new_contract` の値がインスタンスIDです。

```json
{"success": true, "new_contract": 12345678}
```

以降で使うので、シェル変数に入れておくと便利です。

```bash
INSTANCE_ID=12345678
```

## インスタンスの起動を待つ

作成直後はDocker imageのpullや起動処理中なので、少し待ちます。

```bash
uvx vastai show instance $INSTANCE_ID
```

`Status` が `running` になれば接続できる状態です。いつまでも `running` にならない場合は、別のofferで作り直した方が早いこともあります。

出力はテーブル形式で、確認すべき主なカラムは以下の通りです。

| カラム | 意味 |
| ----------- | ----------------------------------- |
| `Status`    | インスタンスの状態。`running` になったら接続可能 |
| `Model`     | GPUの種類。注文通りのGPUか確認する |
| `SSH Addr`  | SSH接続先のホスト名 |
| `SSH Port`  | SSH接続先のポート番号 |
| `$/hr`      | 時間あたりのコスト |

![show instanceでrunningになった状態](/img/vast-ai/instance-running.png)

## SSH接続する

`running` になったら、SSH接続用の情報を取得します。

```bash
uvx vastai ssh-url $INSTANCE_ID
```

以下のような形式で表示されます。

```bash
ssh://root@sshX.vast.ai:XXXXX
```

`-i` オプションで秘密鍵を指定して接続します（`sshX.vast.ai` と `XXXXX` は実際の値に置き換えてください）。

```bash
ssh -i ~/.ssh/id_ed25519_vastai root@sshX.vast.ai -p XXXXX
```

接続すると、Vast.aiのコンテナはデフォルトでtmuxが自動起動します。`ctrl+b` → `d` でtmuxをデタッチ（プロセスを残したまま切断）できます。

毎回 `-i` や `-p` を指定するのが面倒なら、`~/.ssh/config` に登録しておくと便利です。

```sshconfig
Host vastai-gpu
  HostName sshX.vast.ai
  User root
  Port XXXXX
  IdentityFile ~/.ssh/id_ed25519_vastai
  IdentitiesOnly yes
```

こうしておけば `ssh vastai-gpu` だけで接続できます。なお、インスタンスを作り直すたびにHostNameとPortは変わるので、その都度更新が必要です。

## nvidia-smiでGPUを確認する

SSH接続できたら、GPUが見えているか確認します。

```bash
nvidia-smi
```

GPU名、Driver Version、CUDA Versionなどが表示されればOKです。

![nvidia-smiの実行結果](/img/vast-ai/nvidia-smi.png)

PyTorch入りのimageを使っている場合は、以下でPythonからも確認できます。

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

## ファイルの転送

ローカルからインスタンスにファイルを送りたい場合は `vastai copy` が使えます。

```bash
# ローカル → インスタンス
uvx vastai copy local:./data/ $INSTANCE_ID:/workspace/data/

# インスタンス → ローカル
uvx vastai copy $INSTANCE_ID:/workspace/results/ local:./results/
```

SSH configを設定していれば、通常の `scp` でも問題ありません。

```bash
scp ./train.py vastai-gpu:/workspace/train.py
scp -r vastai-gpu:/workspace/results ./results
```

## 使い終わったらインスタンスを削除する

作業が終わったら忘れずにインスタンスを削除します。
停止中でもディスク料金が残る場合があるので、不要なインスタンスは `destroy` するのが安全です。

```bash
uvx vastai destroy instance $INSTANCE_ID
```

## よく使うコマンドまとめ

### API key設定・確認

```bash
uvx vastai set api-key YOUR_API_KEY
uvx vastai show user
```

### SSH key作成・登録

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_vastai -C "vastai"
uvx vastai create ssh-key "$(cat ~/.ssh/id_ed25519_vastai.pub)"
```

### GPU検索

```bash
uvx vastai search offers 'gpu_name=RTX_4090 num_gpus=1 verified=true direct_port_count>=1 rentable=true' -o 'dlperf_usd-'
```

### インスタンス作成・確認

```bash
uvx vastai create instance OFFER_ID \
  --image nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 \
  --disk 20 \
  --onstart-cmd "nvidia-smi" \
  --ssh

uvx vastai show instance $INSTANCE_ID
uvx vastai ssh-url $INSTANCE_ID
```

### SSH接続

```bash
ssh -i ~/.ssh/id_ed25519_vastai root@xxx.xxx.xxx.xxx -p 12345
# SSH config 設定後
ssh vastai-gpu
```

### ファイル転送・GPU確認・削除

```bash
uvx vastai copy local:./data/ $INSTANCE_ID:/workspace/data/
nvidia-smi
uvx vastai destroy instance $INSTANCE_ID
```

お疲れ様でした。

## 参考

- [Vast.ai CLI Hello World](https://docs.vast.ai/cli/hello-world)
- [Vast.ai CLI Authentication](https://docs.vast.ai/cli/authentication)
- [Vast.ai SSH Connection](https://docs.vast.ai/guides/instances/connect/ssh)
- [Vast.ai Creating Templates](https://docs.vast.ai/documentation/templates/creating-templates)
