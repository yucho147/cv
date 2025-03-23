---
title: "ファイル名がバッティングする場合のpytestのファイルパスの管理方法について"
subtitle: "AWS Lambda の単体テスト構成(pytest + conftest 対応)"

# Summary for listings and search engines
summary: "ファイル名がバッティングする場合のpytestのファイルパスバッティング回避方法(conftest)"

# Link this post with a project
projects: []

# Date published
date: 2025-03-23T00:00:00+09:00

# Date updated
lastmod: 2024-03-23T00:00:00+09:00

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
- pytest

categories:
- post
- pytest
---

# AWS Lambda の単体テスト構成(pytest + conftest 対応)

## ゴール

- 本番の Lambda 関数コードのインポート構文(例：`from utils import mogamoga`)を一切変更せずに単体テストを実行したい
- Lambda 関数ごとにディレクトリ(例：`lambda_A`, `lambda_B`)を分け、同名の `lambda_handler.py` や `utils.py` などが共存しても、テストごとに正しく切り替えたい
- テスト側に毎回パス設定や import 記述を書かずに、共通の fixture で完結させたい

---

## ディレクトリ構成
下記のような別々のlambdaごとにtestをしたいが、個々のlambdaごとにファイル名がバッティングしている際にpytestで参照するパスがなかなかうまく通せなかった。
それをうまく通す方法を残しておく。

```
project-root/
├── aws_lambda/
│   ├── lambda_A/
│   │   ├── lambda_handler.py  # from utils import ...
│   │   └── utils.py
│   ├── lambda_B/
│   │   ├── lambda_handler.py
│   │   └── utils.py
├── tests/
│   ├── conftest.py            # fixtureとモジュールローダー
│   └── unit/
│       ├── test_lambda_A.py
│       └── test_lambda_B.py
```

---

## テストコード(例)
`conftest.py` での設定が鍵ではあるが、先に `conftest.py` で設定するfixtureの利用方法を提示しておく。

```python
# tests/unit/test_lambda_A.py

def test_lambda_A_handler(lambda_A_handler):
    response = lambda_A_handler.handler({}, {})
    assert response["statusCode"] == 200
    assert "Hello from utils in A" in response["body"]
```

```python
# tests/unit/test_lambda_B.py

def test_lambda_B_handler(lambda_B_handler):
    response = lambda_B_handler.handler({}, {})
    assert response["statusCode"] == 201
    assert "Hello from utils in B" in response["body"]
```

---

## conftest.py の中身(共通fixture)
ここは完全に理解せずにchatgptに作ってもらったものである。
各テストコードで想定通りの利用をすれば、正しいパスが読み込まれていることは確認済みである。

```python
# tests/conftest.py
import sys
import pytest
import importlib.util
from pathlib import Path


def clear_modules_from_lambda_dir(lambda_name: str) -> None:
    lambda_path = Path("aws_lambda") / lambda_name
    for py_file in lambda_path.rglob("*.py"):
        mod_name = py_file.stem
        if mod_name in sys.modules:
            del sys.modules[mod_name]


def add_lambda_path(lambda_name: str) -> None:
    path = Path("aws_lambda") / lambda_name
    abs_path = str(path.resolve())
    if abs_path not in sys.path:
        sys.path.insert(0, abs_path)


def load_lambda_handler(lambda_name: str):
    clear_modules_from_lambda_dir(lambda_name)
    handler_path = Path("aws_lambda") / lambda_name / "lambda_handler.py"
    spec = importlib.util.spec_from_file_location(f"{lambda_name}_handler", handler_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def lambda_A_handler():
    add_lambda_path("lambda_A")
    return load_lambda_handler("lambda_A")


@pytest.fixture(scope="session")
def lambda_B_handler():
    add_lambda_path("lambda_B")
    return load_lambda_handler("lambda_B")
```

---

## 実行方法

プロジェクトルートで以下を実行：

```bash
pytest tests
```

---

## サンプルZIPファイル

こちらにサンプル構成一式をまとめた ZIP を共有しています：

👉 [lambda_test_fixture_pathlib.zip をダウンロード](https://drive.google.com/file/d/1nPbCDtqMNIu4wMa5fDGxqf4RHIXXFNes/view?usp=drive_link)

適当なからディレクトリでunzipして前述の `pytest tests` を実行することで確かめることができる。

---

## 補足

- Lambda 関数が増えても `conftest.py` に fixture を1つ追加するだけで拡張可能です
- `clear_modules_from_lambda_dir` によって `utils.py` をはじめとする個別のファイルのバッティングを防止しています
