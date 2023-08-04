import os


class Config:
    POSTS_SOURCE_DIR = os.environ.get("POSTS_SOURCE_DIR", "posts")
    TEMPLATES_SOURCE_DIR = os.environ.get("TEMPLATES_SOURCE_DIR", "templates")
    PUBLIC_SOURCE_DIR = os.environ.get("PUBLIC_SOURCE_DIR", "public")
    OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "_dist")

    POST_SRC_META_FILE_NAME = os.environ.get("POST_SRC_META_FILE_NAME", "meta.yaml")
    POST_SRC_CONTENT_FILE_NAME = os.environ.get("POST_SRC_CONTENT_FILE_NAME", "content.md")
    RSS_FILE_PATH = "rss.xml"

    URL_BASE = os.environ.get("URL_BASE", "https://blog.marcsello.com/")
    INCLUDE_UNPUBLISHED = os.environ.get("INCLUDE_UNPUBLISHED", "0").lower() in ['1', 'yes', 'true']
