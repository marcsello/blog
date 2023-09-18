This is one of those posts you can't really appreciate without having part of your childhood spent on building weird contraptions in [Garry's Mod](https://store.steampowered.com/app/4000/Garrys_Mod/) with some cool [Wiremod](https://wiremod.com/) bits.
I was one of those kids. Sometimes, while I was in the middle of building the most advanced machines I could think of, I found myself running out of keys on my keyboard to control them. Therefore, I was constantly thinking of how could I add more ways of input to the game. 

This thought still bugs me today. Not because I'm still in a huge need of extra buttons, but rather because I'm intrigued by the problem itself.
I'm definitely not playing as much as I used to, but out of nostalgia, I picked up the game again recently, so this  perfect weekend project.

Sure, you can hook up a joystick to your computer, and Garry's mod being a source game, would probably support using it with Wiremod stuff, but that's just about 10% interesting.

# Wiremod and input



# The HTTP capabilities of Expression 2

Sadly the `http*` functions on E2 are very limited and poorly documented. So I had to do some digging and investigation.

Basically E2 can only make `GET` requests, and you can only set the URL for the request. After the request has been made, you only get a single boolean to indicate if it was successful, and you can obtain the response body as a string. 
No headers, no other verbs, no HTTP status, no fancy options like timeout, but that's still plenty of real-world communication here. Oh, and it supports HTTPS at least!

![E2 Extensions menu](permissions.png "From the E2 extensions settings I've also learned, that requests are made by the server itself. This may impose even more limits. It also have to be explicitly enabled by the server administrator.")

The other problematic part of the E2 HTTP methods that they are rather costly (especially if you want to parse JSON). So rapid polling of something is completely out of question. 

![The Expression 2 helper utility](e2helper.png "The httpRequest method costs a mere 20... marbles? the jsonDecode even more. In comparison common E2 function costs around 1-5 marbles.")

So we are stuck with a very slow way of state updating... but wait! Maybe we can implement long polling!

Long-polling is basically just starting a long-lived HTTP request and not doing anything until it returns.
The server holds up the connection until something happens (or closes it after a certain timeout). 
By utilizing long-polling we can receive the "events" as soon as they occur (plus network delay) without wasting resources. 
It seems like we could make this work somehow.  

# Expression 2 and long polling

To test the long-polling "capabilities" of E2 I've [quickly hacked together a tool](https://github.com/marcsello/longPollTester) that starts an HTTP server and measures how long can a client keep up the connection. I've started this tool on my computer, launched Garry's mod, started a single-player game to do some testing. 

![](first_request.png "The first request!")

First, I've learned that for some reason E2 refuses to make requests towards `127.0.0.1`, but I've quickly overcome this by using the DNS name of my computer (fun fact: this is an [intentional limitation](https://wiki.facepunch.com/gmod/http.Fetch), but it seems like it's implemented badly). 
Second, I have found out, that you indeed can not do rapid polling, as there is an approximately 3-second delay after each request when you are not allowed to make another one.

Regarding the long-polling capabilities, after some measurements it seems like I can reliably run requests even as long as 10 minutes (and possibly above that, but that would take too much time to test).

But the initial success in single-player didn't hold up much in multiplayer. 
On my own server with default settings, I couldn't make a request that lasted longer than 1 minute. 
When I went above just a few milliseconds, the request became unsuccessful. 
This isn't great... Firing an HTTP request every 63 sec could be considered spamming by some administrators, but let's hope for the best.  

I was also curious how would multiple E2 chips affect each-other.
And strangely enough, they did disturb each-other, but instead of the 3 second delay, it seemed initially that the individual chips had to wait a lot longer to get a chance to make a request. But after a few minutes these delays normalized.

![](test_farm.jpg "Testing concurrency, the red light means that a request is in progress.")


After checking the convars, and digging up the Wiremod sourcecode, I have found two convars `wire_expression2_http_timeout` and `wire_expression2_http_delay`. 
The delay one is obviously the 3 sec delay between requests that I've already measured, but the timeout with 15 as it's value is a bit odd. 
 

![](convars.png "Convars to control http timings")

[Turns out](https://github.com/wiremod/wire/blob/b43c615d86165240917bd5a86a130174538048d2/lua/entities/gmod_wire_expression2/core/http.lua#L19-L21) that value means the delay after the last request that is still pending. 
That explains the weird behaviour I've observed above. 
Interesting limitation, but I think this is the best they could come up with, as Gmod's builtin http client [does not (seem to) support timeouts](https://wiki.facepunch.com/gmod/http.Fetch).
Thankfully these limits seems to be per-player based, so at least I won't upset other players.

TODO: Test with drops!!