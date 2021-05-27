# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: email_handler.py
    Time: 2021/4/10 下午4:49
-------------------------------------------------
    Change Activity: 2021/4/10 下午4:49
-------------------------------------------------
    Desc: 
"""
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class EmailHandler(object):
    mail_host = 'smtp.qq.com'
    mail_user = '2027762055@qq.com'
    mail_pass = 'lcpzxzargptleibi'
    sender = '2027762055@qq.com'
    receivers = ['qinjiahu@gnlab.com']

    @staticmethod
    def __send_email_image(image_path, title):
        send_str = f'''
            <html><body>
                <img src="cid:image1" alt="image1" align="center" width=100% >
            </body></html>
        '''

        # 构建message
        msg = MIMEMultipart()

        # 添加邮件内容
        content = MIMEText(send_str, _subtype='html', _charset='utf8')
        msg.attach(content)

        # 构建并添加图像对象
        img1 = MIMEImage(open(image_path, 'rb').read(), _subtype='octet-stream')
        img1.add_header('Content-ID', 'image1')
        msg.attach(img1)

        # 邮件主题
        msg['Subject'] = title

        # 邮件收、发件人
        msg['To'] = EmailHandler.receivers[0]
        msg['From'] = EmailHandler.sender

        try:
            # 登录邮箱
            server = smtplib.SMTP_SSL("smtp.qq.com", port=465)
            server.login(EmailHandler.sender, EmailHandler.mail_pass)
            server.sendmail(EmailHandler.sender, EmailHandler.receivers, msg.as_string())
            server.quit()
        except smtplib.SMTPException as e:
            print('send_email_image.error: ', e)  # 打印错误

    @staticmethod
    def __send_email(content, title):
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = EmailHandler.sender
        # 接受方信息
        message['To'] = EmailHandler.receivers[0]

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(EmailHandler.mail_host, 25)
            # 登录到服务器
            smtpObj.login(EmailHandler.mail_user, EmailHandler.mail_pass)
            # 发送
            smtpObj.sendmail(EmailHandler.sender, EmailHandler.receivers, message.as_string())
            # 退出
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print('__send_email.error: ', e)  # 打印错误

    @staticmethod
    def send_email(title, image_path=None):
        content = f'cookie 失效，请及时补充 {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}'

        if image_path:
            EmailHandler.__send_email_image(image_path, title)

        else:
            EmailHandler.__send_email(content, title)


if __name__ == "__main__":
    EmailHandler.send_email('JD 商家后台 Cookie')
