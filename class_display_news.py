from tkinter import *
import feedparser
import time
import re

'''
    python 3.6
    rewritten in class

    module with class display_news with methods:
        - initialise display_news(width, height, title, URL)
        - main_tite()       : displays main title at top
        - news_window()     : displays news window area below title
        - display_news()    : displays news title and news banner
        - update_news()     : update news information feed
        - exit_news(*event) : set the run flag to False to stop the program

'''

class display_news:

    padding          = 3
    title_spacing    = 10
    title_y          = 60
    news_box_spacing = 20 
    newsbox_y        = 200

    newsbox_vertical = padding + title_spacing + title_y + padding + news_box_spacing
    news_title_y     = 40
    summary_y        = 30
    news_summary_y   = news_title_y + 2*20 + summary_y # related to font size \
                                                       # news_title and requirement of 2 lines
    delay            = 4 # millisecond delay per pixel 
    dx               = 1
    dy               = 0

    font_main_title  = ('Calibri', 32, 'bold')
    font_news_title  = ('Calibri', 20, 'bold')
    font_summary     = ('Calibri', 16)
    font_reference   = ('Calibri',  8)

    def __init__(self, root, width, height, title, URL):
        self.root           = root        
        self.width          = width
        self.height         = height   # note this parameter is not used
        self.title_text     = title

        self.news_URL       = URL
        self.title_x        = self.width - 2*self.padding
        self.newsbox_x      = self.width - 2*self.padding                                    

        self.news_title_txt = Label(root,text="")
        self.status_txt     = Label(root,text="")
        self.reference_txt  = Label(root,text="")

        self.run            = True

    # method to display the main title
    def main_title(self):
        title_tl = (self.padding, self.padding + self.title_spacing)
        
        title_frame = Frame(self.root, width= self.title_x, height= self.title_y, \
                            relief=RIDGE, highlightbackground="black", highlightcolor="black",  \
                            highlightthickness=1, bg='white') \
                              # highlight etc is a trick to get border color
        title_frame.place(x = title_tl[0], y = title_tl[1])
        title_main = Label(title_frame, text=self.title_text, bd=-1, fg='black',bg='white', \
                           font=self.font_main_title)
        title_main.place(x = int(self.title_x/2), y = -self.padding+32, anchor = 'center')

    # method to display the news window
    def news_window(self):
        newsbox_tl = (self.padding, self.newsbox_vertical)

        self.newsbox_frame = Frame(self.root, width= self.newsbox_x, height= self.newsbox_y, \
                                   relief=RIDGE, highlightbackground="black", \
                                   highlightcolor="black", highlightthickness=1, bg='white')

        self.newsbox_frame.place(x = newsbox_tl[0], y = newsbox_tl[1])

    # method to display the news feed and display references
    def display_news(self):
        self.reference_txt.destroy() # remove the previous message after update as this takes a little time
        reference_text ="Nieuws update van " + self.news_URL + " op " + time.ctime()
        self.reference_txt  = Label(self.newsbox_frame, text=reference_text,bd=-1,  \
                                    fg='grey',bg='white',font=self.font_reference)
        self.reference_txt.place(x = self.padding,y = self.padding)

        for i in range(self.items):
            # clean the previous messages
            self.news_title_txt.destroy()
            self.status_txt.destroy()

            # display main news title and status
            self.news_title_txt = Label(self.newsbox_frame,text=self.feed["entries"][i].title,bd=-1, \
                                        anchor='nw', fg='darkblue', bg='white', \
                                        font=self.font_news_title, wraplength= self.newsbox_x)
            self.news_title_txt.place(x = self.padding, y = self.padding+self.news_title_y)
            status_text = "Nieuws item: " + str(i+1) +" van " + str(self.items)
            self.status_txt = Label(self.newsbox_frame, text=status_text, bd=-1, \
                                    fg='grey',bg='white',font=self.font_reference)

            self.status_txt.place(x = self.padding,y = self.newsbox_y-self.padding-2*8)

            # show the summary of the news item as scrolling right to left in the news summary frame
            news_summary = self.feed["entries"][i].summary
            news_summary = re.sub('&nbsp;', ' ', news_summary) # replace formatting occurences
            news_summary_frame = Frame(self.newsbox_frame, width= self.newsbox_x-3*self.padding, 
                                       height= self.summary_y, bg='lightgrey')
            news_summary_frame.place(x = self.padding, y = self.news_summary_y)
            news_text = Label(news_summary_frame,text=news_summary, font=self.font_summary,bg='lightgrey')
    
            self.root.update_idletasks() # necessary to get the winfo_reqwidth information

            pixels=int((news_text.winfo_reqwidth()+int(0.5*self.newsbox_x))/self.dx)
            x = self.width
            y = 0
            while x > (self.width-pixels) and self.run:
                # move text object by increments dx, dy
                # -dx --> right to left
                news_text.place(x = x, y = y)
                x = x - self.dx
                self.root.update()
                self.root.after(self.delay) # message reading time is delay (ms) * pixels - so 10 ms * 1000 pxl = 10 s - 
                                            # is depending of the length of the message

    # method to update the news
    def update_news(self):
        self.feed  = feedparser.parse(self.news_URL)
        self.items = len(self.feed["items"])

    def exit_news(self,*event):
        print("we will leave the program now....")
        self.root.after(1000) # 1000 ms
        self.run = False

