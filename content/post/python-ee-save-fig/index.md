---
title: "Google Earth Engineを使った衛星画像の可視化"
subtitle: "pythonを用いて、GEEの衛星画像の可視化を行います"

# Summary for listings and search engines
summary: "pythonを用いて、GEEの衛星画像の可視化を行います"

# Link this post with a project
projects: []

# Date published
date: 2024-06-19T08:46:22+09:00

# Date updated
lastmod: 2024-06-19T08:46:22+09:00

# Is this an unpublished draft?
draft: true

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

本ページでは `earthengine-api` を使ってGoogle Earth Engine(GEE)をpythonを通してアクセスします。
さらに、衛星画像をpngファイルとして保存するまでの手続きをフォローします。

### 環境構築

pythonからGEEを用いるために `earthengine-api` をインストールしましょう

```bash
pip install earthengine-api
```

### `earthengine-api` のimport

以前[紹介したページ](../gee-setup/)で紐づけた `Project-ID` をあらかじめ用意しておいてください。

```python
import ee

project = "your_project_id"
ee.Authenticate()
ee.Initialize(project=project)
```

### `earthengine-api` について

`earthengine-api` では下記の9つのオブジェクトを提供しています。

+ `Image`
+ `ImageCollection`
+ `Geometry`
+ `Feature`
+ `FeatureCollection`
+ `Reducer`
+ `Join`
+ `Array`
+ `Chart`

衛星画像を取得するために、上記のうち `ImageCollection, Image` を用います。
また、衛星画像に対して特定の条件を課して、目的にあうデータを取得します。

### 取得データの設定

まず取得する緯度経度を定義します

```python
coords = [
    [139.872241, 35.621194],  # 左下
    [139.872241, 35.639219],  # 左上
    [139.893765, 35.639219],  # 右上
    [139.893765, 35.621194],  # 右下
    [139.872241, 35.621194],  # 左下(ポリゴンを閉じなくてはならない)
]
```

取得する期間を設定します

```python
# 期間の設定
# 開始
start_date ='2023-07-01'
# 終了
end_date = '2023-07-31'
```

今回はSentinel-2と呼ばれるESAが管理する衛星のデータを取得します。
[こちら](https://www.restec.or.jp/satellite/sentinel-2-a-2-b)のRESTECさんのページにて詳細はまとまめられています。
可視光に当たるデータを取得してみましょう。可視化の場合、雲が覆ってしまうと地表面が見えなくなってしまいます。通常地表を観測したい場合が多く、雲の被覆率に応じたフィルタリングもかけることが可能です。
あらかじめその被覆率の上限値を設定しておきましょう。

```python
# 雲の被覆率の上限値
cloud_cover_rate = 30
```

### データの取得

設定が終わり、データの取得を実行してみましょう。

```python
# ImageCollectionの絞り込み
imgcol = (
    ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(ee.Geometry.Polygon(coords))
    .filterDate(ee.Date(start_date), ee.Date(end_date))
    .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',cloud_cover_rate))
)
```

この処理で得られる `imgcol` は `ImageCollection` というオブジェクトになっています。

フィルタをかけた `ImageCollection` の画像IDを確認してみます。

```python
id_list = imgcol.aggregate_array('system:id').getInfo()
print(id_list)
```

結果
```python
['COPERNICUS/S2_SR_HARMONIZED/20230711T012659_20230711T013643_T54SUE', 'COPERNICUS/S2_SR_HARMONIZED/20230716T012701_20230716T013426_T54SUE', 'COPERNICUS/S2_SR_HARMONIZED/20230726T012701_20230726T013640_T54SUE']
```
と出力され、3枚の衛星画像を取得できていることが確認できました。

### 画像の可視化

まずは取得した衛星画像を取得します

```python
# ImageCollectionから1枚目の画像を選択
image = ee.Image(id_list[0])

# 選択した画像のバンド情報を確認
print(image.bandNames().getInfo())
```

結果
```python
['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12', 'AOT', 'WVP', 'SCL', 'TCI_R', 'TCI_G', 'TCI_B', 'MSK_CLDPRB', 'MSK_SNWPRB', 'QA10', 'QA20', 'QA60']
```
と出力され、格納されているバンド情報を確認できます。
特にSentinel-2データには複数のバンド(波長)情報が含まれており、可視化する際にはこれらのバンドを組み合わせて表示します。一般的にはRGB画像を表示するためにB4(赤)、B3(緑)、B2(青)のバンドを使用します。

続いて、指定したバンドを用いて衛星画像を可視化し、PNGファイルとして保存する手順を説明します。

### 画像のHTMLでの可視化

取得した衛星画像をHTML上で可視化するために、Foliumを使用します。Foliumは、PythonでLeaflet.jsを使った地図を生成するライブラリです。まず、Foliumをインストールしましょう。

```bash
pip install folium
```

次に、Foliumを使用して衛星画像を地図上に表示します。

```python
import folium

# 中心座標を設定
center_coords = [35.630207, 139.882853]

# Foliumマップを作成
m = folium.Map(location=center_coords, zoom_start=13)

# 画像をマップに追加
folium.TileLayer(
    tiles=image.getMapId({'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000})['tile_fetcher'].url_format,
    attr='Google Earth Engine',
    name='Sentinel-2',
    overlay=True
).add_to(m)

# レイヤーコントロールを追加
folium.LayerControl().add_to(m)

# マップをHTMLファイルとして保存
m.save('satellite_image.html')
```

これで、satellite_image.html ファイルをブラウザで開くと、取得した衛星画像が表示されます。

### 画像のPNGファイルとしての保存

取得した衛星画像をPNGファイルとしてローカルに保存するために、まず画像を取得して配列に変換し、次にその配列をmatplotlibを使用してPNGファイルとして保存します。

以下に、matplotlibを使用して衛星画像をPNGファイルとして保存する手順を示します。

まず、必要なライブラリをインストールします。

```bash
pip install matplotlib
```

次に、取得した画像を配列に変換してPNGファイルとして保存します。

```python
import numpy as np
import matplotlib.pyplot as plt

# 画像を取得
image = ee.Image(id_list[0])

# 画像の取得範囲を指定
region = ee.Geometry.Polygon(coords)

# 画像を配列に変換
image_data = image.select(['B4', 'B3', 'B2']).reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=region,
    scale=10
).getInfo()

# 各バンドのデータを配列に変換
b4 = np.array(image_data['B4']).reshape((len(image_data['B4'])//len(coords), len(coords)))
b3 = np.array(image_data['B3']).reshape((len(image_data['B3'])//len(coords), len(coords)))
b2 = np.array(image_data['B2']).reshape((len(image_data['B2'])//len(coords), len(coords)))

# 各バンドのデータをスタックしてRGB画像を作成
rgb_image = np.dstack((b4, b3, b2))

# 画像を表示
plt.imshow(rgb_image)
plt.axis('off')

# 画像をPNGファイルとして保存
plt.savefig('satellite_image.png', bbox_inches='tight')
plt.show()
```
