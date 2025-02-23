So, it all started with a [Stanford Lifestyle Medicine article](https://longevity.stanford.edu/lifestyle/2024/05/30/what-excessive-screen-time-does-to-the-adult-brain/) about "What Excessive Screen Time Does to the Adult Brain".
You wouldn't have guessed it, but it's not healthy! I know, I know, this groundbreaking discovery probably won't change the world on its own. The awesome thing about this article however is that it actually gives you some advice on how to improve your life in this regard.

Their advice, which I took by heart, is "No Screen Time for the First Hour of the Day". Actually, they recommended this as a practice for a month, but I'm actually doing this practice for half a year now.
I won't say it changed my life or anything, it's just something I've been doing ever since. I've been also thinking of stepping up my game for a while: **baning smartphones from the bedroom altogether**.

I'm thinking of setting up a nice charging station somewhere outside and leaving my phone there while I sleep. I could also get some nice bedroom lamp, and maybe read a book or something instead of being on my phone before sleep.
But there's one thing that prevents me from doing that...

# How do I get up in the morning?

Yes, that's right. Ever since I had a mobile phone (not even a smartphone), I'm using it as my alarm clock.
This is the most reliable way to wake me up. It has an internal battery, so it works during power outages. It synchronizes its clock to the network, so it will always alarm on time. It's portable and I can even choose the alarm sound.

It's really just the perfect solution for waking someone up. There was even quite a long period of my life, while used sleep tracking.
I purchased [Sleep as Android](https://play.google.com/store/apps/details?id=com.urbandroid.sleep) in 2015 and used it just until a few years ago.

![My Google Play purchase history](purchase_history.png)

I no longer use sleep tracking, but their little puzzles that you have to solve to turn off the alarm are pretty clever, and I still use this feature.
Sometimes I'm having a super hard time waking up. Since I overslept some of my meetings in the morning (which were super embarrassing to me), I have an NFC tag in the hallway that I have to scan to stop the alarm. (I used to do "simple maths" before, but as it turned out, it just helped me develop the ability to do maths in my sleep.)

So using a smartphone (or even a dumb phone) to wake me up is just the best thing I could have, but sadly it conflicts with my plan above. So I've got to look for an alternate solution.

# Getting an Alarm Clock

The _easy_ solution to this problem would be to just buy any alarm clock, put it on my bedside table and call it a day. But that would be the most boring solution imaginable.

You see, I can't just buy any alarm clock. If I'm going to get one, I need one that is specifically tuned for my needs. And that need is the need for running Linux. (Also the things I described above would be nice to have.)

So the only logical thing to do here is to ignore the market altogether, go ahead and design and build an alarm clock that ticks that all-important box.
(It's possible that there are clocks out there that would probably meet my needs, but there's no stopping now.)

I expect this project to take up years if not months. So instead of writing a post about it at the end (as I try with most of my projects), I try to write about it each time I hit a noteworthy milestone.

This post marks the first milestone, where I get a neat shell for my project.

# The Tesco Value CR-106 clock radio

When I was a kid, and I didn't have a mobile phone (or I didn't use it as an alarm clock, I can't remember). I had this exact model of a radio clock.

I remember going to the nearest Tesco, with my saved money, and there was a shelf full of radio alarm clocks. This one was on the end of the line, the cheapest option. They sold it in the usual white-blue "Tesco Value" box.

![Photo of a Tesco Value CR-106 clock radio](clock.jpg "The glorious Tesco Value CR-106 clock radio. With years of dirt attached to it.")

While it wasn't really the nicest option, I still remember this clock as "The radio alarm clock" that I had, and when I have to think about a "radio alarm clock" this comes to my mind.

Sadly, I no longer have mine, still I decided I want something that looks like this. The best way to achieve this (to me) is by getting one and modifying its internals.
At that time I didn't remember anything else about it aside from how it looked like, so I searched the local and online markets for one, but none of the ones I could find were to my liking.
Until eventually, I discovered that this was "The model," and after that, I could finally look for it.

I managed to find it at an online second-hand marketplace, for a few thousand local currencies (that's actually not that much here), so I picked it up. It was mostly functional, a bit dirty (the picture above was made just when I got it home), the buttons were a bit hard to press, the radio sounded very crunchy, and it was missing its antenna.
But it was there! I was delighted about it. It brought back some of my childhood memories.

# TODO

So it is time to tear it down, so we can use the shell, and maybe some of the internal components could be useful.


TODO



# Fun facts

Obviously, while looking for the perfect radio alarm clock, I found some interesting bits.

## Other models

Apparently, this radio alarm clock was sold under different brands than Tesco Value.

There is a brand that is unknown to me that seems to have sold the exact same clock without any modifications.

![](carrefour-clr218.jpg "Source: https://www.wallapop.com/item/radio-despertador-511546335")

Also, a little more known brand, Elta seem to have their own version of this radio alarm clock, but they did a twist on the colors as well.

![](elta-4218-n.jpg "Source: http://www.hifi-forum.de/themen/produkte/elta/4218-n")

## CR106R

It seems like there was an upgraded version of this radio that featured a digital tuner. I found less online listings for it, so I assume It wasn't as popular. I found the manual for it, however.

![Cover page of the Tesco Value CR106R radio alarm clock's user manual](cr106r.png "Source: https://www.manua.ls/tesco/cr106r/manual?p=2")

At first glance, it looked very similar to mine, except for the extra button on the top. I guess that was added because there was a need for an extra button to adjust the volume, and the extra alarm option was just an afterthought.  
They seem to have changed very little in the manufacturing process of the case. The holes for the dials and switches on the side are covered up instead of making a new shell (so I assume the hole for the extra button on top is also drilled into existing cases).

However, they have changed the internals. The display must have been changed because there is no segment in the place of the "AL2Buzzer" on the display for the CR-106.
Also, according to the manual, it needs 2xAA batteries instead of the 9V battery for the time backup.