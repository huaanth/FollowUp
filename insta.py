from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

username =""
password = ""
count =0

def login(driver):
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(u'\ue007')

def click(driver, css_selector):
    element = WebDriverWait(driver,20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR), css_selector)
    )
    element.click()

def navigate(driver):
    dropdown = '[alt*="' + username + '"]'
    profile = "[href*=\"" + username +"\"]"
    click(driver, dropdown)
    click(driver, profile)

def get_usernames(driver):
    list_xpath = "//div[@role='dialog']//li"
    WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH), list_xpath)
    )
    
    scroll_down(driver)
    list_elmt = driver.find_elements_by_xpath(list_xpath)
    time.sleep(1)
    for i in range(len(list_elmt)):
        try:
            row_text = list_elmt[i].text
            if "Follow" in row_text:
                follower_user = row_text[:row_text.index("\n")]
                users += [follower_user]
        except:
            print("continue")
    return users

def scroll_down(driver):
        global count
        ind = 0
        while 1:
            scroll_top_num = str(ind*1000)
            ind +=1
            driver.execute_script("document.querySelector('div[role=dialog] ul').parentNode.scrollTop="+scroll_top_num)

            try:
                WebDriverWait(driver, 1).until(check_diff)
            except:
                count = 0
                break
        return

def check_diff(driver):
    global count
    new_count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))

    if new_count != count:
        count = new_count
        return True
    else:
        return False

def doesnt_followback(followers, following):
    followers.sort()
    following.sort()
    fake = []
    for i in range(len(following)):
        try:
            followers.index(following[i])
        except ValueError:
            fake += [following[i]]
    return fake


def __main__():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(1)
    login(driver)
    navigate(driver)
    
    follower_css = "[href*=\"" + username +"/followers/\"]"
    css_close = '[aria-label="Close"]'
    following_css ="[href*=\"" + username +"/following/\"]"

    click(driver, follower_css)
    follower_list = get_usernames(driver)

    click(driver, css_close)

    click(driver, following_css)
    following_list = get_usernames(driver,following_css)

    fin =doesnt_followback(follower_list, following_list)

    return fin

    