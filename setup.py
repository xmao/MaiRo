#!/usr/bin/env python

from glob import glob 
from distutils.core import setup

setup(name = "grobot",
      version = "0.1",
      description = "Gmail robot",
      author = "Xizeng Mao, Yumin Liu",
      author_email = "xizeng.mao@gmail.com",
      url = "http://csbl.bmb.uga.edu/~xizeng/",
      package_dir = {"mailrobot":"mailrobot"},
      packages = ['mailrobot', 'mailrobot/imapclient', 'mailrobot/yaml'], )
