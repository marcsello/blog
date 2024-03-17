<!-- cspell:ignore Webploy -->
This is a follow-up post to my previous writing on [Building this blog](/posts/2023/building-this-blog/). In that post I've used a simple shell script and [webhook](https://github.com/adnanh/webhook) to facilitate the deployment process from the web server side. This post is about how I turned that shell script into a whole new project.

# Problems with the original Webploy script

Since I've created the original shell script which just takes the uploaded TAR file, extracts it to a new directory and updates a symlink, I've been thinking to myself "how could I improve on it". I've identified some (pain) points, that I summarize bellow.

## Lack of proper configuration

My initial design was really just a simple shell script. I've "hard-coded" almost every path, filename command, etc. in it.

This was fine, for it's original purpose of deploying a single blog. But as I worked on more projects, that involved deploying static sites, the convenience of deploying the with a simple, set-and-forget CI job, was more and more tempting. So I started hacking the shell script to handle multiple sites, with multiple different configurations and needs, which quickly become a mess.

While deploying a static site isn't really different from another, there might still be tiny differences. And when you are deploying more than 2 sites like this, it would be nice to gather all those tiny things in one place, where you can see trough and edit all of them.

So I really needed a proper configuration file or something (Also something that I can easily manage with [Ansible](https://www.ansible.com/)).

## Lifecycle of deployments is unclear (and also hacky)

The original script had a single flow, that was basically just extracting all files to a new directory, and then update the symlink that points to it.

![]()

This is simple enough, but there comes a bunch of what-ifs which might question if it's the best approach here.

Let's say, **what if** the client, that is in the middle of uploading the files crashed or lost connection? Or **what if** the client realized the files were broken after uploading it (for example the job that generated the files hasn't finished yet)? Originally there were really no way to tell the server, to abort the deployment process. In a perfect world, we wouldn't need this option, but in reality, this seems like a pretty valid use-case. So originally I've hacked together a "sealing" mechanism, which basically adds an empty file, named `__SEAL__` to the end of the TAR file, and the server only proceeds with the deployment if this file exists in the received archive, otherwise it just deletes the received files.

Okay, but **what if** we had a super-smart client, that might want to retry uploading the files (this is usually a bad pattern in the CI world, it's simpler to retry the whole job, but there might be cases where this is a valid concern)? Each deployment is strongly tied to a single HTTP request, if it breaks somehow, the entire process has to be re-started. If we try to de-couple these two things, the scope of the problem will just blow up... **What if** a client tries to modify the live version? **What if** there is a legit file named `__SEAL__` in the deployment? **What if** we never receive a seal? **What if** a client tries to upload files a non-existent deployment (maybe the deployment was deleted during the process)?

It is easy to see, that this flow became more like a burden, which can not be improved easily, once we try to extend it, we will run into more design problems that has to be addressed than we started off with.

## Deployment administration is still manual work

I think, keeping a previous version of the deployment still available on the web-server is a good thing. It might take 2-3x more disk space than a single site, but it is super-easy to roll back, a deployment in case something goes wrong. Maybe some advanced workflows can even take advantage of having multiple versions of a site that can be switched with a simple symlink update.

But that symlink still has to be updated "manually". By that, I mean, there is no first-party support from the webploy script to manipulate the symlink other than updating it to point to the new deployment. So if we want to take advantage of having multiple deployments ready, we still have to log in to that machine and run some commands, that is really one of the pain points I wanted to elevate in the first place.

So in order for storing multiple deployments to make sense, we really need to have the same convenience when rolling back deployments as we have with uploading new deployments.

## Security

Some of the above points I've described could easily manifest into security problems as well. But besides that we are still talking about a shell script that takes it's input from the wild internet. Even trough I did all I could, it was hard to sleep with this tough on my mind. I wanted perfect validation at every point of the script with proper authentication, and authorization, and most importantly logging of what's going on on my server. But this were all missing. A simple symmetric API key was what separated my script from anyone passing by. Even trough I'm not expecting anyone to actively exploit my solution, a bit more focus on the security side of things would certainly be a nice addition.

# Re-inventing the wheel (again)

# Self-imposed limitations

 - want to keep this good for small sites with a single webserver
