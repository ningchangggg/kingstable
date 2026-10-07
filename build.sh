#!/usr/bin/env bash
# 由 iCloud 的成品檔產生 GitHub Pages 用的完整 HTML 文件。
# 用法：./build.sh   （改完內容後執行，再 git commit && git push）
# 上層資料夾改名過（○山城一鳴 → ◼︎山城一鳴），所以來源檔用檔名搜尋，不寫死路徑。
# 找不到或找到多個時，自己指定：SRC="/完整/路徑/檔名.html" ./build.sh
set -e
NAME="大人物牛排_創作者拍攝指南_手機版.html"
ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$SRC" ]; then
  FOUND="$(find "$ICLOUD" -maxdepth 3 -name "$NAME" 2>/dev/null)"
  COUNT="$(printf '%s' "$FOUND" | grep -c . || true)"
  [ "$COUNT" -eq 1 ] || { echo "找到 $COUNT 個來源檔（應該剛好 1 個），請用 SRC=... 指定：" >&2; printf '%s\n' "$FOUND" >&2; exit 1; }
  SRC="$FOUND"
fi
[ -f "$SRC" ] || { echo "找不到來源檔：$SRC" >&2; exit 1; }

python3 "$DIR/wrap.py" "$SRC" "$DIR/index.html"
