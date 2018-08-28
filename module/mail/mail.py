# -*- coding: utf-8 -*-

from util.mail.sender import Sender
from os.path import getsize

class Mail(object):

    @staticmethod
    def send(msg, sub, attachments={}):
        sender = Sender(msg, sub)

        checked_attach = dict()
        
        for kv in attachments.items():
            if getsize(kv[1]) <= 50 * 0x400 * 0x400:
                checked_attach = dict(checked_attach, **{kv[0]:kv[1]})

        if len(checked_attach.items()) > 0:
            [sender.add_attachment(name, path) for name, path in checked_attach.items()]
        sender.send()