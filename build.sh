#!/usr/bin/env bash
cd $(dirname $0)
set -e
PYTHON_COMMAND="python3"

if ! command -v python3 &>/dev/null; then
    if ! command -v python &>/dev/null; then
        echo "Error: Python not found, please install python 3.8 or higher and try again"
        exit 1
    fi
fi

if command -v python &>/dev/null; then
   PYTHON_COMMAND="python"
fi

echo "Found $PYTHON_COMMAND command"

python_version=$($PYTHON_COMMAND --version 2>&1 | awk '{print $2}')  
echo "Python version : $python_version"

BASEDIR=$(pwd)

# shellcheck disable=SC1091
pip install virtualenv
$PYTHON_COMMAND -m virtualenv --python=python3.12 "$BASEDIR/python312"
source "$BASEDIR/python312/bin/activate"

$PYTHON_COMMAND -m pip install wheel
$PYTHON_COMMAND -m pip install -r "$BASEDIR/requirements.txt"


echo "Build start..."

# UPXのパスを取得
UPX_PATH=$(command -v upx)

# UPXのパスが見つからない場合エラーを表示
if [ -z "$UPX_PATH" ]; then
    echo "Error: UPX not found in PATH."
    echo "Please ensure UPX is installed and its directory is in the PATH environment variable."
    exit 1
fi

# UPXのディレクトリを取得
UPX_DIR=$(dirname "$UPX_PATH")
echo "UPX Directory: $UPX_DIR"

# Poetry仮想環境でPyInstallerを実行
poetry run pyinstaller --onefile --name radiko-recorder -c --hidden-import=radiko_recorder --upx-dir "$UPX_DIR" -p ./radiko_recorder radiko_recorder/__main__.py

# ビルドが成功したかを確認
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo "Build complete!"

