import os.path
from typing import Generator

import os

from .config import Config
from .meta import load_meta_file

from dataclasses import dataclass


@dataclass
class PostRepr:
    id: str
    source_dir: str
    output_dir: str
    meta: dict


def iter_posts(posts_dir: str) -> Generator[PostRepr, None, None]:
    for post_dir in os.listdir(posts_dir):
        source_dir = os.path.join(posts_dir, post_dir)
        meta_file_path = os.path.join(source_dir, Config.POST_SRC_META_FILE_NAME)

        if not os.path.isfile(meta_file_path):
            print(" >", post_dir, "missing meta file, skipping")
            continue

        if not os.path.isfile(os.path.join(source_dir, Config.POST_SRC_CONTENT_FILE_NAME)):
            print(" >", post_dir, "missing content file, skipping")
            continue

        meta = load_meta_file(meta_file_path)

        if not meta['published']:
            if not Config.INCLUDE_UNPUBLISHED:
                print(" >", post_dir, "is unpublished, skipping")
                continue

        subfolder = "_"
        if meta['published']:
            subfolder = str(meta['publish_date'].year)

        output_rel_path = os.path.join(os.path.join("posts", subfolder), post_dir)

        yield PostRepr(
            id=post_dir,
            source_dir=source_dir,
            output_dir=output_rel_path,
            meta=meta
        )

