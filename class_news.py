from tkinter import Button, Label, Frame
import feedparser
import time
import re
'''  Module for for Classes:
        - Controls
        - Display

     python 3.6
'''


class Controls:
    '''  Class Controls containing the methods to control:
         - create            : create buttons on the right side
         - reset_controls    : reset control variables to steer the program
         - pause_status      : changes from pause to run and vice versa
         - next_item         : jumps to next news item
         - previous_items    : jumps to previous news item
         - site_select       : select a news site depending on what news site
                               button is pressed
         - exit_news         : exit the program
    '''
    def __init__(self, root, list_sites):
        self.root = root
        self.run = True
        self.list_sites = list_sites
        self.pause = False
        self.next = False
        self.previous = False
        self.orig_bg = ''

    def create(self):
        '''  Method to create control buttons, including news sites defined
             in the Dictonary
        '''
        width = 12
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.pause_button = Button(self.root, text='Pause', width=width,
                                   command=self.pause_status)
        self.pause_button.pack(anchor='e')

        self.next_button = Button(self.root, text='Next', width=width,
                                  command=self.next_item)
        self.next_button.pack(anchor='e')

        self.previous_button = Button(self.root, text='Previous', width=width,
                                      command=self.previous_item)
        self.previous_button.pack(anchor='e')

        self.exit_button = Button(self.root, text='Exit', width=width,
                                  command=self.exit_news)
        self.exit_button.pack(anchor='e')

        self.site_button = {}
        for site in self.list_sites:
            btn = Button(self.root, text=site, width=width,
                         command=lambda x=site: self.site_select(x))
            btn.pack(anchor='e')
            self.site_button[site] = btn
        self.orig_bg = btn.cget("bg")

    def reset_controls(self):
        '''  Method to reset all control booleans
        '''
        self.pause = False
        self.next = False
        self.previous = False
        self.exit_banner = False

    def pause_status(self):
        '''  Method to toggle between pause and run
        '''
        self.pause = not self.pause
        while self.pause and self.run:
            self.pause_button.config(text='Run', relief='raised')
            self.root.update()
        self.pause_button.config(text='Pause', relief='raised')

    def next_item(self):
        '''  Method to jump to a next news item
        '''
        self.next = True
        self.pause = False
        self.exit_banner = True
        self.next_button.config(relief='raised')

    def previous_item(self):
        '''  Method to return to a previous news item
        '''
        self.previous = True
        self.pause = False
        self.exit_banner = True
        self.previous_button.config(relief='raised')

    def site_select(self, site):
        '''  Method to select another news site
        '''
        for x in self.list_sites:
            self.site_button[x].config(relief='raised', bg=self.orig_bg)
        self.news_site = site
        self.exit_banner = True
        self.pause = False
        self.site_button[site].config(relief='sunken', bg='grey')

    def exit_news(self, *event):
        '''  Method to leave the program
        '''
        print("we will leave the program now....")
        self.root.after(1000)  # 1000 ms
        self.run = False
        self.exit_banner = True


