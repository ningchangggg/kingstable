#!/usr/bin/env python3
"""把 Artifact 用的 HTML 片段包成獨立網頁（補 doctype / html / head / body、charset、viewport 與 noindex）。"""
import io, sys, re

src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8").read()

# 去掉可能已存在的外層標籤，永遠從片段狀態重建
s = re.sub(r"(?is)^\s*<!doctype[^>]*>\s*", "", s)
# (?![a-zA-Z]) 避免把 <header> 當成 <head> 誤刪
s = re.sub(r"(?is)</?(?:html|head|body)(?![a-zA-Z])[^>]*>", "", s)

# 切出 head（meta / title / link / style）與 body
m = re.search(r"(?is)</style>", s)
head, body = (s[: m.end()], s[m.end():]) if m else ("", s)

# 來源檔是 Artifact 片段，charset、viewport 與基本重設原本由 Artifact 外框提供，這裡補回來
pre = []
if not re.search(r"(?i)<meta[^>]+charset", head):
    pre.append('<meta charset="utf-8">')
if not re.search(r"(?i)<meta[^>]+name=[\"']?viewport", head):
    pre.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
if "noindex" not in head:
    pre.append('<meta name="robots" content="noindex, nofollow, noarchive">')
# 放在頁面自己的 <style> 之前，頁面的樣式會蓋過它
pre.append(
    "<style>body{margin:0;padding:0}img{max-width:100%}"
    "[hidden]:not([hidden=until-found i]){display:none!important}</style>"
)

out = (
    "<!DOCTYPE html>\n<html lang=\"zh-Hant\">\n<head>\n"
    + "\n".join(pre)
    + "\n"
    + head.strip()
    + "\n</head>\n<body>\n"
    + body.strip()
    + "\n</body>\n</html>\n"
)
io.open(dst, "w", encoding="utf-8").write(out)
print(f"wrapped -> {dst} ({len(out)/1024/1024:.2f} MB)")
