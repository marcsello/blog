import os.path
import os


def list_post_dirs(posts_dir: str):
    for post_dir in os.listdir(posts_dir):
        meta_file = os.path.join(posts_dir, os.path.join(post_dir, "meta.yaml"))
        if not os.path.isfile(meta_file):
            continue
        yield meta_file


def load_post_meta(post_dir: str):
    pass
