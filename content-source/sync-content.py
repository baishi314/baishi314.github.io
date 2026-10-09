# -*- coding: utf-8 -*-
"""
三站内容同步器
==============
唯一内容源：content-source/{profile,projects,resources}.json + posts/

运行：
    python content-source/sync-content.py          # 同步全部
    python content-source/sync-content.py --check  # 只检查是否一致

每套主题有自己的「语气」和 frontmatter 格式，正文保持一致。
"""
import os
import re
import sys
import json
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "content-source")

# ------------------------------------------------------------------
# 三套站点的语气设定：标题/摘要按主题微调，正文不动
# ------------------------------------------------------------------
FLAVOR = {
    "minimal": {
        "label": "极简笔记",
        "site_name": "极简笔记",
        "hello_title": "Hello World：给博客开个头",
        "hello_summary": "第一篇文章，说说为什么又要折腾一个博客。",
        "welcome_title": None,  # minimal 不放欢迎文
    },
    "anime": {
        "label": "二次元小屋",
        "site_name": "二次元小屋",
        "hello_title": "欢迎来到二次元小屋",
        "hello_summary": "这个版本的博客用了 Firefly 主题，记录一下怎么搭起来的。",
        "welcome_title": "欢迎来到二次元小屋",
    },
    "xinghui": {
        "label": "星辉小屋",
        "site_name": "星辉小屋",
        "hello_title": "开站啦！这里是 baishi314 的小窝",
        "hello_summary": "第一篇博客，聊聊这个站怎么来的。",
        "welcome_title": None,
    },
}


