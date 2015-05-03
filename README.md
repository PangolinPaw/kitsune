### Introduction
This Twitter bot is designed to run 24/7 on a Raspberry Pi. It scans recent Tweets for the key words & phrases defined by the user and can then do any (or all) of the following, as pre-set by the user:
- Post a reply to each Tweet found (each search term can have a different, customised response).
- Favourite any Tweets containing the keywords.
- Follow the individual who posted a Tweet containing the keywords.

This allows for automated responses to certain hash-tags, key words and phrases which is useful for running competitions, advertising or any other project that needs to record or reply to a large variety of Tweets autonomously.

Each search term can be a full boolean search string, as used in the search box on Twitter's website.
E.G. '+key +words -RT' would return all tweets containing both 'key' and 'words' but not 'RT'.

Within the quotas set by the Twitter API, KITSUNE can work with up to 5 separate search terms, checking for new tweets every 5 minutes.

### Future Features
- The inclusion of images in Replies.
- Regular reporting on Replies, Favourites and Follows via email for analysis.
- Remote addition/editing of Search terms and Reply messages via email.

### Please Note
KITSUNE relies on a Twitter API. On the first run of the program you will need to input all four keys from the API associated with your Twitter account. This can be set up on [apps.twitter.com](https://apps.twitter.com) and is free of charge at the time of writing.

### Installation
The control.py script needs to be set to run on boot and the Pi needs to automatically reboot every 24hrs (via cron). This will ensure software updates that require a reboot are implemented after download without the need for human intervention.

Please note that the current version of KITSUNE was designed for a specific use, on a specific SD card and hasn't yet been made flexible enough for distribution to other Raspberry Pis. In particular, the self-updates relies on the scripts being saved in a specific directory that is set up as a local Git repository.

###Contact
Please feel free to leave feedback, comments or suggested improvements via GitHub, or you can email me at *botKITSUNE@gmail.com*.
