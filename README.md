# display-news-banner
> A news banner application to show RSS news headlines.

![](news_banner_screen_shot.png)

Author: Bruno Vermeulen<br />
Email: bruno_vermeulen2001@yahoo.com<br />
Date: 21 March 2018<br />
Latest Update: 18 June 2018<br />
*This application was originally inspired by a school project by Olof Vermeulen, Groningen.*
## Use: 
Python 3.6<br />
This program uses the modules: tkinter, feedparser, time, re, sys.<br />
feedparser can be downloaded at: https://pypi.python.org/pypi/feedparser<br />

To start the application:
```sh
python3 news.py [-b] [news_site]
```
argument: news site name as per dictionary below, for example 'BBC World News'. If the argument is omitted it takes the news site 'Nu.nl'. Option '-b' starts program in banner mode.

The news sites available are given in the dictionary news_list in the module news_sites.py:
```sh
news_list = {'CNN World News':
             'http://rss.cnn.com/rss/edition_world.rss',
             'The Guardian':
             'https://www.theguardian.com/business/economics/rss',
             'Nu.nl':
             'http://www.nu.nl/rss/Algemeen',
             'BBC World News':
             'http://feeds.bbci.co.uk/news/world/rss.xml',
             'BBC Technology':
             'http://feeds.bbci.co.uk/news/technology/rss.xml',
             'BBC Business':
             'http://feeds.bbci.co.uk/news/business/rss.xml'}
```
Use the buttons for control:
* pause - toggles between pause and run
* previous - go to the previous news item
* next - go to the next news item
* banner - toggles between banner mode and box text mode
* exit - leaves the program
* selection of news site

Exit by pressing Exit button, "Escape" or the root window exit (X)
