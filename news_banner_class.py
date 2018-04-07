import class_display_news 
from tkinter import *

'''
    Newsbanner application for python 3.6
    with a summary of news given in a ticker

    rewritten in class
'''

def main():
    width      =  800
    height     =  300
    bgcolor    = '#14B4E1'
    title_text = 'Nederlands Nieuws'
    news_url   = 'http://www.nu.nl/rss/Algemeen'

    root= Tk()
    root.title(title_text)
    root.geometry("%dx%d" % (width, height))
    root.configure(background=bgcolor)

    NL_nieuws = class_display_news.display_news(root, width, height, title_text, news_url)
    NL_nieuws.main_title()
    NL_nieuws.news_window()
    root.update()

    # go in an infinate loop to leave by pressing Escape or Main window exit X
    root.bind("<Escape>", NL_nieuws.exit_news)
    root.protocol('WM_DELETE_WINDOW', NL_nieuws.exit_news)

    while NL_nieuws.run:
        NL_nieuws.update_news()     
        NL_nieuws.display_news()
    
    root.destroy()

if __name__ == "__main__": 
    main()
