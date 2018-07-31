from tkinter import Tk
from module_news import Controls, Display, root

'''   Newsbanner application for python 3.6

      start:
      python news.py [-b] [news_site]
'''
def main():

    control = Controls()
    control.handleargs()
    print('display: ', control.displaybanner)
    control.create()
    news = Display(control)
    control.site_select(control.news_site)
    control.reset_controls()

    while control.run:
        news.update_news()
        news.site_title()
        news.display_news()

    root.destroy()


if __name__ == "__main__":
    main()
