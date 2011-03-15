#!/usr/bin/env python

import imapclient

def login_emailbox(host, user, password, ssl=True):
    client = imapclient.IMAPClient(host, ssl=ssl)
    client.login(user, password)
    return client

def logout_emailbox(client):
    client.logout()
    
def get_matched_messages(client, folder = 'INBOX'):
    def is_matched(msg):
        return msg.find('From: MyPoints BonusMail') != -1
    
    client.select_folder(folder)
    
    msgs = client.fetch(client.search('(UNSEEN)'), ('RFC822',)).values()
    client.set_flags([ i['SEQ'] for i in msgs ], ('UNSEEN',))

    return [ i for i in msgs if is_matched(i['RFC822']) ]
