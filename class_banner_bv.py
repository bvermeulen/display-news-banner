from tkinter import *
import feedparser
import time

def UpdateNews(URL):
    global feed, items
    feed  = feedparser.parse(URL)
    items = len(feed["items"])
    return

def Exit_banner(event):
    print("we will leave the program in 3 seconds....")
    time.sleep(3)
    root.destroy()

root=Tk()

width      = 1000
height     =  400
bgcolor    = '#14B4E1'
title_text =  "Haren's Lyceum News Banner"

# create the main window
root.title(title_text)
Banner = Canvas(root, width=width, height=height,bg=bgcolor)
Banner.pack()
padding         = 5

# create the title
title_x         = width - 2*padding
title_y         = 80
title_vertical  = 10

title_tl        = (padding, padding + title_vertical)
title_br        = (title_tl[0]+title_x,title_tl[1]+title_y)
font_size       = 40
font            = ('Calibri', font_size)
Banner.create_rectangle(title_tl,title_br, fill='white')
Banner.create_text(int((title_tl[0]+title_br[0])/2),int((title_tl[1]+title_br[1])/2), anchor='center',text=title_text, width=title_x,font=font,fill='black')

# create newsfeed banner
news_URL           = 'http://www.nu.nl/rss/Algemeen'
banner_x           = width - 2*padding
banner_y           = 200
space_title_banner = 35
banner_vertical    = padding + title_vertical + title_y + padding + space_title_banner
banner_tl          = (padding, banner_vertical)
banner_br          = (banner_tl[0]+banner_x,banner_tl[1]+banner_y)
delay              = 0.01
font_title         = ('Calibri', 24, 'bold')
font_summary       = ('Calibri', 18)
font_time          = ('Calibri', 12)
space              = ' ' * 5
pixels             = 1000
dx                 = 1
dy                 = 0
run                = True

# go in an infinate loop to leave by pressing Escape or Main window exit X
root.bind("<Escape>",Exit_banner)

while run: 

    # update the news
    Banner.create_rectangle(banner_tl,banner_br, fill='white')
    UpdateNews(news_URL)
    datetime="Nieuws update van " + news_URL + " op " + time.ctime()

    # display the news
    for i in range(items):
        # clean the banner screen
        Banner.create_rectangle(banner_tl,banner_br, fill='white')

        # display news source and time of update
        Banner.create_text(banner_tl[0]+padding,banner_tl[1], anchor='nw',text=datetime, width=banner_x,font=font_time,fill='black')
        news_title   = feed["entries"][i].title

        # display the news item title
        Banner.create_text(banner_tl[0]+padding,banner_tl[1]+40, anchor='nw',text=news_title, width=banner_x,font=font_title,fill='black')     
        news_summary = space + feed["entries"][i].summary + space

        # show the summary of the new items as scrolling right to left
        text = Banner.create_text(banner_tl[0]+padding,banner_tl[1]+80, anchor='nw',text=news_summary, font=font_summary,fill='blue')
        for p in range(pixels):
            # move text object by increments dx, dy
            # -dx --> right to left
            Banner.move(text, -dx, dy)
            Banner.update()
            time.sleep(delay) # message reading time is delay * pixels - so 0.01 * 1000 = 10 s

root.mainloop()
