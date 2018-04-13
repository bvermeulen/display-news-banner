from tkinter import *
import sys, os
import time
from class_news import Controls, Display

'''
    Newsbanner application for python 3.6
    with a summary of news given in a ticker

    rewritten in class
'''

def main():
    width      =  950
    height     =  300
    bgcolor    = '#14B4E1'

    news_list  = {  'CNN World News' : 'http://rss.cnn.com/rss/edition_world.rss',
                    'The Guardian'   : 'https://www.theguardian.com/business/economics/rss',
                    'Nu.nl'          : 'http://www.nu.nl/rss/Algemeen',
                    'BBC World News' : 'http://feeds.bbci.co.uk/news/world/rss.xml',
                    'BBC Technology' : 'http://feeds.bbci.co.uk/news/technology/rss.xml',
                    'BBC Business'   : 'http://feeds.bbci.co.uk/news/business/rss.xml'}
    try:
        news_site = sys.argv[1]
    except:
        news_site = 'Nu.nl'
            
    root= Tk()
    root.title('News feed')
    root.geometry("%dx%d" % (width, height))
    root.configure(background=bgcolor)

    control = Controls(root, news_list)
    control.create()

    news = Display(root, control, width-120, height, news_list)
    root.bind("<Escape>", control.exit_news)
    root.protocol('WM_DELETE_WINDOW', control.exit_news)
    
    news.news_window()
    control.reset_controls()
    control.news_site = news_site

    while control.run:
        news_site = control.news_site
        news.update_news(news_site)     
        news.main_title(news_site)
    
        i = 0
        while i < news.items and control.run and control.news_site == news_site:
            news.display_news_item(i)
            if control.next:
                i = (i + 1) % news.items
            elif control.previous:
                i = (i - 1) % news.items
            else:
                i+= 1

            control.reset_controls()

    root.destroy()

if __name__ == "__main__": 
    main()
