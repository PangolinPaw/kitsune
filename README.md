kitsune
=======

Kitsune twitter response bot


Introduction
------------
This twitter bot scans recent tweets for the keywords defined in key_word.txt and exctracts
the senders' user names. It then tweets a response using those names and the text from
message.txt.

The order of keywords and messages in these files is important. I.E. Tweets containing the
phrase on line 1 of key_word.txt are sent the response from line 1 of message.txt.

This allows for automated responses to certain hashtags; useful for running competitions,
advertising or any other project that needs to send large numbers of a large variety of
tweets autonomously.

Planned features
----------------
- Include images with responses.
- Send email updates of tweets found, responses sent etc. for analytics.
- Allow for remote addition/editing of keywords and response messages via email.

Please Note
-----------
The kitsune python script relies on my own twitter module which is not included in this
repository.
