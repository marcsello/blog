import os.path
from datetime import datetime
from urllib.parse import urljoin

import output
from .config import Config
from .output_initializer import init_output
from .posts import iter_posts
from .rss import generate_rss
from .galaxy_brain import find_related_posts

import jinja2


def init_jinja_env(build_timestamp: datetime) -> jinja2.Environment:
    def _urljoin_filter(parts: list[str]) -> str:
        result = parts[0]
        for part in parts[1:]:
            result = urljoin(result, part)
        return result

    print(" * reading templates from", Config.TEMPLATES_SOURCE_DIR)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(Config.TEMPLATES_SOURCE_DIR))
    jinja_env.globals.update(site={
        "url_base": Config.URL_BASE,
        "build_timestamp": build_timestamp,
        "rss_feed_path": urljoin(Config.URL_BASE, Config.RSS_FILE_PATH),
        "config": {  # only pass "safe" keys
            "RSS_FILE_PATH": Config.RSS_FILE_PATH
        }
    })
    jinja_env.filters['urljoin'] = _urljoin_filter
    return jinja_env


def main():
    build_timestamp = datetime.now()
    print("start", build_timestamp)
    print("init output")
    o = init_output()
    try:
        run_build(o, build_timestamp)
    except:
        print("something went wrong, aborting output...")
        o.abort()
        raise

    print("closing output")
    o.close()

    print("done, took", datetime.now() - build_timestamp)


def run_build(o: output.OutputBase, build_timestamp: datetime):
    print("init jinja2 env")
    jinja_env = init_jinja_env(build_timestamp)
    print("copy public")
    o.add_folder("public", ".")
    print("read posts")
    posts = list(iter_posts())

    print("extract tags")
    tags = set()
    for post in posts:
        tags.update(set(post.meta['tags']))

    for tag in tags:
        print(" *", tag)

    ordered_tags = list(tags)
    ordered_tags.sort()

    jinja_env.globals.update(tags=ordered_tags)

    print("sort and organize posts")
    posts.sort(key=lambda p: p.meta['publish_date'], reverse=True)

    # == posts ==
    print("render posts")
    template = jinja_env.get_template("post.html.j2")
    for post in posts:
        print(" *", post.id)

        # generate some related posts
        related_posts = find_related_posts(post, posts)
        for rp in related_posts:
            print("   +", rp.id)

        ctx = {
            "post": post,
            "related_posts": related_posts
        }

        o.write_file(template.render(ctx), os.path.join(post.output_dir, "index.html"))

        available_files = post.attached_files()
        for res in post.referenced_resources():
            if res.startswith("http://"):  # noqa
                print(" > [WARNING] HTTP RESOURCE LINKED:", res)
                continue  # nothing to copy, skip

            if res.startswith("https://"):
                continue  # nothing to copy, skip

            if res not in available_files:
                continue  # nothing to copy, skip

            o.add_file(os.path.join(post.source_dir, res), os.path.join(post.output_dir, res))

    # == index ==
    print("render index")
    template = jinja_env.get_template("index.html.j2")

    ctx = {
        "posts": posts,  # all posts ordered by date
    }

    o.write_file(template.render(ctx), "index.html")

    # == lists ==
    print("render lists")
    template = jinja_env.get_template("list.html.j2")
    for tag in tags:
        print(" *", tag)
        posts_with_tag = list(filter(lambda p: tag in p.meta['tags'], posts))
        ctx = {
            "posts": posts_with_tag,  # all posts ordered by date
            "list_base": "TAG",
            "tag": tag,
        }
        o.write_file(template.render(ctx), os.path.join("tag", tag + ".html"))

    # finalizing steps
    print("generate rss")
    o.write_file(generate_rss(posts[:5]), Config.RSS_FILE_PATH)
