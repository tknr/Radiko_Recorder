# Radiko Recorder

本ツールは、Radikoからラジオ放送を録音するためのアプリケーションです。

## 1. 必要条件

本ツールを使用する前に、以下の条件を満たしていることを確認してください：

- `ffmpeg`のインストール
  - 録音機能を使用するには、ffmpegが必要です。
  - `ffmpeg`がインストールされていない場合、以下のコマンドを使用してインストールしてください：

**Ubuntu/Debian**:
```sh
sudo apt update
sudo apt install ffmpeg
```

**Mac (Homebrew)**:
```sh
brew install ffmpeg
```

**Windows**:
1. [公式サイト](https://ffmpeg.org/download.html)からダウンロードしてください。
2. システム環境変数にffmpegのパスを追加してください。


## 2. 放送局リストの表示

放送局のリストを表示するには、`-s`または`--station-list`オプションを使用します：

```sh
radiko-recorder -s
```

## 3. 放送局の録音

ラジオ放送を録音するには、以下のコマンドを使用します：

```sh
radiko-recorder <station_id> <start_time> <duration_minutes>
```

- `<station_id>`: 録音したい放送局のID（例：`TBS`, `QRR`など）。
- `<start_time>`: 録音開始時間を`YYYYMMDDHHMMSS`形式で指定。
- `<duration_minutes>`: 録音時間（分）。

例:
```sh
radiko-recorder FMT 20241120120000 50
```

これは、2024年11月20日12:00:00から50分間、TOKYO FM局からの放送を録音します。

## 4. ライセンス
本プロジェクトは、MITライセンスの下でライセンスされています。
詳細については、[LICENSEファイル](./LICENSE)を参照してください。

## 5. 著作権表示
Copyright (c) 2024 ARM
