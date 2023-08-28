So I've been thinking for a while of creating this blog. But I tend to over-engineer my ideas, which usually result in me planning and designing things for weeks and ending up not building anything.
I've decided I'll keep things at a minimum so that I could actually come up with an [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) and improve later. 


All I want now is to write cool [Markdown](https://en.wikipedia.org/wiki/Markdown) files, with some metadata, maybe include some pictures, and turn all this into a pile of HTML and CSS.

But if that is all for it, it wouldn't really make sense of writing a whole blog post about it. So, let's see how could I still sneak in some pointless engineering to such a simple thing.

# Useful abstraction: The CMS

The Content Management System (or CMS for short) is actually a pretty vital part of every website that's primary focus is to share information in a somewhat unified fashion.
Think of any news outlets, it would be very unconventional for every writer to edit the HTML code of a page to publish their article. And it would be even more of a nightmare to run such a site.

So we need something inbetween, where at one side, writers can focus on writing their posts without even thinking of what's going under the hoods. And something for the site builders that functions as a text repository that they can use to fill up their website with content. This is where CMS systems come into play.

There are at least a hundred CMS solutions out there, both that include the site rendering functionality (such as [WordPress](https://wordpress.org/), [Drupal](https://www.drupal.org/), [Joomla](https://www.joomla.org/), [e107](https://e107.org/), etc.) and without it (such as [Strapi](https://strapi.io/), [Keystone](https://keystonejs.com/) and [many others](https://jamstack.org/headless-cms/)...). Those are so-called [headless CMSes](https://www.netlify.com/blog/complete-guide-to-headless-cms/), and the cool thing about them is that you can basically build any solution on them to render your website exactly how you like. And as the tinkerer I am, this is something I love.

_But, how simple can a CMS really be?_

Well, if you think of it... even a simple git repository can be a CMS, right? You can place the article texts in neatly organized folders, along with some metadata and other assets for that post. It's not just super-simple but allows having some great features at no cost! With git, you can have commits, branches, synchronization at ease, and what's possibly the coolest is that you can use all the other awesome tools built on Git as well... like free public hosting such as [GitHub](https://github.com/) or [GitLab](https://gitlab.com/), CI/CD solutions, Issues, Comments, Pull/Merge requests, enhanced collaboration tools, IDEs and many others. Those are features that even the paid CMS solutions sometimes fail to deliver properly (to be fair, most of those rarely needed in the publishing industry). It's a marvel of a simple solution that can be extended to infinity and beyond.  

_And that's exactly what I need!_ 

As a developer I'm already familiar with these tools. And I love the idea of having this many possibilities to experiment with. While a blog's main function to deliver articles to its readers, this is still a project of mine, and as such, I want to have fun building and maintaining it to unreasonable levels...
If I were tasked to build something for a publishing collective, I am most certain that I would take a different approach.

# Problems I've invented for myself
