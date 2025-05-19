---
title: "xROAD常時観測交通量(国管理道路)データ取得MCP"
subtitle: "xROAD常時観測交通量(国管理道路)のデータを取得するMCPを構築する"

# Summary for listings and search engines
summary: "xROAD常時観測交通量(国管理道路)のデータを取得するMCPを構築する"

# Link this post with a project
projects: []

# Date published
date: 2025-05-20T00:00:00+09:00

# Date updated
lastmod: 2024-05-20T00:00:00+09:00

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
- xROAD
- MCP

categories:
- post
- xROAD
- MCP
---

# はじめに
2023年はRAG, 2024年はAgent, 2025年はMCPが流行っていますね。

自分でも構築できるように、前回の[xROAD常時観測交通量(国管理道路)データ取得](https://www.yuyakaneta.page/post/xroad_jartic-open-traffic/)のデータ取得用のMCPを構築してみました。

(ただし、非常に発展が早い事柄であるために、今回共有するコードがすぐ非推奨の実装になってしまうかもです。)

# 環境構築
おそらくpythonで動くコードであれば、 `uv` を使うことをお勧めします。

`uv` だと環境構築が簡易化・高速化されることもそうですが、コマンド(`uv run mogamoga.py` といった具合)一つで仮想環境での実行も実現することが良さげだなーと思いました。
実際にMCP Python SDKの公式でも `uv` を推奨しています。本記事では `uv` の解説は省略します。

今回必要なモジュールをインストールします。

```bash
uv add "mcp[cli] "pandera[geopandas]" geopandas geopy requests langchain langchain-openai langgraph langchain_mcp_adapters
```

必要なモジュールを一括で入れておきました。

# MCPサーバーの構築
[前回](https://www.yuyakaneta.page/post/xroad_jartic-open-traffic/)の記事を参考にMCPサーバーを構築しました。

まずはジオコーディングをして、文字列から緯度経度を取得する関数を用意します。

```python
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="geoapi_test")


def get_lat_lon(
        address: Annotated[str, Field(description="地名（例：札幌駅）")],
) -> dict:
    """地名から緯度経度を取得します"""
    location = geolocator.geocode(address)
    if location:
        return {"lat": location.latitude, "lon": location.longitude}
    else:
        raise ValueError("Address not found")
```

`geopy` を使うことで、こんな感じで緯度経度を取得できます。OpenStreetMapなどからデータを取得して、ジオコーディングをしているっぽいです。

超簡単なMCPとしては

```python
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("XROAD")


@mcp.tool()
def get_current_datetime() -> str:
    """現在日時をISO8601形式で返します"""
    return datetime.now(tz=timezone.utc).isoformat()


if __name__ == "__main__":
    mcp.run()
```

こんな感じで現在時刻を取得するMCP(tool)が完成です。

その上で、前回の記事と組み合わせて、一挙にxROADからデータを自然言語で取得するtoolを構築します。

```python
from datetime import datetime, timezone
from typing import Annotated, Literal

import geopandas as gpd
import pandera.pandas as pa
import requests
from mcp.server.fastmcp import FastMCP
from geopy.geocoders import Nominatim
from pandera.pandas import Column, Check
from pydantic import Field


mcp = FastMCP("XROAD")
geolocator = Nominatim(user_agent="geoapi_test")


def valid_timecode_str(series):
    try:
        # 文字列として整数に変換し、分 < 60 を満たすものだけ通す
        series_int = series.astype(int)
        return (
            series_int.between(0, 2359) & (series_int % 100 < 60)
        )
    except Exception:
        return False


schema = pa.DataFrameSchema(
    {
        "id": Column(str),
        "地方整備局等番号": Column(int, checks=Check.ge(0)),
        "開発建設部／都道府県コード": Column(str),
        "常時観測点コード": Column(int, checks=Check.ge(0)),
        "収集時間フラグ（5分間／1時間）": Column(str, checks=Check.isin(["1", "2"])),
        "観測年月日": Column(int, checks=Check.in_range(20000101, 21000101)),

        "時間帯": Column(str, checks=Check(check_fn=valid_timecode_str)),

        "上り・小型交通量": Column(int, checks=Check.ge(0)),
        "上り・大型交通量": Column(int, checks=Check.ge(0)),
        "上り・車種判別不能交通量": Column(int, checks=Check.ge(0)),
        "上り・停電": Column(str, checks=Check.isin(["0", "1"])),
        "上り・ループ異常": Column(str, checks=Check.isin(["0", "1"])),
        "上り・超音波異常": Column(str, checks=Check.isin(["0", "1"])),
        "上り・欠測": Column(str, checks=Check.isin(["0", "1"])),

        "下り・小型交通量": Column(int, checks=Check.ge(0)),
        "下り・大型交通量": Column(int, checks=Check.ge(0)),
        "下り・車種判別不能交通量": Column(int, checks=Check.ge(0)),
        "下り・停電": Column(str, checks=Check.isin(["0", "1"])),
        "下り・ループ異常": Column(str, checks=Check.isin(["0", "1"])),
        "下り・超音波異常": Column(str, checks=Check.isin(["0", "1"])),
        "下り・欠測": Column(str, checks=Check.isin(["0", "1"])),

        "道路種別": Column(str),
        "時間コード": Column(str, checks=[
            Check.str_length(12),
            Check.str_matches(r"^\d{12}$"),
        ]),

        "geometry": Column("geometry"),
    },
    coerce=True
)


def get_lat_lon(
        address: Annotated[str, Field(description="地名（例：札幌駅）")],
) -> dict:
    """地名から緯度経度を取得します"""
    location = geolocator.geocode(address)
    if location:
        return {"lat": location.latitude, "lon": location.longitude}
    else:
        raise ValueError("Address not found")


@mcp.tool()
def fetch_jartic_open_traffic_1h_data(
        location: Annotated[str, Field(description="地名（例：札幌駅）")],
        start_date: Annotated[str, Field(description="開始日時（YYYYMMDDHHMM）")],
        end_date: Annotated[str, Field(description="終了日時（YYYYMMDDHHMM）")],
        road_type: Annotated[Literal["1", "3"], Field(description="道路種別（1: 高速道路, 3: 国道）")],
        lat_margin: Annotated[float, Field(description="緯度方向の検索範囲マージン（度）")] = 0.1,
        lon_margin: Annotated[float, Field(description="経度方向の検索範囲マージン（度）")] = 0.1,
) -> dict:
    """地名と期間を指定して、1時間ごとの国道交通量データ（GeoJSON）を取得します"""
    lat_lon = get_lat_lon(location)
    lat = lat_lon["lat"]
    lon = lat_lon["lon"]

    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeNames": "t_travospublic_measure_1h",
        "srsName": "EPSG:4326",
        "outputFormat": "application/json",
        "exceptions": "application/json",
        "cql_filter": (
            f"道路種別 = {road_type} AND "
            f"時間コード >= {start_date} AND "
            f"時間コード <= {end_date} AND "
            f"BBOX(ジオメトリ, {lon - lon_margin}, {lat - lat_margin}, "
            f"{lon + lon_margin}, {lat + lat_margin}, 'EPSG:4326')"
        ),
    }

    response = requests.get(
        "https://api.jartic-open-traffic.org/geoserver",
        params=params,
    )
    response.raise_for_status()
    return aggregate_daily_volume(response.text)  # GeoJSON形式の文字列を検証


def aggregate_daily_volume(
    traffic_geojson: Annotated[str, Field(description="交通量データのGeoJSON文字列")],
) -> dict:
    """交通量データ（GeoJSON）を日毎に集計します"""
    gdf = gpd.read_file(traffic_geojson)
    gdf = schema.validate(gdf)
    if "時間コード" not in gdf:
        return {"error": "時間コードが見つかりません"}

    # 時間コードから日付（YYYYMMDD部分）を抽出
    gdf["日付"] = gdf["時間コード"].str[:8]

    # 上り・下りそれぞれの合計交通量列を作成
    gdf["上り交通量合計"] = (
        gdf["上り・小型交通量"]
        + gdf["上り・大型交通量"]
        + gdf["上り・車種判別不能交通量"]
    )
    gdf["下り交通量合計"] = (
        gdf["下り・小型交通量"]
        + gdf["下り・大型交通量"]
        + gdf["下り・車種判別不能交通量"]
    )

    # 日毎に合計を集計
    df = (
        gdf.groupby("日付")[["上り交通量合計", "下り交通量合計"]]
        .sum()
        .reset_index()
    )

    return df.to_dict(orient="records")


@mcp.tool()
def get_current_datetime() -> str:
    """現在日時をISO8601形式で返します"""
    return datetime.now(tz=timezone.utc).isoformat()


if __name__ == "__main__":
    mcp.run()
```

上記のファイルを `server.py` として保存しておいてください。

データのバリデーションを `pandera` を使って実装していますが、geojsonの段階で `pydantic` で構築しても良いかもです。
まぁMCPの場合、処理系とagentを分離できることが強いメリットなのだろうと思います。
これによって機能の分離が実現し、toolの単体テストなども容易にできます。
一方、コンテキストウィンドウも節約するためにできる限り関数の中で集計処理も実施しているため、機能が小さく切られているとは言いにくいかもです。


# Agent(ReAct型)の構築
MCPだけでは何も面白くないので、Agent(ReAct)でMCPを受け取り、想定通りの処理ができているか確かめてみます。
Agent自体は `langgraph` での実装なので、本質的には数行で完了します。

一方MCPを認識させるためには、設定ファイル(`config.yaml`)で実行方法などを書き記しておきます。

```yaml
XROAD:
  transport: stdio
  command: uv
  args:
    - run
    - --with
    - mcp[cli],pandera[geopandas],geopandas,geopy,requests
    - mcp
    - run
    - /your/file/path/server.py
```

こんな具合です。

この `config.yaml` を読み込んで、あとは `langchain_mcp_adapters` に任せて、MCPとAgentを接続させます。

```python
import yaml
from langchain_mcp_adapters.client import MultiServerMCPClient

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# MCPクライアントの初期化
client = MultiServerMCPClient(config)
tools = await client.get_tools()
```

こんな具合です(上記のままでは `await` があるため正常に動きません)。この処理で `server.py` (MCP)で定義したtoolを、 `langchain` のtool型のオブジェクトを得ることができます。

ReAct型のAgentは

```python
from langgraph.prebuilt import create_react_agent

graph = create_react_agent(
    model="openai:gpt-4o",
    tools=tools,
)
```

こんな感じで用意することができます。
あとは非同期処理も含む応答をcliで実行するコードを構築したので、共有します。

```python
import asyncio
import yaml
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


async def main():
    # 設定ファイルの読み込み
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # MCPクライアントの初期化
    client = MultiServerMCPClient(config)
    tools = await client.get_tools()

    # ReActエージェントの作成
    graph = create_react_agent(
        model="openai:gpt-4o",
        tools=tools,
    )

    print("LangGraphのReActエージェントを実行します。終了するには 'exit' または 'quit' と入力してください。")

    # ユーザーとの対話ループ
    while True:
        user_input = input("\nユーザー: ")
        if user_input.lower() in {"exit", "quit"}:
            print("エージェントを終了します。")
            break

        inputs = {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        }
        # 非同期ストリーム出力をawaitで処理
        async for s in graph.astream(inputs, stream_mode="values"):
            message = s["messages"][-1]

            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())
```

これを使うことで、いつでも簡易的に自作MCPを試すことができます(使いまわせます)。
ぜひ自作MCPの実験に使ってみてください。

結果、下記の動画のような実行が実現できます。
<iframe src="https://drive.google.com/file/d/1JnMY8IMNQt0gRXd55sWE-cDXPoX0wK-C/preview" width="640" height="480" allow="autoplay"></iframe>
