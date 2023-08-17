import random
import zlib
from .posts import Post


def find_related_posts(post: Post, posts: list[Post]):
    id_hash = zlib.adler32(post.id.encode("utf-8"))  # python's hash() is non-deterministic between runs
    rnd = random.Random(id_hash)  # seed random to be deterministic
    related_posts = []

    # first, don't include the post itself
    posts_no_self = list(
        filter(lambda p: p.id != post.id, posts)
    )

    # find the latest post
    # in theory the posts are already ordered, but let's not build on assumptions
    latest_post = max(posts_no_self, key=lambda p: p.meta['publish_date'])
    related_posts.append(latest_post)

    # then separate them based on tags similarity (don't include the latest one)
    tags_set = set(post.meta['tags'])
    similar_tag_posts = []
    unsimilar_tag_posts = []
    for p in posts_no_self:
        if p.id == latest_post.id:
            # the latest post will always be included, so we don't need to include that
            continue

        if tags_set.intersection(set(p.meta['tags'])):
            similar_tag_posts.append(p)
        else:
            unsimilar_tag_posts.append(p)

    # include max 3 more, try to add at least 2 with similar tags and one with unsimilar
    target = 3
    include_from_similar = min(target - min(1, len(unsimilar_tag_posts)), len(similar_tag_posts))
    include_from_unsimilar = min(target - include_from_similar, len(unsimilar_tag_posts))

    # add the ones that are similar
    related_posts.extend(rnd.sample(similar_tag_posts, k=include_from_similar))

    # add the one(s) that are unsimilar
    related_posts.extend(rnd.sample(unsimilar_tag_posts, k=include_from_unsimilar))

    # shuffle them well
    rnd.shuffle(related_posts)

    return related_posts
