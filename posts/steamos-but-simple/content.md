Those who know me, aren't surprised when I simply ignore that there are better solutions to a problem, and start engineering my own solution to it. Sadly, this isn't the case here.

# My precious Steam Box

So, the story started back in 2017ish, when [Steam Deck](https://en.wikipedia.org/wiki/Steam_Deck) wasn't a thing yet, but Valve already invested a lot in Linux Gaming, and their [original SteamOS](https://store.steampowered.com/steamos/buildyourown) wasn't abandoned yet.
My tinkerer self loved the idea of building your own gaming console to play games that I already owned. In fact, I even turned my old Pentium 4 PC to a "Steam Box" for a while when Steam Big picture was a new thing, but that was short-lived.

Once I've got to university, and got some scholarship I started saving up to build a machine to this specific reason. I got half the parts used, some were gifted, and I got the rest as new. After about a year I've got everything I needed.

![My Steam Box](steambox.jpg "The part I was the most proud of is the slick HTPC case it is built into.")

It was nothing spectacular, a 6th gen i3 processor, 8gb of ram, a GTX 1050Ti and 500 gigabytes of spinning rust. But it was all mine, and it was ready to embrace Valve's own SteamOS.

![My Steam Box](steambox2.jpg "It went trough some upgrades since, it's got an SSD in place of the HDD and also the processor has been upgraded to an i5 one. Notice, that you can only really fit low profile video cards in here. The single high profile slot is does not have enough clearance of the CPU cooler.")

# Software troubles

First SteamOS ran mostly fine. I obviously had to hack things on it, and broke it sometimes, but it worked fine. But after some time I can't remember exactly why, but it had some issues.

After that I moved in to dormitory where I didn't have a television in my room, so my Steam Box were just collecting dust for a few years. In 2022 when I graduated I moved in with my girlfriend to an apartment where I had access to a television yet again. So it was time to set up my Steam Box once again.

While I was in the dorm, I've heard of a new thing called Gamer OS which were later renamed to [ChimeraOS](https://chimeraos.org/). Since I had issues with SteamOS back than, and it seemed abandoned, given it's still based on Debian 8. 

So I've done what seemed logical. I've installed Chimera OS. And it was awesome! Sure it had some flaws, but I assumed they will be fixed with later upgrades. They delivered exactly what I was looking for. An install-and-forget Linux OS for my living room.

The web management was pretty nicely done, and I could even get some retro games running effortlessly. It just worked, and I loved it. 

_Until it doesn't._

One day, I've got a notification from Steam, that [Untitled Goose Game](https://store.steampowered.com/app/837470/Untitled_Goose_Game/) is on sale. I wanted this game for a while, and this was the perfect opportunity to get it. It has a local co-op mode and full controller support, so I've thought that it would be perfect to play it on the tv with girlfriend. I've fired up the Steam Box to download it, and try it out.

It updated Chimera OS, then after a while I was greeted with... a desktop?

Since I had some custom modifications here and there I thought that maybe I broke something, so I blkdiscarded the SSD, and re-installed Chimera OS cleanly, to be greeted yet again with a Desktop...

After some fruitless googling, I was pointed to the Chimera OS Discord. (I highly dislike the idea that people threat Discord as a forum of some kind, and lock out everyone else from finding solution to their problem, but it is what it is). And indeed [I've found what the problem was](https://discord.com/channels/560281725175988233/1133481947272859728/1133481947272859728) (but sadly, the suggested solution did not work for me).
Long story short, Chimera OS dropped support for Nvidia GPUs, and they only support AMD ones now. It just happened that an issue came up now that broke my system, that was only a question of time since they did no longer test for Nvidia. I can't blame them, Nvidia really gives a hard time for the Linux community. 

_But I was mad._

The hardware I had, and would be perfectly capable of running games, but some software wick-wacky prevented me from this. 
I've looked up if it would be possible to painlessly just switch to AMD, but sadly they did not seem to manufacture low-profile gpus. (And I had problems with AMD as well, as my desktop have an AMD card). So I couldn't even fix my problem with money. So what could I do?

# Time to re-invent the wheel!

_How hard would it be to build my own simplified "SteamOS"?_

Turn's out, pretty easy, if you go for the bare minimum.

So I've come up with the following plan:
1. Install Debian
2. Install Nvidia Drivers
3. Install Steam
4. Come up with something to boot into Gamepad UI (successor of Big Picture)
5. ???
6. Profit!

I also didn't want to invest much time into this project... I just wanted to finally play! But I had some goals: Keep it super-minimal, and install only what I really need for my games to work.

In the following few sections I will try to write things in a tutorial fashion, but I worked on this project before I created this blog, so I'm doing my best to remember stuff, expect some mistakes.

## Install Debian

That was simple. I got my trusty `blkdiscard`, and cleared the SSD. Then I installed Debian as anyone would do: Through the installer (I know at least seven ways to install Debian, that's why I pointed this out).

I've installed the latest stable version as of today: Debian Bookworm. I figured stable just fits perfectly for this setup.
In [tasksel](https://wiki.debian.org/tasksel) I've chosen only to install the SSH server and nothing else. I want to install just what I need manually.

Also, not that it matters, but I've chosen to install everything on one big partition. This wouldn't be the best choice for some scenarios... but for a living room PC this is fine.

After the installion was complete, I've logged in using SSH, so I can work from the comfort of my desktop PC.

And started installing stuff! First we will need X, "drivers" for it and some utils to help us to work with it:
```bash
sudo apt install xserver-xorg dbus libpam-systemd x11-common xserver-xorg-legacy x11-xserver-utils x11-xkb-utils dbus-x11 xserver-xorg-input-all xinit xterm
```

I know, Wayland this and Wayland that. The sad truth is that (probably just my bad experience) if you want (somewhat) working proprietary Nvidia drivers in 2023 on your Linux desktop, you've gotta use Xorg. X is still very usable, and for this purpose, it will be sufficent. 

Along the utils I've mentioned, I've installed xinit and xterm, those are a great help when you are tinkering with X manually, which I needed while I figured everything out.

Next it was time for PulseAudio! We will need sound after all.

```bash
sudo apt install pulseaudio pavucontrol
```

I know, I know, Pipewire...

I've also installed `pavucontrol`, for debugging purposes later.

**Important:** by default, the Debian installer did not assign the primary user to the `input` group. This generally not a problem, but I've spent at least two hours (which was half of the time I spent on this project as a whole) figuring out that this was the issue why Steam couldn't use my controller. So to make controllers work, add the primary user to the `input` group:

```bash
$ sudo usermod -a -G input <username>
```

## Install Nvidia Drivers

This was quite simple. Debian packs Nvidia drivers and in my experience this is the most reliable way of having them properly installed and updated.  

So, just enable non-free repos:
```bash
$ sudo apt edit-sources
```

![repos](repos.png "Added `contrib`, `non-free` and `nonfree-firmware` repos")

And install the drivers (along with some stuff we will need in the future)
```bash
$ sudo apt update
$ sudo apt install nvidia-driver mesa-vulkan-drivers mesa-utils
```

Keep in mind, that we want to install Steam here... that is still built for 32 bit in 2023. So we also have to install the 32 bit libs as well:

```bash
$ sudo dpkg --add-architecture i386
$ sudo apt update
$ sudo apt install nvidia-driver-libs:i386 libglx-mesa0:i386 mesa-vulkan-drivers:i386 libgl1-mesa-dri:i386
```

After that I rebooted. Started X manually using `xinit` and checked `glxgears` and `glxinfo`. Everything was cool and good.

## Install Steam

This is also pretty simple, once you figure out some quirks, like I did. Thankfully steam is available in the Debian 12 repos, once you enable `non-free` software (which we did).

```bash
$ sudo apt install steam-installer
```

Fun fact: you need to have lsof installed manually, as for some reason the steam package does not depend on it, but it won't launch witout it:
```bash
$ sudo apt install lsof 
```

Fun fact 2: Steam depends on NetworkManager to it's networking related stuff. This isn't an issue on dasktop, but the Gamepad UI is designed to also provide an interface for basic OS tasks (network management, mounting/unmounting sdcard, sound stuff). Without NetworkManager it can not tell the state of the network and maybe even (wrongly) assume that you are offline and refuse to go online. So we have to install that as well:

```bash
$ sudo apt install NetworkManager
```

And to let NetworkManger manage the wired interface, we have to remove all related config to it from ifupdown's config:

```bash
$ cat /etc/network/interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# config for enp3s0 removed
```

## Come up with something to boot into Gamepad UI

So this is the actual fun part of the project. I knew what I needed, and was sure about what I want to avoid. 

no gamescope
no desktop mode

```bash
#!/bin/bash

# set wallpaper
feh --bg-fill /opt/bg.png

# start pulseaudio
pulseaudio -D

openbox &
OPENBOX_PID=$!

# start steam
steam -steamdeck -gamepadui -steamos3 -steampal

kill -TREM $OPENBOX_PID
pulseaudio --kill
```

```bash
# nodm configuration

# Set NODM_ENABLED to something different than 'false' to enable nodm
NODM_ENABLED=true

# User to autologin for
NODM_USER=marcsello

# First vt to try when looking for free VTs
NODM_FIRST_VT=7

# X session
NODM_XSESSION=/opt/startup.sh

# Options for nodm itself
NODM_OPTIONS=

# Options for the X server.
#
# Format: [/usr/bin/<Xserver>] [:<disp>] <Xserver-options>
#
# The Xserver executable and the display name can be omitted, but should
# be placed in front, if nodm's defaults shall be overridden.
NODM_X_OPTIONS='-nolisten tcp -nocursor'

# If an X session will run for less than this time in seconds, nodm will wait an
# increasing bit of time before restarting the session.
NODM_MIN_SESSION_TIME=60

# Timeout (in seconds) to wait for X to be ready to accept connections. If X is
# not ready before this timeout, it is killed and restarted.
NODM_X_TIMEOUT=30
```

https://github.com/ChimeraOS/gamescope-session/blob/cdf6d4c18497fa00e7ee4c6342b16229a1eaa742/usr/share/gamescope-session/gamescope-session-script


# Future improvements

This project was done on the scale of hours, obviously it is nowhere near perfect. Here are some areas that it should be improved per se.

## Work around some games that have trouble going into full screen

So, none of the games I've initially tested this with had this problem, but I've recently also bought a load of [Jackbox Games](https://www.jackboxgames.com/). For some reason these games don't go into full-screen. So the window border around them, and Steam in the background is still visible.

I'm currently having a plasma tv, so having static parts of the screen is a bit problematic as it could burn in badly.

So, I need something that changes these games to run in a borderless fullscreen window. I've already seem to [found useful info and some code](https://github.com/FreddyBLtv/borderless-fullscreen) on the matter, so I might update this post later, once I figure this part out.

Although this wouldn't be an issue if I used Gamescope, so I might re-evaluate my possibilities regarading that. 

## Replace nodm

nodm is old... The [first commit was made in 2008](https://github.com/spanezz/nodm/commit/eebb441dba9acc9c2876824bac50c27d44c3b19e), which isn't a problem by itself, but sadly, as [it's own README states](https://github.com/spanezz/nodm/blob/master/README.md#this-repository-is-not-maintained), it really needs to be refactored to stand up to today's standards, but the project got abandoned, so it won't seem to happen.

There is also one inconvenience (which I was lazy to investigate deeper) but during shutdown nodm restarts the xsession. This causes Steam to restart for a short time then being killed soon after. I don't expect Steam to be prepared for this, so I can only wait until it corrupts something this way.

So sadly, nodm has to go. There are a few possible alternatives, as nodm's author suggests, lightdm autologin is one possibility. I'm also thinking of doing some lower level magic with `xinit`, or directly starting X, but don't know which direction I would end up eventually.

## Add emulators

What was super-cool about ChimeraOS is its built-in emulators. It was super easy to add and play retro games. I've actually miss this feature.

It would be nice to install some emulators and play retro games on my tv again.

# Conclusion

asd