#!/usr/bin/env python

import os, email
import re, urllib2, urllib

import setting, mailbox

def process(account):
    old_points, extra_points = 0, 0

    print "Login email box: %s" % account[0]
    c = mailbox.login_emailbox(
        host = 'imap.gmail.com', ssl = True, user = account[0], password = account[1])
    
    msgs = [ i for i in mailbox.get_matched_messages(c, 'MyPoints') ]
    
    if msgs:    
        logdir = setting.get_today_mail_dir(account[0])
        
        url_pattern = re.compile(r'<a href="([^"]*)".*><img .* alt="Get Points".*')
        
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        urllib2.install_opener(opener)
        
        # Sign into MyPoints
        print "Sign into MyPoints for %s" % account[2]
        params = urllib.urlencode({
            'email' : account[2], 'password' : account[3],
            'action' : 'login', 'onOK' : '/'})
        f = opener.open('https://www.mypoints.com/emp/u/login.do?rloc=%2Femp%2Fu%2Findex.vm%3F', params)
        data = f.read(); f.close()
        
        
        for i in msgs:
            msg = email.message_from_string(i['RFC822'])
            
            print "Processing email: %s, " % msg['Subject'],
    
            try:
                url = url_pattern.findall(i['RFC822'])[0]
            except:
                print "Failed :-("
            else:
                name = ''.join([ j.isalnum() and j or ' ' for j in msg['Subject'] ])
                print >>open(os.path.join(logdir, '%s.eml' % name), 'w'), i['RFC822']
                
                f = opener.open(url)
                print >>open(os.path.join(logdir, '%s.html' % name), 'w'), f.read()
                f.close()
                c.set_flags(i['SEQ'], (r'\SEEN', ))
                
                if old_points == 0:
                    points_pattern = re.compile(r'you have <span [^>]*>(\d+)</span> *Points!')
                    old_points = int(points_pattern.findall(i['RFC822'])[0])
                extra_points += 5
                    
                print "Succeeded :-)"
                    
        # Sign out of MyPoints
        print "Sign out of MyPoints"
        f = opener.open('https://www.mypoints.com/emp/u/logout.do')
        f.read(); f.close()
    
    # Log out of emailbox
    print "Log out of email box: %s" % account[0]
    mailbox.logout_emailbox(c)
    return old_points, extra_points

if __name__ == '__main__':
    import sys

    conf = setting.get_conf_file()

    msg = ''
    for account in conf['accounts']:
        old, extra = process(account)
        if old:
            msg += 'MyPoints account: %s\n' % (account[2])
            msg += 'Get %d more points, and you have %d points now :-)\n' % (extra, old + extra)
    print msg
        
