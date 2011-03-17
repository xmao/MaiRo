#!/usr/bin/env python

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import robot, setting

class RobotGUI(QDialog):

    def __init__(self, parent = None):
        super(RobotGUI, self).__init__(parent=parent)
        self.conf = setting.get_conf_file()

        self.browser = QTextBrowser()

        self.button = QPushButton('I know now')
        self.connect(self.button, SIGNAL('clicked()'), self.quit)

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.quitAction = QAction("&Quit", self, triggered = qApp.quit)

        self.setTrayIcon()
        
        self.setWindowTitle('Mail robot')

        QTimer.singleShot(1000, self.processAccounts)

    def quit(self):
        qApp.quit()

    def setTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)
        
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(
            os.path.join(os.path.dirname(__file__), 'images', 'heart.svg')))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        
        self.trayIcon.show()

    def processAccounts(self):
        import sys, cStringIO
        backup = sys.stdout
        sys.stdout = cStringIO.StringIO()
        
        msg = ''
        for account in self.conf['accounts']:
            old, extra = robot.process(account)
            self.browser.append(sys.stdout.getvalue())
            if old:
                msg += 'MyPoints account: %s\n' % (account[2])
                msg += 'Get %d more points, and you have %d points now :-)\n' % (extra, old + extra)
        self.browser.append(msg or "Get no point today :-(\n")
        self.trayIcon.setToolTip(msg or "Get no point today :-(\n")

        sys.stdout.close(); sys.stdout = backup

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import *

    a = QApplication(sys.argv)
    d = RobotGUI(); d.show()
    
    sys.exit(a.exec_())
