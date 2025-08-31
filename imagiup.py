from flask import Flask, request, redirect, url_for, render_template, flash
import os
import sys

from datetime import datetime
from PIL import Image
# スクリプトファイルがあるディレクトリを基準に保存先フォルダを設定
basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, 'templates')

# アプリケーションを起動する前に、テンプレートフォルダとファイルの存在を確認
if not os.path.isdir(template_dir):
    print(f"致命的なエラー: テンプレートフォルダが見つかりません。")
    print(f"期待されるパス: {template_dir}")
    print(f"スクリプトと同じ階層に 'templates' という名前のフォルダを作成してください。")
    sys.exit(1)

if not os.path.isfile(os.path.join(template_dir, 'index.html')):
    print(f"致命的なエラー: 'index.html' が 'templates' フォルダ内に見つかりません。")
    print(f"ファイル名や場所が正しいか確認してください。")
    print(f"期待されるファイルのフルパス: {os.path.join(template_dir, 'index.html')}")
    sys.exit(1)


# Flaskアプリの初期化時に、テンプレートフォルダの場所を明示的に指定
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'your-secret-key' # flashメッセージのために必要
UPLOAD_FOLDER = os.path.join(basedir, 'uploaded_images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 'image'キーでアップロードされたファイルのリストを取得
    uploaded_files = request.files.getlist('image')

    # ファイルが1つも選択されていない場合
    if not uploaded_files or uploaded_files[0].filename == '':
        flash('ファイルが選択されていません', 'warning')
        return redirect(url_for('index'))

    saved_files = []
    for file in uploaded_files:
        # ファイルが存在し、ファイル名があることを確認
        if file and file.filename:
            year_month_folder = None
            try:
                # Pillowで画像を開きEXIF情報を読み取る
                with Image.open(file) as img:
                    exif_data = img._getexif()
                    if exif_data:
                        # 36867は撮影日時のタグID (DateTimeOriginal)
                        date_str = exif_data.get(36867)
                        if date_str and isinstance(date_str, str) and len(date_str) >= 7:
                            # 'YYYY:MM:DD ...' 形式から 'YYYY-MM' を作成
                            year_month_folder = f"{date_str[:4]}-{date_str[5:7]}"
            except Exception:
                # EXIFが読めない、または画像ファイルでない場合は何もしない
                pass

            # EXIFに日付がない場合は、現在の年月をフォルダ名として使用
            if not year_month_folder:
                year_month_folder = datetime.now().strftime('%Y-%m')

            # 保存先フォルダを作成
            target_dir = os.path.join(UPLOAD_FOLDER, year_month_folder)
            os.makedirs(target_dir, exist_ok=True)

            # ファイルを保存
            filepath = os.path.join(target_dir, file.filename)
            file.seek(0) # Pillowがストリームを読み進めているため、先頭に戻す
            file.save(filepath)
            # 結果表示用に相対パスを保存 (例: "2025-06/image.jpg")
            saved_files.append(os.path.join(year_month_folder, file.filename))

    if not saved_files:
        flash('アップロードできるファイルがありませんでした。', 'info')
        return redirect(url_for('index'))
    return render_template('upload_result.html', saved_files=saved_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
