# メディア･テキストアップローダ
クラウドサービスやケーブルを使用せず、モバイル端末とPC間でメディア（画像・動画）やURLなどのテキストを転送できるシンプルなWebサーバープロジェクトです。

## 機能
- 画像・動画のアップロード: iOSデバイスからPCへの直接アップロードをサポート。
- メディアリストの表示: アップロードされたメディアファイルのリンクを一覧表示。
- シンプルなUI: iOSデバイスにも最適化されたボタンや表示スタイル。
- セキュリティ: PC上で指定したディレクトリ以外へのアクセスを制限。

## 動作環境
- Python 3.x
- Flask

## インストール
Flaskのインストール: 以下のコマンドでFlaskをインストールします。
```
pip install Flask
```

リポジトリのクローン:
```
git clone https://github.com/t3kkun/media_uploader.git
cd media_uploader
```

## 使用方法
サーバーの起動:
```
python upload_server_flask.py
```
サーバーが起動すると、PCのIPアドレスとポート番号が表示されます。

LAN内にいる他のデバイスからアクセス: ブラウザで、表示されたIPアドレスとポート番号にアクセスします

(例: `http://192.168.x.x:8000`)

実行中のマシンで`http://localhost:8000`を参照するとローカルIPアドレスを確認することもできます。

メディアのアップロード: Choose a file ボタンから画像や動画を選択し、Upload ボタンでアップロードできます。

アップロードされたファイルの確認: ページ下部にアップロード済みメディアのリンクが表示されます。リンクをクリックすることで、各メディアファイルを確認可能です。

## 注意事項
- ネットワーク設定: iOSデバイスとPCが同一ネットワークに接続されている必要があります。
- セキュリティ: 上位ディレクトリの参照を制限していますが、使用時には注意してください。

## ライセンス
- MIT License
