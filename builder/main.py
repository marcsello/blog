import os.path
from datetime import datetime

from .config import Config
from .output import LocalDirOutput
from .posts import iter_posts
from .markdown_magic import render_markdown
from .rss import generate_rss

import jinja2


def main():
    build_timestamp = datetime.now()
    print("start", build_timestamp)
    print("init jinja2 env")
    print(" * reading templates from", Config.TEMPLATES_SOURCE_DIR)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(Config.TEMPLATES_SOURCE_DIR))
    jinja_env.globals.update(site={
        "url_base": Config.URL_BASE,
        "build_timestamp": build_timestamp,
    })

    print("init output")
    o = LocalDirOutput(Config.OUTPUT_DIR)
    print("copy public")
    o.add_folder("public", ".")
    print("read posts")
    posts = []
    for post in iter_posts(Config.POSTS_SOURCE_DIR):
        # post id is the name of the directory
        print(" >", post.id)
        posts.append(post)

    print("extract tags")
    tags = set()
    for post in posts:
        tags.update(set(post.meta['tags']))

    for tag in tags:
        print(" *", tag)

    print("sort and organize posts")
    posts.sort(key=lambda p: p.meta['publish_date'], reverse=True)

    print("render index")
    template = jinja_env.get_template("index.html.j2")

    ctx = {
        "posts": posts  # all posts ordered by date
    }

    o.write_file(template.render(ctx), "index.html")
    print("render lists")
    template = jinja_env.get_template("list.html.j2")
    for tag in tags:
        print(" *", tag)
        posts_with_tag = list(filter(lambda p: tag in p.meta['tags'], posts))
        ctx = {
            "posts": posts_with_tag  # all posts ordered by date
        }
        o.write_file(template.render(ctx), os.path.join("tag", tag + ".html"))

    print("render posts")
    template = jinja_env.get_template("post.html.j2")
    for post in posts:
        print(" *", post.id)

        with open(os.path.join(post.source_dir, Config.POST_SRC_CONTENT_FILE_NAME)) as f:
            markdown_str = f.read()
        html_str, referenced_resources = render_markdown(markdown_str)

        ctx = {
            "post": post,
            "content": html_str
        }

        o.write_file(template.render(ctx), os.path.join(post.output_dir, "index.html"))

        available_files = os.listdir(post.source_dir)
        for res in referenced_resources:
            if res.startswith("http://"): # noqa
                print(" > [WARNING] HTTP RESOURCE LINKED:", res)
                continue  # nothing to copy, skip

            if res.startswith("https://"):
                continue  # nothing to copy, skip

            if res not in available_files:
                continue  # nothing to copy, skip

            o.add_file(os.path.join(post.source_dir, res), os.path.join(post.output_dir, res))

    print("generate rss")
    o.write_file(generate_rss(posts[:5]), Config.RSS_FILE_PATH)
