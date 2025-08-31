# Image Uploader

## 概要
このプロジェクトは、PythonのWebフレームワークであるFlaskを使って構築された、シンプルな画像アップロードツールです。ユーザーがブラウザから画像をアップロードでき、アップロードされた画像はEXIFデータ（撮影日時など）に基づいて自動的にフォルダ分けされます。

## 特徴
- **自動フォルダ分け**: 画像のEXIF情報を読み取り、撮影年月に応じたフォルダ（例：`2025-08`）に画像を整理して保存します。
- **軽量でシンプル**: FlaskとPillowという2つの主要なライブラリのみを使用しており、最小限の依存関係で動作します。
- **エラーハンドリング**: 必要なフォルダやファイルが存在しない場合に、分かりやすいエラーメッセージを表示して起動を停止します。

## 必要な環境
- Python 3.6以上
- Flask
- Pillow

## インストール
1. このリポジトリをクローンします。
   ```bash
   git clone [https://github.com/caster2731/image-uploader.git](https://github.com/caster2731/image-uploader.git)
プロジェクトディレクトリに移動します。

Bash

cd image-uploader
必要なライブラリをインストールします。

Bash

pip install Flask Pillow
使い方
スクリプトを実行します。

Bash

python imagiup.py
ブラウザを開き、http://127.0.0.1:8000 にアクセスします。

ウェブ画面で画像をアップロードしてください。
