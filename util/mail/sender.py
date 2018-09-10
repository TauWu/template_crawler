# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

from constant.config import EMAIL_CFG
from util.common.logger import LogBase

class Sender():

    def __init__(self, msg="", subject="", recvers=None):
        '''Sender
        params:
            msg:     Content
            subject: Subject
        '''
        if recvers is None:
            self.recvers = EMAIL_CFG['recver'].split(',')
        else:
            if isinstance(recvers, list):
                self.recvers = recvers
            else:
                self.recvers = recvers.split(',')
        self.logger = LogBase('email', "email_sender")
        self.__smtp_predo__

        self.msg = MIMEMultipart()
        self.msg.attach(MIMEText(msg, 'html', 'utf-8'))

        self.msg['From'] = formataddr([EMAIL_CFG['sender_name'], EMAIL_CFG['sender']])
        self.msg['To'] = formataddr(["", ",".join(self.recvers)])
        self.msg['Subject'] = Header(subject, 'utf-8')

    def add_attachment(self, filename, filepath):
        '''add_attachment
        params:
            filename: display name
            filepath: attachment path
        '''
        attach = MIMEText(open(filepath, "rb").read(), 'base64', 'utf-8')
        attach["Content-Type"] = 'application/octet-stream'
        attach["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
        self.msg.attach(attach)

    def send(self):
        try:
            self.__smtp.sendmail(EMAIL_CFG['sender'], self.recvers, self.msg.as_string())
        except Exception:
            self.logger.error("Send mail FAILED!")
        else:
            self.logger.info("Send mail success!", recver=self.recvers)
        finally:
            self.__smtp_aftdo__

    @property
    def __smtp_predo__(self):
        # Connect to smtp server.
        try:
            self.__smtp = smtplib.SMTP_SSL()
            self.__smtp.connect(EMAIL_CFG["smtp_server"], EMAIL_CFG["smtp_port"])
            self.__smtp.ehlo()
        except Exception:
            self.logger.error('Connect to SMTP server FAILED.', server=EMAIL_CFG["smtp_server"])
        else:
            self.logger.info('Connect to SMTP server succeed.', server=EMAIL_CFG["smtp_server"])

        # Login sender email.
        try:
            self.__smtp.login(user=EMAIL_CFG['sender'], password=EMAIL_CFG['sender_pwd'])
        except Exception:
            self.logger.error('Login FAILED.', user=EMAIL_CFG['sender'])
        finally:
            self.logger.info('Login succeed.', user=EMAIL_CFG['sender'])

    @property
    def __smtp_aftdo__(self):
        self.__smtp.quit()


if __name__ == "__main__":
    email_sender = Sender('测试用的文本<p></p><font color="grey">第二个测试</font>', "测试用的主题")
    email_sender.send()