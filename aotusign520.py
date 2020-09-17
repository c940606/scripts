from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from reminder.reminder import wechat_reminder


def autoSignIn():
    cfg = ConfigParser()
    cfg.read('config.ini')
    chorme_options = Options()
    chorme_options.add_argument("---headless")
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=chorme_options)
    driver.implicitly_wait(20)
    driver.get("https://www.520ssr.info/auth/login")
    email = cfg.get("personal_information", "my_email")
    password = cfg.get("personal_information", "pwd")

    try:
        driver.find_element_by_id("email").send_keys(email)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_tag_name("button").click()
        driver.find_element_by_xpath('//*[@id="popup-ann-modal"]/div/div/div[3]/button').click()
        driver.find_element_by_xpath('//*[@id="checkin-div"]/a').click()
        wechat_reminder("tSafTa1", "签到成功")
    except:
        wechat_reminder("tSafTa1", "未知错误")
    finally:
        driver.close()


if __name__ == '__main__':
    autoSignIn()
