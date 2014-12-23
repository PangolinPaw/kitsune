kitsune
=======

KITSUNE Twitter Interaction Bot
===============================

Introduction
------------------------
This twitter bot scans recent tweets for the keywords defined in key_word.txt and exctracts
the senders' user names. It then tweets a response using those names and the text from
response.txt.

The order of keywords and messages in these files is important. I.E. Tweets containing the
phrase on line 1 of key_word.txt are sent the response from line 1 of response.txt.

This allows for automated responses to certain hashtags, key words and phrases; useful for 
running competitions, advertising or any other project that needs to send large numbers of 
a large variety of tweets autonomously.

Each 'keyword' can be a full boolean search string.
e.g. 'key +words -RT' would return all tweets containing both 'key' and 'words' but not 'RT'.

Possible Future Features
------------------------
- Include images with responses.
- Send email updates of tweets found, responses sent etc. for analytics.
- Allow for remote addition/editing of keywords and response messages via email.

Please Note
------------------------
The kitsune bot relies on a Twitter API. On the first run of the program you will need to
input all four keys from the API aassociated with your Twitter account. This can be set up
on https://apps.twitter.com and is free of charge at the time of writing.

Installation
------------------------
The control.py script needs to be set to run on boot and the pi needs to automatically reboot
every 24hrs (via cron). This will ensure software updates that require a reboot are 
implemented after download without the need for human intervention.

