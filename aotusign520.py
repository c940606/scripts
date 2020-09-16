from selenium import webdriver
from configparser import ConfigParser
from reminder.reminder import wechat_reminder, email_reminder

def autoSignIn():
    cfg = ConfigParser()
    cfg.read('config.ini')
    driver = webdriver.Chrome("chromedriver.exe")
    driver.implicitly_wait(10)
    driver.get("https://www.520ssr.info/auth/login")
    email = cfg.get("personal_information", "my_email")
    password = cfg.get("personal_information", "pwd")
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_tag_name("button").click()
    driver.find_element_by_xpath('//*[@id="popup-ann-modal"]/div/div/div[3]/button').click()
    try:
        driver.find_element_by_xpath('//*[@id="checkin-div"]/a').click()
        wechat_reminder("tSafTa1", "签到成功")
    except:
        wechat_reminder("tSafTa1", "未知错误")
    finally:
        driver.close()




if __name__ == '__main__':
    autoSignIn()
