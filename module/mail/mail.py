# -*- coding: utf-8 -*-

from util.mail.sender import Sender

class Mail(object):

    @staticmethod
    def send(msg, sub, attachments={}):
        sender = Sender(msg, sub)
        if len(attachments.items()) > 0:
            [sender.add_attachment(name, path) for name, path in attachments.items()]
        sender.send()