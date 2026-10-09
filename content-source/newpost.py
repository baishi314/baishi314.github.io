# -*- coding: utf-8 -*-
"""
新建文章向导
============
双击「发布.bat」会调用这里。

也可以命令行直接用：
    python content-source/newpost.py
"""
import os
import re
import sys
import datetime

# Windows 控制台/管道默认是 GBK，会把中文读坏。强制按 UTF-8 处理输入输出。
try:
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "content-source", "posts")


def ask(prompt, default=""):
    if default:
        r = input(f"{prompt} [{default}]: ").strip()
        return r if r else default
    return input(f"{prompt}: ").strip()


def ask_yes(prompt, default="n"):
    r = input(f"{prompt} (y/n) [{default}]: ").strip().lower()
    if not r:
        r = default
    return r in ("y", "yes", "是", "1")


def slugify(title):
    """生成文件名 slug。

    为什么不用中文名：
      Next.js 会把中文 slug 做 URL 编码后再去找文件，导致 ENOENT 构建失败；
      Hugo / Astro 对中文文件名也各有坑。
      所以文件名统一用 ASCII：截取标题里的英文数字，没有就问一个。
    """
    s = title.strip()
    # 全角/标点先净化
    trans = {
        "：": " ", "？": " ", "！": " ", "，": " ", "。": " ",
        "、": " ", "；": " ", "“": "", "”": "", "《": "", "》": "",
        "（": " ", "）": " ", "　": " ",
    }
    for k, v in trans.items():
        s = s.replace(k, v)
    # 只保留 ASCII 字母数字和空格/连字符
    s = re.sub(r"[^A-Za-z0-9\s\-]", " ", s)
    s = re.sub(r"[\s\-]+", "-", s).strip("-.").lower()
    return s[:60]


def main():
    os.makedirs(POSTS, exist_ok=True)

    print()
    print("=" * 64)
    print("  新建文章")
    print("=" * 64)
    print()

    title = ""
    while not title:
        title = ask("标题")

    now = datetime.datetime.now()
    default_date = now.strftime("%Y-%m-%d %H:%M:%S")
    date = ask("日期时间", default_date)

    tags_raw = ask("标签（多个用逗号隔开，可留空）")
    tags = [t.strip() for t in re.split(r"[,，]", tags_raw) if t.strip()]

    category = ask("分类（单个词，可留空）")
    summary = ask("摘要（一句话，可留空）")

    pinned = ask_yes("要置顶吗", "n")
    cover = ""
    if not pinned:
        cover = ask("封面图地址（可留空用默认图）")

    # 文件名（URL 用）：中文标题没法直接当文件名，让用户给个英文短名
    slug = slugify(title)
    if not slug:
        print()
        print("  （标题是中文，URL 里需要一段英文短名，比如 hexo-setup）")
        while True:
            slug = slugify(ask("英文短名（用 - 连接，如 my-first-post）"))
            if slug:
                break
            print("  这个不能为空，再试一次。")

    path = os.path.join(POSTS, slug + ".md")
    n = 2
    while os.path.exists(path):
        path = os.path.join(POSTS, f"{slug}-{n}.md")
        n += 1

    tag_s = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
    fm = [
        "---",
        f'title: "{title}"',
        f"date: {date}",
        f"tags: {tag_s}",
        f'category: "{category}"',
        f'summary: "{summary}"',
        f"pinned: {'true' if pinned else 'false'}",
        "draft: false",
        f'cover: "{cover}"',
        "---",
        "",
        "在这里开始写正文。",
        "",
        "## 小标题",
        "",
        "正文内容……",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(fm))

    print()
    print("-" * 64)
    print("  已创建：", os.path.relpath(path, ROOT))
    print("-" * 64)
    print()
    print("  现在会用记事本打开，写完后【保存 + 关掉记事本】再回到这里。")
    print()

    # 打开编辑器；任何失败都不影响后续流程
    try:
        os.startfile(path)
    except Exception:
        pass

    try:
        input("  写完 + 保存后，按回车继续发布...")
    except EOFError:
        pass
    print()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n已取消。")
        sys.exit(1)
    except OSError as e:
        print(f"\n[错误] {e}")
        sys.exit(1)
