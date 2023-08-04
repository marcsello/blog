import marko
import marko.inline


def _extract_all_src(root) -> list:
    srcs = []

    if isinstance(root, marko.inline.Image) or isinstance(root, marko.inline.Link):
        srcs.append(root.dest)

    if hasattr(root, 'children'):
        for elm in root.children:
            srcs.extend(_extract_all_src(elm))

    return srcs


def render_markdown(markdown_str: str) -> tuple[str, list[str]]:  # html_str, referenced_resources
    md = marko.Markdown()
    doc = md.parse(markdown_str)

    res_list = _extract_all_src(doc)

    html_str = md.render(doc)

    return html_str, res_list
