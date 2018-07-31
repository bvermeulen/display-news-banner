from tkinter import Tk, Button, Label, Frame, Text, Scrollbar
from news_sites import news_list
import feedparser
import time
import re
import sys
import pdb
'''  Module for for classes:
        - Controls
        - Display

     Functions:
        - clean
        - accurate_delay
'''
width = 850
height = 400
bgcolor = '#58024b'
root = Tk()
root.title('News feed')
root.geometry(f'{width+140}x{height}')
root.configure(background=bgcolor)
summary_too_long = 3000
width_char = 100
height_char = 6

class Controls:
    '''  Class Controls containing the methods to control:
         - handleargs        : handle the arguments at startup
         - create            : create buttons
         - reset_controls    : reset control variables to steer the program
         - pause_status      : toggles from pause to run
         - previous_item     : jumps to previous news item
         - next_item         : jumps to next news item
         - site_select       : select a news site depending on what news site
                               button is pressed
         - banner_status     : toggles from banner display to normal display
         - exit_news         : exit the program
    '''

    def __init__(self):
        self.run = True
        self.pause = False
        self.next = False
        self.previous = False
        self.orig_bg = ''

    def handleargs(self):
        '''  handle the arguments: python news.py [-b] <news_site> '''
        print(sys.argv)
        try:
            if sys.argv[1] == '-b':
                self.displaybanner = True
                argid = 2
            else:
                self.displaybanner = False
                argid = 1
        except IndexError:
            argid = 1
            self.displaybanner = False

        try:
            self.news_site = sys.argv[argid]
            if self.news_site not in news_list:
                self.news_site = 'BBC Business'
        except IdexError:
            self.news_site = 'Nu.nl'

    def create(self):
        '''  Method to create control buttons, including news sites defined
             in the Dictonary '''
        bwidth = 8
        padx = 3
        buttonframe = Frame(root, bd=6, relief='sunken')

        self.pause_button = Button(buttonframe, text='Pause', width=bwidth,
                                   command=self.pause_status)
        self.pause_button.pack(side='left', padx=padx)
        self.orig_bg = self.pause_button.cget("bg")

        self.previous_button = Button(buttonframe, text='Previous',
                                      width=bwidth, command=self.previous_item)
        self.previous_button.pack(side='left', padx=padx)

        self.next_button = Button(buttonframe, text='Next', width=bwidth,
                                  command=self.next_item)
        self.next_button.pack(side='left', padx=padx)

        self.banner_button = Button(buttonframe, text='Banner', width=bwidth,
                                    command=self.banner_status)
        self.banner_button.pack(side='left', padx=padx)
        # note that banner_status will reverse the flag!
        self.displaybanner = not self.displaybanner
        self.banner_status()

        self.exit_button = Button(buttonframe, text='Exit', width=bwidth,
                                  command=self.exit_news)
        self.exit_button.pack(side='left', padx=padx)

        buttonframe.pack(side='bottom', anchor='sw')

        bwidth = 12
        newsbuttonframe = Frame(root, bd=6, relief='sunken')
        rows = 10
        self.site_button = {}
        for i, site in enumerate(news_list):
            btn = Button(newsbuttonframe, text=site, width=bwidth,
                         command=lambda x=site: self.site_select(x))
            row = i % rows
            column = i // rows
            btn.grid(row=row, column=column)

            self.site_button[site] = btn

        newsbuttonframe.pack(side='right', anchor='ne')

    def reset_controls(self):
        '''  Method to reset all control booleans '''
        self.pause = False
        self.next = False
        self.previous = False
        self.exit_banner = False

    def pause_status(self):
        '''  Method to toggle between pause and run '''
        self.pause = not self.pause
        while self.pause and self.run:
            self.pause_button.config(relief='sunken', bg='grey')
            root.update()
        self.pause_button.config(relief='raised', bg=self.orig_bg)

    def previous_item(self):
        '''  Method to return to a previous news item
        '''
        self.previous = True
        self.pause = False
        self.exit_banner = True
        self.previous_button.config(relief='raised')

    def next_item(self):
        '''  Method to jump to a next news item '''
        self.next = True
        self.pause = False
        self.exit_banner = True
        self.next_button.config(relief='raised')

    def site_select(self, site):
        '''  Method to select another news site '''
        self.news_site = site
        for x in news_list:
            self.site_button[x].config(relief='raised', bg=self.orig_bg)
        self.exit_banner = True
        self.pause = False
        self.site_button[self.news_site].config(relief='sunken', bg='grey')

    def banner_status(self):
        self.displaybanner = not self.displaybanner
        if self.displaybanner:
            self.banner_button.config(relief='raised', bg='grey')
        else:
            self.banner_button.config(relief='raised', bg=self.orig_bg)
        self.pause = False
        self.exit_banner = True

    def exit_news(self, *event):
        '''  Method to leave the program '''
        print("we will leave the program now....")
        root.after(1000)  # 1000 ms
        self.run = False
        self.exit_banner = True


