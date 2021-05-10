# Discord Voice Channel Entry Time Recording
ボイスチャンネルの入室時間を計測します。

## 特徴
- ボイスチャンネルの入室から退室までの時間を計測できます。
- 時間計測の有無をコマンドで管理できます。
- 複数サーバーには未対応

## 環境構築
1. Make sure to get Python 3.9 or higher  
This is required to actually run the bot.

1. Set up venv  
   Just do `python3.9 -m venv venv`
   PyCharmの場合、環境構築が容易なのでそちらをつかうことをおすすめします。   

1. Install dependencies  
`pip install -U -r requirements.txt`
   
1. Setup configuration
```
client_id   = '' # your bot's client ID
token = '' # your bot's token
```
1. Start
`python launcher.py`
