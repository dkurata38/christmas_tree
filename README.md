# christmas_tree **執筆中**
クリスマスツリー度を判定します。

## Webアプリの起動方法
### 目次
+ Python3.6をインストール
+ SQliteをインストール
+ 依存するパッケージのインストール
+ Flask Serverの起動

### pythonのインストール
#### Windows
**加筆予定**


#### Mac
Homebrewでpyenvをインストールし、pyenvでPythonのバージョン管理をします。
``` bash
$ brew install pyenv
$ pyenv versions
$ pyenv install 3.6.6
$ pyenv global 3.6.6
```
### SQliteのインストール
#### Windows
**加筆予定**
とりあえずこれを見てインストールしてほしい
[SQLiteのインストール|SQLite入門](https://www.dbonline.jp/sqlite/install/)
#### Mac
Homebrewでsqliteをインストールする。
```bash
$ brew install sqlite3
```
バグった場合は、`brew doctor`コマンドでHomebrewが正常に動くかどうかを確かめる。
警告が出た場合は警告の内容を検索する。

### パッケージのインストール
pipでインストールをする。
Python3なのでpip3のほうがいいかもしれない。
```bash
$ pip3 install -r requirements.txt
```

### DBの構築
Pythonのコンソールを開く。
```bash
$ cd christmas_tree_web/
$ python
```
Pythonのコンソールから、SQliteのデータベースを初期化する。
```python
from app import db
db.create_all()
```

### Flask Serverの起動
christmas_tree_webディレクトリ配下で以下のコマンドを実行する。
```bash
$ python run.py
```
