#!/usr/bin/env python

import yaml

import os, sys, time

def get_home_dir() :
    return os.path.expanduser('~')

def get_conf_dir():
    d = os.path.join(get_home_dir(), '.mailrobot')
    if not os.path.isdir(d):
        os.mkdir(d)
        os.mkdir(os.path.join(d, 'emails'))
    return d

def get_conf_file():
    return yaml.load(open(os.path.join(get_conf_dir(), 'mailrobotrc.yaml')))

def get_mailbox_dir(mailbox=''):
    d = os.path.join(get_conf_dir(), 'emails', mailbox)
    if not os.path.isdir(d):
        os.mkdir(d)
    return d

def get_today_mail_dir(mailbox=''):
    def get_date():
        t = time.localtime(time.time())
        return '%d-%d-%d' % (t.tm_year, t.tm_mon, t.tm_mday)

    d = os.path.join(
        get_mailbox_dir(mailbox), get_date())
    if not os.path.isdir(d): os.mkdir(d)
    return d
