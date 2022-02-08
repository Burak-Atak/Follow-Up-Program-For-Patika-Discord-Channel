from tkinter import *
from get_links import GetLinks
from selenium_for_program import FollowWithSelenium

# Colors For UI
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


# UI Class
class UserInterface:

    def __init__(self):
        self.screen = Tk()
        self.screen.config(padx=100, pady=100, bg=YELLOW)
        self.screen.title("Follow Up Program For Patika Discord Channel")
        self.Follow = FollowWithSelenium(self.screen)

        # BUTTONS
        start_button_linkedin = Button(text="Start Follow in Linkedin",
                                       font=(FONT_NAME, 12, ""),
                                       highlightthickness=0,
                                       bg=GREEN,
                                       width=25,
                                       command=lambda: self.start_following_linkedin())

        start_button_linkedin.grid(row=1, column=2, sticky="w")

        start_button_github = Button(text="Start Follow in Github",
                                     font=(FONT_NAME, 12, ""),
                                     highlightthickness=0,
                                     bg=GREEN,
                                     width=23,
                                     command=lambda: self.start_following_github())

        start_button_github.grid(row=1, column=1, sticky="w")

        get_links_github_button = Button(text="Get Links For GitHub",
                                         font=(FONT_NAME, 12, ""),
                                         highlightthickness=0,
                                         bg=GREEN,
                                         width=23,
                                         command=lambda: self.call_github())

        get_links_github_button.grid(row=0, column=1, sticky="w")

        get_links_linkedin_button = Button(text="Get Links For Linkedin",
                                           font=(FONT_NAME, 12, ""),
                                           highlightthickness=0,
                                           bg=GREEN,
                                           width=25,
                                           command=lambda: self.call_linkedin())

        get_links_linkedin_button.grid(row=0, column=2, sticky="w")

        # Labels
        get_links_label = Label(text="Get Links:",
                                font=(FONT_NAME, 20, ""),
                                highlightthickness=0,
                                bg=YELLOW)

        get_links_label.grid(row=0, column=0, sticky="w")

        start_following_label = Label(text="Start Following:",
                                      font=(FONT_NAME, 20, ""),
                                      highlightthickness=0,
                                      bg=YELLOW)

        start_following_label.grid(row=1, column=0, sticky="w")

        authorization_label = Label(text="Authorization Key:",
                                    font=(FONT_NAME, 20, ""),
                                    highlightthickness=0,
                                    bg=YELLOW)

        authorization_label.grid(row=2, column=0, sticky="w")

        # Entry
        self.authorization_entry = Entry(width=82)
        self.authorization_entry.grid(row=2, column=1, sticky="w", columnspan=2, ipady=4)

        self.get_link = GetLinks()
        self.screen.mainloop()

    # Get Link for Linkedin
    def call_linkedin(self):
        authorization = self.authorization_entry.get()
        self.get_link.read_file(authorization, linkedin=True)

    # Get Link for GitHub
    def call_github(self):
        authorization = self.authorization_entry.get()
        self.get_link.read_file(authorization, linkedin=False)

    # Start to follow in Linkedin
    def start_following_linkedin(self):
        self.Follow.add_list("linkedin_links.txt")

    # Start to follow in GitHub
    def start_following_github(self):
        self.Follow.add_list("github_links.txt")