def load(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------
# 文章：单一源 content-source/posts/*.md
# 作者只写一份统一的 frontmatter，这里翻译成三站各自的格式
# ------------------------------------------------------------------
POSTS_DIR = os.path.join(SRC, "posts")

# 统一 frontmatter 字段：
#   title / date / tags / category / summary / pinned / draft / cover
_UNQUOTE = re.compile(r'^["\'](.*)["\']$')


def _parse_scalar(v):
    v = v.strip()
    m = _UNQUOTE.match(v)
    if m:
        return m.group(1)
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    return v


def _parse_list(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        v = v[1:-1]
    if not v.strip():
        return []
    parts = re.split(r",(?![^\[]*\])", v)
    out = []
    for p in parts:
        p = _parse_scalar(p.strip())
        if p != "":
            out.append(str(p))
    return out


def parse_post(path):
    """解析统一格式的文章，返回 (meta dict, body str)"""
    raw = open(path, encoding="utf-8").read()
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    fm = raw[3:end].strip("\n")
    body = raw[end + 4:].lstrip("\n")

    meta = {}
    for line in fm.splitlines():
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if k in ("tags", "categories"):
            meta[k] = _parse_list(v)
        else:
            meta[k] = _parse_scalar(v)
    # 归一化
    meta.setdefault("title", "无标题")
    meta.setdefault("tags", [])
    meta.setdefault("category", "")
    meta.setdefault("summary", "")
    meta.setdefault("pinned", False)
    meta.setdefault("draft", False)
    meta.setdefault("cover", "")
    meta.setdefault("date", "2026-01-01 00:00:00")
    return meta, body


def load_posts():
    """读 content-source/posts/*.md，按日期倒序"""
    if not os.path.isdir(POSTS_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(POSTS_DIR)):
        if not fn.endswith((".md", ".mdx")):
            continue
        meta, body = parse_post(os.path.join(POSTS_DIR, fn))
        meta["slug"] = fn.rsplit(".", 1)[0]
        meta["body"] = body
        out.append(meta)
    out.sort(key=lambda m: str(m["date"]), reverse=True)
    return out


def _yaml_date(d):
    """2026-10-08 10:00:00 -> (quoted str, date-only str)"""
    s = str(d).strip()
    dateonly = s.split(" ")[0]
    return s, dateonly


def _yaml_str(s):
    s = str(s).replace('"', '\\"')
    return f'"{s}"'


# ---------------- 三站 frontmatter 生成 ----------------

def fm_minimal(m):
    """Hugo / PaperMod"""
    s, dateonly = _yaml_date(m["date"])
    tags = m["tags"] or []
    tag_s = "[" + ", ".join(_yaml_str(t) for t in tags) + "]"
    cats = [m["category"]] if m["category"] else []
    cat_s = "[" + ", ".join(_yaml_str(c) for c in cats) + "]"
    lines = [
        "---",
        f"title: {_yaml_str(m['title'])}",
        f"date: {dateonly}",
        "draft: false",
        f"tags: {tag_s}",
        f"categories: {cat_s}",
    ]
    if m["summary"]:
        lines.append(f"summary: {_yaml_str(m['summary'])}")
    if m["pinned"]:
        lines += ["weight: 1", "pin: true"]
    lines += ["---", ""]
    return "\n".join(lines)


def fm_anime(m):
    """Astro / Firefly"""
    lines = [
        "---",
        f"title: {m['title']}",
        f"published: {m['date']}",
    ]
    if m["summary"]:
        lines.append(f"description: {m['summary']}")
    if m["cover"]:
        lines.append(f"image: {m['cover']}")
    tags = m["tags"] or []
    lines.append("tags: [" + ", ".join(str(t) for t in tags) + "]")
    if m["category"]:
        lines.append(f"category: {m['category']}")
    lines.append("draft: false")
    if m["pinned"]:
        lines.append("pinned: true")
    lines.append("comment: true")
    lines += ["---", ""]
    return "\n".join(lines)


def fm_xinghui(m):
    """Next.js / 星辉小屋"""
    lines = [
        "---",
        f"title: {_yaml_str(m['title'])}",
        f'date: "{m["date"]}"',
    ]
    if m["summary"]:
        lines.append(f"description: {_yaml_str(m['summary'])}")
    lines.append(f'cover: "{m["cover"] or "/cover-default.svg"}"')
    tags = m["tags"] or []
    lines.append("tags: [" + ", ".join(_yaml_str(t) for t in tags) + "]")
    if m["pinned"]:
        lines.append("pinned: true")
    lines += ["---", ""]
    return "\n".join(lines)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("  WROTE", os.path.relpath(path, ROOT))


def rm(path):
    if os.path.exists(path):
        os.remove(path)
        print("  RM   ", os.path.relpath(path, ROOT))


# ------------------------------------------------------------------
# 正文渲染：三站共用同一段 markdown 骨架
# ------------------------------------------------------------------
def render_about(p):
    """关于我正文（不含 frontmatter）"""
    out = []
    out.append("## whoami\n")
    out.append(p["intro"] + "\n")
    out.append(p["intro2"] + "\n")
    out.append(p["route"] + "\n")
    out.append("| | |")
    out.append("|---|---|")
    for k, v in p["facts"]:
        out.append(f"| **{k}** | {v} |")
    out.append("")
    out.append("---\n")
    out.append("## 技能栈\n")
    for name, items in p["skills"]:
        out.append(f"### {name}\n")
        out.append(" ".join(f"`{i}`" for i in items) + "\n")
    out.append("---\n")
    out.append("## 项目作品\n")
    for pr in load("projects.json"):
        out.append(f"### {pr['name']}\n")
        out.append(pr["desc"] + "\n")
        out.append(" ".join(f"`{t}`" for t in pr["tags"]) + "\n")
    out.append("---\n")
    out.append("## 联系我\n")
    for label, text, url in p["contact"]:
        out.append(f"- **{label}** — [{text}]({url})")
    out.append("")
    out.append("---\n")
    out.append("## 请我喝杯咖啡\n")
    out.append("如果这里的内容帮到了你，可以扫下面的码。\n")
    return "\n".join(out)


def render_about_qr(theme):
    """各站的赞赏码图片地址"""
    return (
        f'\n<img src="https://baishi314.github.io/{theme}/images/wechat-pay.png" '
        f'alt="微信收款码" style="max-width:260px;border-radius:12px;">\n'
    )


def count_rows(r):
    """统计全部链接条数（兼容平铺 section 与 groups 分组 section）"""
    n = 0
    for s in r["sections"]:
        if "groups" in s:
            n += sum(len(g["rows"]) for g in s["groups"])
        else:
            n += len(s["rows"])
    return n


def _render_rows(rows):
    """渲染一张资源表格（三列：网站 / 是什么 / 直接进）"""
    out = ["| 网站 | 是什么 | 直接进 |", "|---|---|---|"]
    for name, desc, url, label in rows:
        out.append(f"| **{name}** | {desc} | [{label}]({url}) |")
    out.append("")
    return out


def render_resources(r, theme):
    """资源导航正文

    一个 section 有两种写法：
      - 平铺：{"emoji": ..., "name": ..., "rows": [...]}
      - 分组：{"emoji": ..., "name": ..., "groups": [{"name": ..., "rows": [...]}, ...]}
    分组用于顶层分类内部还需再分小类的情况（如「编程语言 → C++ → STL 专题」）。
    """
    out = []
    out.append("> " + r["intro"] + "\n")
    out.append("---\n")
    for sec in r["sections"]:
        out.append(f"## {sec['emoji']} {sec['name']}\n")
        if "groups" in sec:
            for g in sec["groups"]:
                out.append(f"### {g['name']}\n")
                out.extend(_render_rows(g["rows"]))
        else:
            out.extend(_render_rows(sec["rows"]))
        out.append("---\n")
    out.append(r["outro"] + "\n")
    return "\n".join(out)


# ------------------------------------------------------------------
# 主题 1：PaperMod (Hugo)
# ------------------------------------------------------------------
def sync_minimal(p, r, projs, fl):
    base = os.path.join(ROOT, "minimal-src", "content")
    print("\n[minimal / PaperMod]")

    # 关于我
    fm = (
        '---\n'
        'title: "关于我"\n'
        'date: 2026-10-05\n'
        'draft: false\n'
        'ShowToc: false\n'
        'ShowBreadCrumbs: true\n'
        'hidemeta: true\n'
        'comments: false\n'
        '---\n\n'
    )
    write(os.path.join(base, "about.md"),
          fm + render_about(p) + render_about_qr("minimal"))

    # 资源导航（置顶）
    fm = (
        '---\n'
        f'title: "{r["title"]}"\n'
        f'date: {r["date"]}\n'
        'draft: false\n'
        'tags: ["资源", "导航"]\n'
        'categories: ["导航"]\n'
        f'summary: "{r["summary"]}"\n'
        'ShowToc: true\n'
        'TocOpen: true\n'
        'weight: 1\n'
        'pin: true\n'
        '---\n\n'
    )
    write(os.path.join(base, "posts", "resources.md"), fm + render_resources(r, "minimal"))

    # 开篇文
    fm = (
        '---\n'
        f'title: "{fl["hello_title"]}"\n'
        'date: 2026-10-05\n'
        'draft: false\n'
        'tags: ["随笔"]\n'
        'categories: ["日常"]\n'
        f'summary: "{fl["hello_summary"]}"\n'
        '---\n\n'
    )
    write(os.path.join(base, "posts", "hello-world.md"), fm + render_hello(fl))

    # 用户文章（content-source/posts/）
    sync_theme_posts("minimal", os.path.join(base, "posts"), fm_minimal)


def render_hello(fl):
    return (
        "折腾博客这件事，本身就是个坑。但坑归坑，还是想有个地方把东西沉淀下来。\n\n"
        "## 为什么写\n\n"
        "遇到的问题、踩过的坑、想明白的事，散在聊天记录和本地笔记里，过一阵就找不到了。\n"
        "写下来，一来是自己以后能翻，二来是万一能帮到别人。\n\n"
        "## 这里有什么\n\n"
        "- **文章**：学习笔记、踩坑记录、解决办法\n"
        "- **杂谈**：碎片式的想法，随手记\n"
        "- **资源**：好用的网站整理，见置顶那篇\n\n"
        "## 关于风格\n\n"
        "同一个我，现在有三套皮的站：极简笔记、二次元小屋、星辉小屋。\n"
        "内容是一样的，只是看着心情不同。从[风格大厅](https://baishi314.github.io/)都能进。\n\n"
        "慢慢写吧。\n"
    )


# ------------------------------------------------------------------
# 通用文章同步：把 content-source/posts/*.md 渲染进某个主题的 posts 目录
# ------------------------------------------------------------------
# 这三篇由脚本按主题生成，不由 content-source/posts/ 管理，避免冲突
GENERATED_SLUGS = {"resources", "hello-world", "welcome"}


def sync_theme_posts(theme, posts_dir, fm_fn, extra_skip=()):
    """
    把 content-source/posts/ 的文章写进目标目录。
    theme: 站点标识（仅用于日志）
    posts_dir: 目标 posts 目录
    fm_fn: frontmatter 生成函数
    """
    os.makedirs(posts_dir, exist_ok=True)
    posts = load_posts()
    if not posts:
        print(f"  (posts 源为空)")
        return 0

    written = []
    for m in posts:
        if m["slug"] in GENERATED_SLUGS or m["slug"] in extra_skip:
            continue
        if m.get("draft") is True:
            rm(os.path.join(posts_dir, m["slug"] + ".md"))
            continue
        write(os.path.join(posts_dir, m["slug"] + ".md"),
              fm_fn(m) + m["body"].rstrip() + "\n")
        written.append(m["slug"])

    # 清掉源里已删除的文章（只清脚本管的那些）
    keep = set(written) | set(GENERATED_SLUGS) | set(extra_skip)
    for fn in os.listdir(posts_dir):
        if not fn.endswith((".md", ".mdx")):
            continue
        slug = fn.rsplit(".", 1)[0]
        if slug not in keep:
            rm(os.path.join(posts_dir, fn))

    print(f"  posts: {len(written)} 篇 -> {os.path.relpath(posts_dir, ROOT)}")
    return len(written)


# ------------------------------------------------------------------
# 主题 2：Firefly (Astro)
# ------------------------------------------------------------------
def sync_anime(p, r, projs, fl):
    base = os.path.join(ROOT, "anime-src", "src", "content")
    print("\n[anime / Firefly]")

    write(os.path.join(base, "spec", "about.md"),
          "---\ntitle: 关于我\n---\n\n" + render_about(p) + render_about_qr("anime"))

    fm = (
        '---\n'
        f'title: {r["title"]}\n'
        f'published: {r["date"]}\n'
        f'description: {r["summary"]}\n'
        'tags: [资源, 导航]\n'
        'category: 导航\n'
        'draft: false\n'
        'pinned: true\n'
        'comment: true\n'
        '---\n\n'
    )
    write(os.path.join(base, "posts", "resources.md"), fm + render_resources(r, "anime"))

    fm = (
        '---\n'
        f'title: {fl["welcome_title"]}\n'
        'published: 2026-10-05\n'
        f'description: {fl["hello_summary"]}\n'
        'tags: [Astro, 博客]\n'
        'category: 折腾记录\n'
        'draft: false\n'
        '---\n\n'
    )
    body = (
        "这是「风格大厅」里的第二个版本，用的是开源的 **Firefly** 主题。\n\n"
        "## 为什么是它\n\n"
        "前一个版本走极简路线，白底黑字。这个想换个活法——卡片、看板娘、页面转场，\n"
        "花哨一点，看着心情好。\n\n"
        + render_hello(fl)
    )
    write(os.path.join(base, "posts", "welcome.md"), fm + body)

    # 用户文章（content-source/posts/）
    sync_theme_posts("anime", os.path.join(base, "posts"), fm_anime,
                     extra_skip=("welcome",))

    # 项目集合（Firefly 的 projects 页面读这里）
    proj_dir = os.path.join(base, "projects")
    if os.path.isdir(proj_dir):
        shutil.rmtree(proj_dir)
    os.makedirs(proj_dir, exist_ok=True)
    for i, pr in enumerate(projs, start=1):
        pfm = (
            '---\n'
            f'title: {pr["name"]}\n'
            f'published: 2026-10-0{min(i, 9)}\n'
            'draft: false\n'
            f'order: {i}\n'
            f'description: {pr["desc"]}\n'
            'image: ""\n'
            'tags: [' + ", ".join(pr["tags"]) + ']\n'
            'link: []\n'
            'status: 进行中\n'
            'lang: ""\n'
            '---\n\n'
        )
        write(os.path.join(proj_dir, f'{pr["id"]}.md'), pfm + pr["desc"] + "\n")


# ------------------------------------------------------------------
# 主题 3：星辉小屋 (Next.js)
# ------------------------------------------------------------------
def sync_xinghui(p, r, projs, fl):
    base = os.path.join(ROOT, "xinghui-src")
    print("\n[xinghui / Next.js]")

    # 关于我
    write(os.path.join(base, "app", "about", "about.md"),
          "---\ntitle: 关于我\ndate: '2026-10-05'\ntags: []\nmood: ''\n"
          "cover: /cover-default.svg\ndescription: ''\n---\n\n"
          + render_about(p)
          + "\n<img src=\"/images/wechat-pay.png\" alt=\"微信收款码\" "
            "style=\"max-width:260px;border-radius:12px;\">\n")

    # 资源导航
    fm = (
        '---\n'
        f'title: "{r["title"]}"\n'
        f'date: "{r["date"]} 12:00:00"\n'
        f'description: "{r["summary"]}"\n'
        'cover: "/cover-default.svg"\n'
        'tags: ["资源", "导航"]\n'
        'pinned: true\n'
        '---\n\n'
    )
    write(os.path.join(base, "posts", "resources.md"), fm + render_resources(r, "xinghui"))

    # 开篇文
    fm = (
        '---\n'
        f'title: "{fl["hello_title"]}"\n'
        'date: "2026-10-05 20:00:00"\n'
        f'description: "{fl["hello_summary"]}"\n'
        'cover: "/cover-default.svg"\n'
        'tags: ["日常", "开站"]\n'
        '---\n\n'
    )
    write(os.path.join(base, "posts", "hello-world.md"), fm + render_hello(fl))

    # 用户文章（content-source/posts/）
    sync_theme_posts("xinghui", os.path.join(base, "posts"), fm_xinghui)

    # 项目页（从 projects.json 生成 TS）
    lines = [
        "// 本文件由 content-source/sync-content.py 自动生成，请勿手改",
        "",
        "export type Project = {",
        "  id: string;",
        "  name: string;",
        "  description: string;",
        "  icon: string;",
        "  githubUrl: string;",
        "  tags: string[];",
        "};",
        "",
        "export const projectsData: Project[] = [",
    ]
    for pr in projs:
        lines.append("  {")
        lines.append(f'    id: "{pr["id"]}",')
        lines.append(f'    name: "{pr["name"]}",')
        lines.append(f'    githubUrl: "{pr["github"]}",')
        lines.append(f'    description: "{pr["desc"]}",')
        lines.append(f'    icon: "{pr["icon"]}",')
        lines.append("    tags: [" + ", ".join(f'"{t}"' for t in pr["tags"]) + "],")
        lines.append("  },")
    lines.append("];")
    lines.append("")
    write(os.path.join(base, "data", "projects.ts"), "\n".join(lines))

    # 站点简介同步
    cfg = os.path.join(base, "siteConfig.ts")
    t = open(cfg, encoding="utf-8").read()
    t = re.sub(r'bio: "[^"]*"', f'bio: "{p["bio"]}"', t)
    with open(cfg, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    print("  PATCH siteConfig.ts bio")


# ------------------------------------------------------------------
def main():
    check = "--check" in sys.argv
    p = load("profile.json")
    r = load("resources.json")
    projs = load("projects.json")

    print("=" * 60)
    print("内容源：", SRC)
    print(f"  profile.json    {len(p)} 字段")
    print(f"  projects.json   {len(projs)} 个项目")
    print(f"  resources.json  {count_rows(r)} 条链接，"
          f"{len(r['sections'])} 个分类")
    print("=" * 60)

    if check:
        print("\n（--check 模式：只列出内容源，不写入）")
        return

    sync_minimal(p, r, projs, FLAVOR["minimal"])
    sync_anime(p, r, projs, FLAVOR["anime"])
    sync_xinghui(p, r, projs, FLAVOR["xinghui"])

    print("\n" + "=" * 60)
    print("同步完成。三站正文一致，仅标题/措辞按主题微调。")
    print("=" * 60)


if __name__ == "__main__":
    main()
