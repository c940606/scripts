import json
import smtplib
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import request, parse
import mistune

def wechat_reminder(miao_code, text):
    page = request.urlopen(
        "http://miaotixing.com/trigger?" + parse.urlencode({"id": miao_code, "text": text, "type": "json"}))
    result = page.read()
    jsonObj = json.loads(result)
    if (jsonObj["code"] == 0):
        print("成功")
    else:
        print("失败，错误代码：" + str(jsonObj["code"]) + "，描述：" + jsonObj["msg"])


def email_reminder(to_emails, subject, contents):
    cfg = ConfigParser()
    cfg.read('config.ini')
    # 发送方，授权码
    my_email = cfg.get("personal_information", "my_email")
    pwd = cfg.get("personal_information", "authorizationCode")

    msg = MIMEMultipart()

    # 把内容加进去
    msg.attach(MIMEText(contents, 'plain', 'utf-8'))
    # markdown 转 html
    

    # # 添加附件
    # att1 = MIMEText(open('result.xlsx', 'rb').read(), 'base64', 'utf-8')  # 打开附件
    # att1['Content-Type'] = 'application/octet-stream'  # 设置类型是流媒体格式
    # att1['Content-Disposition'] = 'attachment;filename=result.xlsx'  # 设置描述信息
    #
    # att2 = MIMEText(open('1.jpg', 'rb').read(), 'base64', 'utf-8')
    # att2['Content-Type'] = 'application/octet-stream'  # 设置类型是流媒体格式
    # att2['Content-Disposition'] = 'attachment;filename=1.jpg'  # 设置描述信息
    #
    # msg.attach(att1)  # 加入到邮件中
    # msg.attach(att2)

    # 设置邮件主题
    msg['Subject'] = subject

    # 发送方信息
    msg['From'] = my_email

    # 开始发送

    # 通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 登录邮箱
    s.login(my_email, pwd)
    # 开始发送
    s.sendmail(my_email, to_emails, msg.as_string())

# if __name__ == '__main__':
#     # wechat_reminder("tSafTa1", "你好")
#     # email_remain(["caiwei4@zte.com.cn", "762307667@qq.com"], "hello主题", "hello内容")
#     # cfg = ConfigParser()
#     # print(cfg.get("personal_information", "my_email"))
