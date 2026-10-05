---
title: "用 Python 生成 Minecraft 投影文件"
date: 2026-10-04
draft: false
tags: ["Python", "Minecraft", "自动化"]
categories: ["折腾记录"]
summary: "手搓 .litematic 生成器，把红石机械做成可一键粘贴的结构。"
---

Litematica 的 `.litematic` 是个二进制格式，但结构不算复杂，用 Python 完全可以暴力生成。

## 文件结构

核心是 `Regions` 里的 `BlockStates`，它是**按位打包**的：

```python
def pack_bits(indices, bits_per_block):
    """LSB-first 位打包"""
    buf = 0
    offset = 0
    out = []
    for idx in indices:
        buf |= idx << offset
        offset += bits_per_block
        while offset >= 64:
            out.append(buf & 0xFFFFFFFFFFFFFFFF)
            buf >>= 64
            offset -= 64
    if offset:
        out.append(buf & 0xFFFFFFFFFFFFFFFF)
    return out
```

## 踩过的坑

**坑一：位序反了。**

第一版按 MSB-first 打包，游戏里打开全乱了。改成 LSB-first 才对。

**坑二：调色板顺序。**

`Palette` 里的方块顺序要跟 `BlockStates` 里的索引对应，顺序错了方块会串。

## 效果

现在改个参数就能生成不同尺寸的机械，比手搭快多了。

```bash
python mc_gen_litematic.py --size 9x5x3 --out iron_golem.litematic
```