class Display:
    '''  class Display_news with methods:
         - __init__          : initialises instance of Dispay
         - site_tite         : displays site title at top
         - news_window       : displays news window area below title
         - news_title        : display the news title
         - display_news      : displays news title and news banner
         - news_box          : displays summary in text box
         - news_banner       : displays summary in banner
         - update_news       : update news information feed
    '''
    padding = 3
    title_spacing = 5
    title_y = 60
    news_box_spacing = 10
    newsbox_y = 275

    newsbox_vertical = padding + title_spacing + title_y + padding\
        + news_box_spacing
    news_title_y = 40
    summary_y = 20
    banner_height = 30
    news_summary_y = news_title_y + 3*20 + summary_y
    # related to font size news_title and requirement of 2 lines
    delay = 5  # millisecond delay per pixel
    dx = 1
    dy = 0
    font_main_title = ('Calibri', 32, 'bold')
    font_news_title = ('Calibri', 20, 'bold')
    font_summary_banner = ('Calibri', 16)
    font_summary_box = ('Calibri', 12)
    font_reference = ('Calibri', 8)
    title_x = width - 2 * padding
    newsbox_x = width - 2 * padding
    news_title_txt = Label(root, text="")
    status_txt = Label(root, text="")
    reference_txt = Label(root, text="")

    def __init__(self, control):
        self.control = control
        root.bind("<Escape>", control.exit_news)
        root.protocol('WM_DELETE_WINDOW', control.exit_news)
        self.siteframe = Frame(root)
        self.newsframe = Frame(root)
        self.summaryframe = Frame(root)
        self.news_title_txt = Frame(root)
        self.status_txt = Frame(root)

    def site_title(self):
        '''  Method to display the name of the site '''
        #_tl = (self.padding, self.padding + self.title_spacing)
        self.siteframe.destroy()
        self.siteframe = Frame(root,
                               width=self.newsbox_x,
                               height=self.newsbox_y,
                               relief='ridge',
                               highlightbackground="black",
                               highlightcolor="black", highlightthickness=1,
                               bg='white')
        # highlight etc is a trick to get border color
        self.siteframe.pack(padx=2*self.padding, pady=2*self.padding,
                            fill='both')
        #title_frame.place(x=_tl[0], y=_tl[1])

        site_title = Label(self.siteframe,
                           text=self.control.news_site,
                           bd=-1, fg='black',
                           width = 28,
                           height = 1,
                           bg='white', font=self.font_main_title,
                           justify='center',
                          )
        site_title.pack(fill='both')

    def news_window(self):
        '''  Method to display the news window which will contain the news
             item title, news summary '''
        self.newsframe.destroy()
        self.newsframe = Frame(root,
                               width=self.newsbox_x,
                               height=self.newsbox_y,
                               relief='ridge',
                               highlightbackground="black",
                               highlightcolor="black",
                               highlightthickness=1,
                               bg='white')
        self.newsframe.pack(padx=2*self.padding, pady=2*self.padding,
                            fill='both')
        reference_txt = Label(self.newsframe, text=self.reference_text,
                              bd=-1, fg='grey', bg='white',
                              font=self.font_reference)
        reference_txt.pack(side='top', padx=self.padding, pady=self.padding,
                           anchor='w')
        # reference_txt.place(x=self.padding, y=self.padding)

    def news_title(self, i):
        '''  Method to display news item title and reference texts'''
        self.news_title_txt.destroy()
        self.status_txt.destroy()

        self.news_title_txt = Label(self.newsframe,
                                    text=self.feed["entries"][i].title, bd=-1,
                                    anchor='nw', fg='darkblue', bg='white',
                                    font=self.font_news_title,
                                    justify='center',
                                    wraplength=self.newsbox_x)
        self.news_title_txt.pack(padx=self.padding, pady=self.padding,
                                 anchor='w', fill='both')

        # self.news_title_txt.place(x=self.padding,
        #                           y=self.padding + self.news_title_y)

        status_text = ''.join(['Nieuws item: ', str(i+1),' van ',
                               str(self.items),'    '])
        self.status_txt = Label(self.newsframe, text=status_text, bd=-1,
                                fg='grey', bg='white',
                                font=self.font_reference)
        self.status_txt.pack(side='bottom', padx=self.padding,
                              pady=self.padding, anchor='w')
        # self.status_txt.place(x=self.padding,
        #                       y=self.newsbox_y-self.padding - 2 * 8)

    def display_news(self):
        '''  Method to display the news item: title and summary banner plus
             status '''
        self.news_window()
        _news_site = self.control.news_site

        i = 0
        while i < self.items and self.control.run and \
                self.control.news_site == _news_site:

            self.news_title(i)
            news_summary = clean(self.control,
                                 self.feed["entries"][i].summary)

            if self.control.displaybanner:
                self.news_banner(news_summary)

            else:
                self.news_box(news_summary)

            if self.control.next:
                i = (i + 1) % self.items

            elif self.control.previous:
                i = (i - 1) % self.items

            else:
                i += 1

            self.control.reset_controls()

    def news_box(self, news_summary):
        '''  display the news in a text box
        '''
        self.summaryframe.destroy()
        self.summaryframe = Frame(self.newsframe, bg='lightgrey')
        self.summaryframe.pack(padx=self.padding, pady=self.padding,
                               anchor='w', fill='both')
        # self.summaryframe.place(x=self.padding, y=self.news_summary_y)

        news_text = Label(self.summaryframe,
                          text=news_summary,
                          width=width_char-17,
                          height=height_char,
                          justify='left',
                          anchor='nw',
                          font=self.font_summary_box,
                          wraplength=self.newsbox_x - 4 * self.padding,
                         )

        news_text.pack()
        #news_text.insert('end', news_summary)

        x = 0
        buffer = max(80, len(news_summary))
        while x in range(buffer) and not self.control.exit_banner:
            root.update()
            accurate_delay(50)
            x += 1

    def news_banner(self, news_summary):
        '''  display news in a banner
        '''
        self.summaryframe.destroy()
        self.summaryframe = Frame(self.newsframe,
                                   width=self.newsbox_x - 3 * self.padding,
                                   height=self.banner_height, bg='lightgrey')
        self.summaryframe.pack(padx=self.padding, pady=self.padding,
                               anchor='w', fill='both')

        # self.summaryframe.place(x=self.padding, y=self.news_summary_y)

        news_text = Label(self.summaryframe, text=news_summary,
                          font=self.font_summary_banner, bg='lightgrey')
        root.update_idletasks()
        # necessary to get the winfo_reqwidth information

        pixels = int(news_text.winfo_reqwidth() + 0.5 * self.newsbox_x)
        x = width
        y = 0

        while x > (width-pixels) and not self.control.exit_banner:
            # move text object by increments dx, dy
            # -dx --> right to left
            news_text.place(x=x, y=y)
            x = x - self.dx
            root.update()
            accurate_delay(self.delay)
            # message reading time is delay (ms) * pixels -
            # so 10 ms * 1000 pxl = 10 s is depending of the
            # length of the message

    def update_news(self):
        '''  Method to update the news and display the news site
        '''
        news_URL = news_list[self.control.news_site]
        self.feed = feedparser.parse(news_URL)
        self.items = len(self.feed["items"])
        self.reference_txt.destroy()
        self.reference_text = ''.join(['Nieuws update van ', news_URL, ' op ',
                              time.ctime()])


def clean(control, raw_string):
    '''  Function to clean string from unwanted formatting text
    '''
    clean_string = re.sub('&nbsp;', ' ', raw_string)
    clean_string = re.sub(r'<.*?>', '', clean_string)

    if clean_string == '':
        control.next_item()

    if len(clean_string) > summary_too_long:
        clean_string = '###'

    return clean_string


def accurate_delay(delay):
    ''' Function to provide accurate time delay in millisecond
    '''
    _ = time.perf_counter() + delay/1000
    while time.perf_counter() < _:
        pass
