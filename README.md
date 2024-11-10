# Radiko Recorder

Radiko Recorderは、Radikoからラジオ放送を録音するためのツールです。このリポジトリには、Radikoの録音機能を使用するために必要なスクリプトと設定が含まれています。

## ■必要条件

- Python 3.8以上

## ■使い方

Radiko RecorderはコマンドラインまたはJupyterノートブックで使用できます。以下に両方の方法について説明します。

### コマンドライン

#### 放送局リストの表示

放送局のリストを表示するには、`-sl`または`--station-list`オプションを使用します：

```sh
sh Radiko_Recorder.sh -sl
```

## ■放送局の録音

ラジオ放送を録音するには、以下のコマンドを使用します：

```sh
sh Radiko_Recorder.sh <station_id> <start_time> <duration_minutes>
```

- `<station_id>`: 録音したい放送局のID（例：`TBS`, `QRR`など）。
- `<start_time>`: 録音開始時間を`YYYYMMDDHHMMSS`形式で指定。
- `<duration_minutes>`: 録音時間（分）。

例:
```sh
sh Radiko_Recorder.sh FMGUNMA 20240604000000 50
```

これは、2024年6月4日00:00:00から50分間、FMGUNMA局を録音します。

## ■設定
Radiko Recorderを使用するには、`config.py`ファイルでいくつかの設定を行う必要があります。`RADIKO_AREA_ID`と`OUTPUT_DIR`の変数を必要に応じて設定してください。

## ■ファイル
- `Radiko_Recorder.sh`: Pythonを使用してレコーダーを実行するためのシェルスクリプト。
- `Radiko_Recorder.cmd`: Windowsでレコーダーを実行するためのコマンドスクリプト。

## ■ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。

## ■著作権表示
© 2024 ARM