from selenium import webdriver, common
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW

# Html Elements
SEND_INVADE_ACCEPT = [
    "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action']"]

MORE = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[3]/button"
SECOND_SEND = '//button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1"]'
MESSAGE_BUTTON = '//a[@class="message-anywhere-button pvs-profile-actions__action artdeco-button "]'


# Define Exception
class MyError(Exception):
    pass


# Selenium Class
class FollowWithSelenium:
    def __init__(self, screen):
        # Define Driver
        opt = webdriver.ChromeOptions()
        opt.add_argument("--start-maximized")
        opt.add_experimental_option("detach", True)
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_service = Service(ChromeDriverManager().install())
        chrome_service.creationflags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(service=chrome_service, options=opt)

        # Links in new data will be follow.
        self.new_data = []
        self.DELAY = 10
        # Links in followed, were followed.
        self.followed = []
        # Screen is the UI.
        self.screen = screen
        # Number is for new data index.
        self.number = 0
        # Func will use for follow process.
        self.func = self.screen.after(0, self.test)

    # This function open entered file, followed.txt file and read them. Then functionn compares these files and update new_data list.
    def add_list(self, text_file):
        self.new_data.clear()
        self.followed.clear()
        self.number = 0

        with open(text_file, encoding="utf-8") as data:
            data = data.readlines()
            for link in data:
                self.screen.update()
                link = link.replace("\n", "")
                self.new_data.append(link)

        try:
            with open("followed_links.txt", encoding="utf-8") as f:
                self.followed = [link.replace("\n", "") for link in f.readlines()]
        except FileNotFoundError:
            with open("followed_links.txt", "w") as f:
                pass

        link_for_follow = []
        link_for_follow.extend(set(self.new_data) - set(self.followed))
        self.new_data = link_for_follow

        if text_file == "linkedin_links.txt":
            self.start_following_linkedin()
        else:
            self.start_following_github()

    # This function runs the follow process in Linkedin.
    def start_following_linkedin(self):
        if self.number < len(self.new_data):
            try:
                link = self.new_data[self.number]

                self.driver.get(f"{link}")
                self.screen.update()
                self.wait('//section[@class="pt5 pb3 ph4"]')

                message_buttons = self.driver.find_elements(By.XPATH, MESSAGE_BUTTON)
                if len(message_buttons) == 2:
                    with open("followed_links.txt", "a", encoding="utf-8") as f_links:
                        f_links.writelines(link + "\n")

                for path in SEND_INVADE_ACCEPT:

                    elements = self.driver.find_elements(By.XPATH, path)
                    if len(elements) == 2:
                        elements[1].click()
                        try:
                            WebDriverWait(self.driver, self.DELAY).until(
                                EC.presence_of_element_located((By.XPATH, SECOND_SEND)))
                            self.driver.find_element(By.XPATH, SECOND_SEND).click()
                        except common.exceptions.TimeoutException:
                            pass

                        self.driver.find_element(By.XPATH, "//body").click()
                        self.followed.append(link)

                        with open("followed_links.txt", "a", encoding="utf-8") as f_links:
                            f_links.writelines(link + "\n")
                        break

                self.number += 1
                self.func = self.screen.after(1000, self.start_following_linkedin)

            except (common.exceptions.InvalidArgumentException, MyError):
                self.number += 1
                self.screen.after_cancel(self.func)
                self.func = self.screen.after(1000, self.start_following_linkedin)

    # This function runs the follow process in GitHub.
    def start_following_github(self):
        self.screen.update()
        try:
            if self.number < len(self.new_data):
                link = self.new_data[self.number]

                self.driver.get(link)
                e = self.driver.find_elements(By.XPATH,
                                              '//input[@name="commit"][@value="Follow"]')
                e[2].click()

                with open("followed_links.txt", "a", encoding="utf-8") as f_links:
                    f_links.writelines(link + "\n")

                self.number += 1
                self.func = self.screen.after(0, self.start_following_github)

        except (common.exceptions.ElementNotInteractableException, MyError, IndexError):
            self.number += 1
            self.screen.after_cancel(self.func)
            self.func = self.screen.after(0, self.start_following_github)

    # This function checks if element is load.
    def wait(self, path):
        try:
            WebDriverWait(self.driver, self.DELAY).until(EC.presence_of_element_located((By.XPATH, path)))

        except (common.exceptions.TimeoutException, common.exceptions.WebDriverException):
            self.driver.refresh()
            raise MyError

    # This function created for define self.func.
    def test(self):
        self.screen.after_cancel(self.func)














