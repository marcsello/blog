from urllib.parse import urljoin
from datetime import datetime, timezone

from feedgen.feed import FeedGenerator

from .posts import Post
from .config import Config


def generate_rss(posts: list[Post]) -> str:
    rss_link = urljoin(Config.URL_BASE, Config.RSS_FILE_PATH)

    fg = FeedGenerator()
    fg.id(Config.URL_BASE)
    fg.title("Marcsello's blog")
    fg.author({'name': 'Marcsello', 'email': 'marcsello@derpymail.org'})
    # fg.logo('http://ex.com/logo.jpg')
    fg.subtitle('My very own blog')
    fg.link(href=rss_link, rel='self')
    fg.language('en')
    for post in posts:

        post_link = urljoin(urljoin(Config.URL_BASE, post.output_dir), post.id) + "/"

        fe = fg.add_entry()
        fe.id(post_link)
        fe.title(post.meta['title'])
        fe.link(href=post_link)
        if post.meta['published']:
            dt = datetime.combine(post.meta['publish_date'], datetime.min.time(), tzinfo=timezone.utc)
            fe.updated(dt)

    return fg.rss_str(pretty=True).decode("utf-8")
