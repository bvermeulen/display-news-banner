from tkinter import *
import feedparser
import time

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
    print("we will leave the program in 3 seconds....")
    time.sleep(3)
    root.destroy()

width      = 1000
height     =  300
bgcolor    = '#14B4E1'
title_text =  "                 News Banner"
padding    = 5

root= Tk()
root.title(title_text)
root.geometry("%dx%d" % (width, height))
root.configure(background=bgcolor)

Banner = Canvas(root, width=width, height=height,bg=bgcolor)
Banner.pack(fill=BOTH, expand=YES)

# create variables, fontsizes
title_x            = width - 2*padding
title_y            = 60
title_vertical     = 5

title_tl           = (padding, padding + title_vertical)
title_br           = (title_tl[0]+title_x,title_tl[1]+title_y)
font_main_title    = ('Calibri', 32, 'bold')
font_news_title    = ('Calibri', 20, 'bold')
font_summary       = ('Calibri', 16)
font_reference     = ('Calibri',  8)
space_title_banner = 10

news_URL           = 'http://www.nu.nl/rss/Algemeen'
newsbox_x          = width - 2*padding
newsbox_y          = 200
newsbox_vertical   = padding + title_vertical + title_y + padding + space_title_banner
newsbox_tl         = (padding, newsbox_vertical)
newsbox_br         = (newsbox_tl[0]+newsbox_x,newsbox_tl[1]+newsbox_y)
delay              = 0.005
dx                 = 1
dy                 = 0
run                = True

# display main title and the newsbox
Banner.create_rectangle(title_tl,title_br, fill='white')
title_main  = Label(root, text=title_text, bd=-1, fg='black',bg='white', font=font_main_title)
title_main.place(x=title_tl[0]+padding,y=title_tl[1]+padding)
Banner.create_rectangle(newsbox_tl,newsbox_br, fill='white')

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
    reference_txt  = Label(root, text=reference_text,bd=-1, fg='grey',bg='white',font=font_reference)
    reference_txt.place(x=newsbox_tl[0]+padding,y=newsbox_tl[1]+padding)

    for i in range(items):
        # clean the previous messages
        news_title_txt.destroy()
        status_txt.destroy()

        # display main news title and status
        news_title_txt = Label(root,text=feed["entries"][i].title,bd=-1, anchor='nw', 
                               fg='darkblue', bg='white',font=font_news_title, wraplength= newsbox_x)
        news_title_txt.place(x=newsbox_tl[0]+padding, y=newsbox_tl[1]+padding+40)
        status_text = "Nieuws item: " + str(i+1) +" van " + str(items)
        status_txt = Label(root, text=status_text, bd=-1, fg='grey',bg='white',font=font_reference)
        status_txt.place(x=newsbox_tl[0]+padding,y=newsbox_br[1]-2*padding-8)

        # show the summary of the news item as scrolling right to left in the news summary frame
        news_summary = feed["entries"][i].summary
        news_summary_frame = Frame(root, width= newsbox_x-2*padding, height= 30, bg='lightgrey')
        news_text = Label(news_summary_frame,text=news_summary, font=font_summary,bg='lightgrey')
        news_summary_frame.place(x=newsbox_tl[0]+padding, y=newsbox_tl[1]+120)
        
        root.update_idletasks() # necessary to get the winfo_reqwidth information
        pixels=news_text.winfo_reqwidth()+int(0.5*newsbox_x)
        x = width
        y = 0
        for p in range(pixels):
            # move text object by increments dx, dy
            # -dx --> right to left
            news_text.place(x=x, y=y)
            root.update()
            x = x - dx
            time.sleep(delay) # message reading time is delay * pixels - so 0.01 * 1000 = 10 s - 
                              # is depending of the length of the message

root.mainloop()


