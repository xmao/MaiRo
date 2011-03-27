#!/usr/bin/env python

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import robot, setting

class RobotAction(QThread):

    def __init__(self, lock, parent=None):
        super(RobotAction, self).__init__(parent)
        self.lock, self.mutex = lock, QMutex()

        self.conf = setting.get_conf_file()

    def run(self):
        import sys, cStringIO
        backup = sys.stdout
        sys.stdout = cStringIO.StringIO()
        
        msg = ''
        for account in self.conf['accounts']:
            old, extra = robot.process(account)
            self.parent().browser.append(sys.stdout.getvalue())
            if old:
                msg += 'MyPoints account: %s\n' % (account[2])
                msg += 'Get %d more points, and you have %d points now :-)\n' % (extra, old + extra)
        sys.stdout.close(); sys.stdout = backup
        self.parent().browser.append(msg or "Get no point today :-(\n")
        self.parent().trayIcon.setToolTip(msg or "Get no point today :-(\n")

class RobotGUI(QDialog):

    def __init__(self, parent = None):
        super(RobotGUI, self).__init__(parent=parent)

        self.browser = QTextBrowser()
        self.browser.append('Processing, wait...\n')

        self.button = QPushButton('I know now')
        self.connect(self.button, SIGNAL('clicked()'), self.quit)

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.quitAction = QAction("&Quit", self, triggered = qApp.quit)

        self.setTrayIcon()
        
        self.setWindowTitle('Mail robot')

        self.lock = QReadWriteLock()
        self.action = RobotAction(self.lock, self)
        self.action.start()

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

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import *

    a = QApplication(sys.argv)
    d = RobotGUI(); d.show()
    
    sys.exit(a.exec_())
