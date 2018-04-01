from tkinter import *
import feedparser
import time
import re

'''
    Newsbanner application for python 3.6
    with a summary of news given in a ticker

'''

def UpdateNews(URL):
    global feed, items
    feed  = feedparser.parse(URL)
    items = len(feed["items"])
    return

def Exit_banner(event):
    print("we will leave the program now....")
    root.after(1000) # 1000 ms
    root.destroy()

width      = 800
height     =  300
bgcolor    = '#14B4E1'
title_text =  "Nederlands Nieuws"
padding    = 3

root= Tk()
root.title(title_text)
root.geometry("%dx%d" % (width, height))
root.configure(background=bgcolor)

# create variables, fontsizes
title_x            = width - 2*padding
title_y            = 60
title_spacing      = 10

title_tl           = (padding, padding + title_spacing)
font_main_title    = ('Calibri', 32, 'bold')
font_news_title    = ('Calibri', 20, 'bold')
font_summary       = ('Calibri', 16)
font_reference     = ('Calibri',  8)
newsbox_spacing    = 20

news_URL           = 'http://www.nu.nl/rss/Algemeen'
newsbox_x          = width - 2*padding
newsbox_y          = 200
newsbox_vertical   = padding + title_spacing + title_y + padding + newsbox_spacing
newsbox_tl         = (padding, newsbox_vertical)
news_title_y       = 40
summary_y          = 30
news_summary_y     = news_title_y + 2*20 + summary_y # related to font size news_title and requirement of 2 lines
delay              = 4 # millisecond delay per pixel 
dx                 = 1
dy                 = 0
run                = True

# display main title and the newsbox
title_frame   = Frame(root, width= title_x, height= title_y, relief=RIDGE, highlightbackground="black",
                      highlightcolor="black", highlightthickness=1, bg='white') # highlight etc is a trick to get border color
title_frame.place(x = title_tl[0], y =title_tl[1])
title_main    = Label(title_frame, text=title_text, bd=-1, fg='black',bg='white', font=font_main_title)
title_main.place(x = (title_x/2), y = -padding+32, anchor = 'center')
newsbox_frame = Frame(root, width= newsbox_x, height= newsbox_y, relief=RIDGE, highlightbackground="black",
                      highlightcolor="black", highlightthickness=1, bg='white')
newsbox_frame.place(x = newsbox_tl[0], y = newsbox_tl[1])

# go in an infinate loop to leave by pressing Escape or Main window exit X
root.bind("<Escape>",Exit_banner)
news_title_txt = Label(root,text="")
status_txt     = Label(root,text="")
reference_txt  = Label(root,text="")

while run:
    # update the news and display reference
    UpdateNews(news_URL)
    reference_txt.destroy() # remove the previous message after update as this takes a little time
    reference_text ="Nieuws update van " + news_URL + " op " + time.ctime()
    reference_txt  = Label(newsbox_frame, text=reference_text,bd=-1, fg='grey',bg='white',font=font_reference)
    reference_txt.place(x = padding,y = padding)

    for i in range(items):
        # clean the previous messages
        news_title_txt.destroy()
        status_txt.destroy()

        # display main news title and status
        news_title_txt = Label(newsbox_frame,text=feed["entries"][i].title,bd=-1, anchor='nw', 
                               fg='darkblue', bg='white',font=font_news_title, wraplength= newsbox_x)
        news_title_txt.place(x = padding, y = padding+news_title_y)
        status_text = "Nieuws item: " + str(i+1) +" van " + str(items)
        status_txt = Label(newsbox_frame, text=status_text, bd=-1, fg='grey',bg='white',font=font_reference)
        status_txt.place(x = padding,y = newsbox_y-padding-2*8)

        # show the summary of the news item as scrolling right to left in the news summary frame
        news_summary = feed["entries"][i].summary
        news_summary = re.sub('&nbsp;', ' ', news_summary) # replace formatting occurences
        news_summary_frame = Frame(newsbox_frame, width= newsbox_x-3*padding, height= summary_y, bg='lightgrey')
        news_summary_frame.place(x = padding, y = news_summary_y)
        news_text = Label(news_summary_frame,text=news_summary, font=font_summary,bg='lightgrey')
        
        root.update_idletasks() # necessary to get the winfo_reqwidth information
        pixels=int((news_text.winfo_reqwidth()+int(0.5*newsbox_x))/dx)
        x = width
        y = -padding
        for p in range(pixels):
            # move text object by increments dx, dy
            # -dx --> right to left
            news_text.place(x = x, y = y)
            x = x - dx
            root.update()
            root.after(delay) # message reading time is delay (ms) * pixels - so 10 ms * 1000 pxl = 10 s - 
                              # is depending of the length of the message

# root.mainloop()
