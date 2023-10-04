import os
import os.path
from typing import Generator, Optional

import marko
import marko.inline

from .config import Config
from .meta import load_meta_file


class CustomRenderer(marko.HTMLRenderer):

    def render_paragraph(self, element: marko.block.Paragraph) -> str:
        if all(isinstance(c, marko.inline.Image) for c in element.children):
            # prevent the surrounding <p> tag when rendering a figure, because the figure tag can not be placed inside a p
            return self.render_children(element)
        else:
            return super().render_paragraph(element)

    def render_heading(self, element: marko.block.Heading) -> str:
        # Drop each heading one level bellow, because h1 is used for the main title only
        level_override = element.level + 1
        if level_override > 6:
            level_override = 6

        return f"<h{level_override}>{self.render_children(element)}</h{level_override}>\n"

    def render_image(self, element: marko.inline.Image) -> str:
        url = self.escape_url(element.dest)

        if element.dest.endswith(".mp4"):  # we treat mp4 like gif...
            figure_content = f"""<video autoplay loop muted playsinline><source src="{url}" type="video/mp4"></video>"""
        else:
            img_str = super().render_image(element)
            figure_content = f"""<a target="_blank" href="{url}">{img_str}</a>"""

        # we re-use title as caption
        figcaption = ""
        if element.title:
            figcaption = f"<figcaption>{self.escape_html(element.title)}</figcaption>"

        return f"""<figure>{figure_content}{figcaption}</figure>"""


_MD = marko.Markdown(renderer=CustomRenderer)


def _extract_all_src(root) -> list:
    srcs = []

    if isinstance(root, marko.inline.Image) or isinstance(root, marko.inline.Link):
        srcs.append(root.dest)

    if hasattr(root, 'children'):
        for elm in root.children:
            srcs.extend(_extract_all_src(elm))

    return srcs


def _extract_first_paragraph_text(root) -> str:
    for child in root.children:
        if isinstance(child, marko.block.Paragraph):
            paragraph_str = ""
            for part in child.children:
                if isinstance(part, marko.inline.RawText) and isinstance(part.children, str):
                    paragraph_str += part.children
                if isinstance(part, marko.inline.LineBreak):
                    if paragraph_str[-1:] != " ":
                        paragraph_str += " "
                if isinstance(part, marko.inline.Link):  # TODO: a recursive approach would be better here...
                    for part_child in part.children:
                        if isinstance(part_child, marko.inline.RawText) and isinstance(part_child.children, str):
                            paragraph_str += part_child.children

            return paragraph_str  # return after the first paragraph

    return ""


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

    def __init__(self, id_: str):
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
            intro_str = _extract_first_paragraph_text(self.__doc())
            if len(intro_str) > 320:
                intro_str = intro_str[:320]  # cut to length
                # first try to cut at the last period, if it's not too far...
                last_dot_pos = intro_str.rfind(".")
                if 320 - last_dot_pos > 100:
                    intro_str = intro_str[:last_dot_pos + 1]
                else:
                    intro_str += "..."  # If too far, just add more dots

            self._intro = intro_str

    @property
    def id(self) -> str:
        """
        id is basically the name of the folder the post were found in
        :return: id string
        """
        return self._id

    @property
    def source_dir(self) -> str:
        """
        source dir is basically the posts source dir + post id
        :return:
        """
        return self._source_dir

    @property
    def output_dir(self) -> str:
        """
        output dir is basically just "posts" + year + post_id
        year part is "_" for unpublished posts
        it is relative to the output dir
        :return:
        """
        return self._output_dir

    @property
    def meta(self) -> dict:
        """
        This is the direct, parsed version of the meta.yaml
        :return:
        """
        return self._meta

    @property
    def cover(self) -> str | None:
        """
        This is the
        :return:
        """
        return self._cover

    @property
    def intro(self) -> str:
        """
        Intro text for the post.
        First paragraph, or overridden value from the meta yaml
        :return:
        """
        return self._intro

    def html(self) -> str:
        """
        Rendered html document
        :return: html string
        """
        return _MD.render(self.__doc())

    def attached_files(self) -> list[str]:
        """
        List of files in the post's directory except the meta and content file
        Those files count as "attachments"
        :return:
        """
        listing = os.listdir(self.source_dir)
        listing.remove(Config.POST_SRC_META_FILE_NAME)
        listing.remove(Config.POST_SRC_CONTENT_FILE_NAME)
        return listing

    def referenced_resources(self) -> list[str]:
        """
        List of all the resources referenced directly in the content file
        (in form of links, or images)
        :return:
        """
        refs = _extract_all_src(self.__doc())

        if 'cover_override' in self._meta and self._meta['cover_override']:
            refs.append(self._meta['cover_override'])

        return refs


def iter_posts() -> Generator[Post, None, None]:
    for post_id in os.listdir(Config.POSTS_SOURCE_DIR):
        post = Post(post_id)

        if not post.meta['published']:
            if not Config.INCLUDE_UNPUBLISHED:
                print(" >", post_id, "is unpublished, skipping")
                continue

        print(" >", post.id)
        yield post
