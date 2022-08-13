●python 仮想環境作成
python3 -m venv fastapi-env

●仮想環境起動
source fastapi-env/bin/activate

●パッケージインストール
pip3 install fastapi uvicorn

●データベースライブラリ
pip3 install SQLAlchemy

●ハッシュ化ライブラリ
pip3 install passlib bcrypt

●JWTトークン用モジュール
pip3 install python-jose

●フォームデータ用モジュール
pip3 install python-multipart

●webサーバ起動
uvicorn main:app --reload [--host 0.0.0.0]

●仮想環境終了
deactivate


