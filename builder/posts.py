import os
import os.path
from typing import Generator, Optional

import marko
import marko.inline

from .config import Config
from .meta import load_meta_file

_MD = marko.Markdown()

def _extract_all_src(root) -> list:
    srcs = []

    if isinstance(root, marko.inline.Image) or isinstance(root, marko.inline.Link):
        srcs.append(root.dest)

    if hasattr(root, 'children'):
        for elm in root.children:
            srcs.extend(_extract_all_src(elm))

    return srcs

def _extract_first_paragraph_text(root) -> str:
    return "" # TODO

def _get_first_image_path(root) -> Optional[str]:

    if isinstance(root, marko.inline.Image):
        return root.dest

    if hasattr(root, 'children'):
        for elm in root.children:
            img = _get_first_image_path(elm)
            if img:
                return img
    
    return None


class Post:
    def __read_markdown(self) -> str:
        with open(os.path.join(self.source_dir, Config.POST_SRC_CONTENT_FILE_NAME)) as f:
            return f.read()
            
    def __doc(self):
        # TODO: cache
        return _MD.parse(self.__read_markdown()) 

    def __init__(self, id_:str):
        self._id = id_

        # source dir
        self._source_dir = os.path.join(Config.POSTS_SOURCE_DIR, id_)

        # load meta
        meta_file_path = os.path.join(self._source_dir, Config.POST_SRC_META_FILE_NAME)
        self._meta = load_meta_file(meta_file_path)

        # output_dir
        subfolder = "_"
        if self._meta['published']:
            subfolder = str(self._meta['publish_date'].year)

        self._output_dir = os.path.join(os.path.join("posts", subfolder), id_)

        # cover, intro
        if 'cover_override' in self._meta and self._meta['cover_override']:
            self._cover = self._meta['cover_override']
        else:
            self._cover = _get_first_image_path(self.__doc())

        if 'intro_override' in self._meta and self._meta['intro_override']:
            self._intro = self._meta['intro_override']
        else:
            self._intro = _extract_first_paragraph_text(self.__doc())
            if len(self._intro) > 256:
                self._intro = self._intro[:253] + "..."
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def source_dir(self) -> str:
        return self._source_dir

    @property
    def output_dir(self) -> str:
        return self._output_dir
    
    @property
    def meta(self) -> dict:
        return self._meta
    
    @property
    def cover(self) -> str:
        return self._cover
    
    @property
    def intro(self) -> str:
        return self._intro

    def html(self) -> str:
        return _MD.render(self.__doc())

    def attached_files(self) -> list[str]:
        l = os.listdir(self.source_dir)
        l.remove(Config.POST_SRC_META_FILE_NAME)
        l.remove(Config.POST_SRC_CONTENT_FILE_NAME)
        return l

    def referenced_resources(self) -> list[str]:
        return _extract_all_src(self.__doc())


def iter_posts() -> Generator[Post, None, None]:
    for post_id in os.listdir(Config.POSTS_SOURCE_DIR):
        post = Post(post_id)

        if not post.meta['published']:
            if not Config.INCLUDE_UNPUBLISHED:
                print(" >", post_dir, "is unpublished, skipping")
                continue

        print(" >", post.id)
        yield post
