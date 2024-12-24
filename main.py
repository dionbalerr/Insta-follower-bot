from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

SIMILAR_ACCOUNT = "chefsteps"
USERNAME = "MY_USERNAME"
PASSWORD = "MY_PASSWORD"


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url)
        time.sleep(2)

        username = self.driver.find_element(by=By.NAME, value="username")
        password = self.driver.find_element(by=By.NAME, value="password")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        time.sleep(1)
        password.send_keys(Keys.ENTER)

        # Using contains() and text() to find button w/ certain text cause XPATH and selectors change every time you load the page
        time.sleep(3)
        # save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
        # if save_login_prompt:
        #     save_login_prompt.click()
        #
        # time.sleep(2)
        # notifications_prompt = self.driver.find_element(by=By.XPATH, value="// button[contains(text(), 'Not Now')]")
        # if notifications_prompt:
        #     notifications_prompt.click()


    def find_followers(self):
        time.sleep(5)
        # Show followers of the selected account.
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}")

        time.sleep(2)

        follower_button = self.driver.find_element(by=By.XPATH, value="//div/a[contains(text(), 'followers')]")
        if follower_button:
            follower_button.click()

        time.sleep(2)
        # Target the div with scrollbar
        modal_xpath = "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        modal = self.driver.find_element(by=By.XPATH, value=modal_xpath)
        for i in range(5):
            # executing some Javascript
            # using Javascript to say: "scroll the top of the modal (popup) element to the bottom height of the modal (popup)"
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)

            time.sleep(0.5)
        self.driver.execute_script("arguments[0].scrollTo(0, 0)", modal)

    def follow(self):
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, value="button")

        # start at 2 cause 0 is follow main acc, 1 is X button
        for button in all_buttons[2:]:
            try:
                button.click()
                time.sleep(1.1)
            # Clicking button for someone who is already being followed will trigger dialog to Unfollow/Cancel
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_button.click()




bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()