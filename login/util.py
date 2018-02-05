import json
from email.mime.text import MIMEText
import smtplib
from email.header import Header


class Util(object):
    # json格式化
    @staticmethod
    def format(str):
        return json.dumps(str.json(), indent=4, ensure_ascii=False)

    # 发送邮件
    @staticmethod
    def send_mail(msg, title='他__weibo'):
        mail = MIMEText(msg, 'plain', 'utf-8')
        # 发件邮箱
        from_addr = ''
        # 发件邮箱授权码
        password = ''
        # 发件邮箱smtp服务器
        smtp_server = 'smtp.163.com'
        #收件邮箱
        to_addr = ''

        mail["Subject"] = Header(title, 'utf-8')
        mail["From"] = from_addr
        mail["To"] = to_addr
        try:
            # 端口号依不同发件服务器不同
            server = smtplib.SMTP_SSL(smtp_server, 465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], mail.as_string())
            server.quit()
            print('success')
        except smtplib.SMTPException:
            print('fail')
        pass
