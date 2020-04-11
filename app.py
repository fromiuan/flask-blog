#!/usr/bin/python
# -*- coding: UTF-8 -*-

from app import create_app
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.run()
