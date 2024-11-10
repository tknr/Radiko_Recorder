# Radiko Recorder

Radikoからラジオ放送を録音するためのツールです。

## ■放送局リストの表示

放送局のリストを表示するには、`-sl`または`--station-list`オプションを使用します：

```sh
radiko-recorder -sl
```

## ■放送局の録音

ラジオ放送を録音するには、以下のコマンドを使用します：

```sh
radiko-recorder <station_id> <start_time> <duration_minutes>
```

- `<station_id>`: 録音したい放送局のID（例：`TBS`, `QRR`など）。
- `<start_time>`: 録音開始時間を`YYYYMMDDHHMMSS`形式で指定。
- `<duration_minutes>`: 録音時間（分）。

例:
```sh
radiko-recorder FMGUNMA 20240604000000 50
```

これは、2024年6月4日00:00:00から50分間、FMGUNMA局を録音します。

## ■ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。

## ■著作権表示
© 2024 ARM
