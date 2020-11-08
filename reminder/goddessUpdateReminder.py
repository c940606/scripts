from selenium import webdriver
from typing import Set
from ruamel import yaml
from reminder import wechat_reminder
import os


def viewWeibo():
    driver.get("https://weibo.com/p/1005055308938398/home?is_all=1")
    cur_time = driver.find_element_by_xpath(
        r'//*[@id="app"]/div[1]/div[1]/div[4]/div/div/header/div/div/h4/span[1]').text
    cur_content = driver.find_element_by_xpath(
        r'//*[@id="app"]/div[1]/div[1]/div[4]/div/div/article/div[1]/div[1]').text
    return [cur_time, cur_content]


def viewZhihu():
    driver.get("https://www.zhihu.com/people/liu-yan-hong-73-29")
    cur_time = driver.find_element_by_xpath(r'//*[@id="Profile-datalist"]/div/div[1]/div[1]/div/span[2]').text
    cur_content = driver.find_element_by_xpath(r'//*[@id="Profile-datalist"]/div/div[1]/div[2]/h2/div/a').text
    return [cur_time, cur_content]


def viewNetEaseCloud() -> Set[str]:
    """获取网页云最近一周的歌"""
    options.add_argument('user-agent=""')
    driver = webdriver.Chrome(r"D:\learning\projects\chromedriver.exe", options=options)
    recent_playlist = set()
    driver.get("https://music.163.com/#/user/home?id=474258173")
    driver.switch_to.frame('g_iframe')
    for song in driver.find_elements_by_xpath(r'/html/body/div[3]/div/div[3]/div/div[1]/ul/li'):
        recent_playlist.add(song.text.split("\n")[-1])
    return recent_playlist


def compareFiles(current_information):
    last = {}
    if os.path.exists(r"setting\setting.yaml"):
        with open(r"setting\setting.yaml", "r", encoding="utf-8") as f:
            last = yaml.safe_load(f.read())
    send_text = []
    template = "女神{state}更新{name},内容为{content}"
    for key in current_information.keys():
        cmp_result = {
            "state": "未",
            "name": key,
            "content": "空"
        }
        if (key == "NetEaseCloud" and current_information.get(key, set()) - last.get(key, set())) \
                or current_information.get(key, "") != last.get(key, ""):
            cmp_result["state"] = "已"
            cmp_result["content"] = current_information[key]
        send_text.append(template.format(**cmp_result))
    # 更新原来文件
    with open(r"setting\setting.yaml", "w", encoding="utf-8") as f:
        yaml.dump(current_information, f, default_flow_style=False, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    return "\n".join(send_text)


def main():
    current_information = {}
    # 微博
    current_information["Weibo"] = viewWeibo()
    # 知乎
    current_information["Zhihu"] = viewZhihu()
    # 网易云
    current_information["NetEaseCloud"] = viewNetEaseCloud()
    send_text = compareFiles(current_information)
    wechat_reminder("tmzjfnL", send_text)


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # 用手机头
    options.add_argument(
        'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument("---headless")
    driver = webdriver.Chrome(r"D:\learning\projects\chromedriver.exe", options=options)
    driver.implicitly_wait(20)
    try:
        main()
    except:
        pass
    finally:
        driver.quit()
    # compareFiles({})