class Display:
    '''  class Display_news with methods:
         - initialise display_news(width, height, title, URL)
         - main_tite()       : displays main title at top
         - news_window()     : displays news window area below title
         - display_news()    : displays news title and news banner
         - update_news()     : update news information feed
    '''
    padding = 3
    title_spacing = 10
    title_y = 60
    news_box_spacing = 20
    newsbox_y = 200
    summary_too_long = 3000

    newsbox_vertical = padding + title_spacing + title_y + padding\
        + news_box_spacing
    news_title_y = 40
    summary_y = 30
    news_summary_y = news_title_y + 2*20 + summary_y
    # related to font size news_title and requirement of 2 lines
    delay = 4  # millisecond delay per pixel
    dx = 1
    dy = 0

    font_main_title = ('Calibri', 32, 'bold')
    font_news_title = ('Calibri', 20, 'bold')
    font_summary = ('Calibri', 16)
    font_reference = ('Calibri',  8)

    def __init__(self, root, control, width, height, list_sites):
        self.root = root
        self.control = control
        self.width = width
        self.height = height   # note this parameter is not used
        self.list_sites = list_sites
        self.title_x = self.width - 2 * self.padding
        self.newsbox_x = self.width - 2 * self.padding
        self.news_title_txt = Label(root, text="")
        self.status_txt = Label(root, text="")
        self.reference_txt = Label(root, text="")

    def main_title(self, title_text):
        '''  Method to display the main news title being the news site
        '''
        title_tl = (self.padding, self.padding + self.title_spacing)
        title_frame = Frame(self.root, width=self.title_x,
                            height=self.title_y, relief='ridge',
                            highlightbackground="black",
                            highlightcolor="black", highlightthickness=1,
                            bg='white')
        # highlight etc is a trick to get border color
        title_frame.place(x=title_tl[0], y=title_tl[1])
        title_main = Label(title_frame, text=title_text, bd=-1, fg='black',
                           bg='white', font=self.font_main_title)
        title_main.place(x=int(self.title_x / 2), y=-self.padding + 32,
                         anchor='center')

    def news_window(self):
        '''  Method to display the news window which will contain the news
             item title, news summary
        '''
        newsbox_tl = (self.padding, self.newsbox_vertical)

        self.newsbox_frame = Frame(self.root, width=self.newsbox_x,
                                   height=self.newsbox_y, relief='ridge',
                                   highlightbackground="black",
                                   highlightcolor="black",
                                   highlightthickness=1, bg='white')
        self.newsbox_frame.place(x=newsbox_tl[0], y=newsbox_tl[1])

    def display_news_item(self, i):
        '''  Method to display the news item: title and summary banner plus status
        '''
        # clean the previous messages
        self.news_title_txt.destroy()
        self.status_txt.destroy()

        # display main news title and status
        self.news_title_txt = Label(self.newsbox_frame,
                                    text=self.feed["entries"][i].title, bd=-1,
                                    anchor='nw', fg='darkblue', bg='white',
                                    font=self.font_news_title,
                                    wraplength=self.newsbox_x)
        self.news_title_txt.place(x=self.padding,
                                  y=self.padding + self.news_title_y)

        status_text = "Nieuws item: " + str(i+1) + " van " + str(self.items)
        self.status_txt = Label(self.newsbox_frame, text=status_text, bd=-1,
                                fg='grey', bg='white',
                                font=self.font_reference)
        self.status_txt.place(x=self.padding,
                              y=self.newsbox_y-self.padding - 2 * 8)

        # show the summary of the news item as scrolling right to left
        # in the news summary frame
        news_summary = clean(self.control, self.feed["entries"][i].summary)
        if len(news_summary) > self.summary_too_long:
            news_summary = '###'

        news_summary_frame = Frame(self.newsbox_frame,
                                   width=self.newsbox_x - 3 * self.padding,
                                   height=self.summary_y, bg='lightgrey')
        news_summary_frame.place(x=self.padding, y=self.news_summary_y)

        news_text = Label(news_summary_frame, text=news_summary,
                          font=self.font_summary, bg='lightgrey')
        self.root.update_idletasks()
        # necessary to get the winfo_reqwidth information

        pixels = int(news_text.winfo_reqwidth() + 0.5 * self.newsbox_x)
        x = self.width
        y = 0

        while x > (self.width-pixels) and not self.control.exit_banner:
            # move text object by increments dx, dy
            # -dx --> right to left
            news_text.place(x=x, y=y)
            x = x - self.dx
            self.root.update()
            self.root.after(self.delay)
            # message reading time is delay (ms) * pixels -
            # so 10 ms * 1000 pxl = 10 s is depending of the
            # length of the message

    def update_news(self, news_site):
        '''  Method to update the news and display the news site
        '''
        news_URL = self.list_sites[news_site]
        self.feed = feedparser.parse(news_URL)
        self.items = len(self.feed["items"])
        self.reference_txt.destroy()
        # remove the previous message after update as this takes a little time
        reference_text = "Nieuws update van " + news_URL + " op "\
                         + time.ctime()
        self.reference_txt = Label(self.newsbox_frame, text=reference_text,
                                   bd=-1, fg='grey', bg='white',
                                   font=self.font_reference)
        self.reference_txt.place(x=self.padding, y=self.padding)


def clean(control, raw_string):
    '''  Function to clean string from unwanted formatting text
    '''
    clean_string = re.sub('&nbsp;', ' ', raw_string)
    clean_string = re.sub(r'<.*?>', '', clean_string)
    if clean_string == '':
        control.next_item()
    return clean_string
