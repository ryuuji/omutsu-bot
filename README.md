omutsu-bot
================
おむつの記録をSlackに送る

コンセプト
-----
- HueブリッジとスイッチのイベントをSlackに送る

![](image.png)

コマンドライン
----
```bash
poetry install
poetry run python main.py {ブリッジのIP} {APPKEY} {センサーID} {SlackのWEBHOOK}
```
