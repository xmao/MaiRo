#!/usr/bin/env python

from glob import glob 
from distutils.core import setup

setup(name = "mairo",
      version = "0.1",
      description = "Mail robot",
      author = "Xizeng Mao, Yumin Liu",
      author_email = "xizeng.mao@gmail.com",
      url = "http://csbl.bmb.uga.edu/~xizeng/",
      package_dir = {"mairo":"mairo"},
      packages = ['mairo', 'mairo/imapclient', 'mairo/yaml'], )
