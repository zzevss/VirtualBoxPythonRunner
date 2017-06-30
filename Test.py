# import os
# os.chdir('C:\\Test\\')


import time
from pywinauto import application
import unittest

__SLEEP__ = True


def sleep(timer):
    if __SLEEP__:
        return time.sleep(timer)

class TestStringMethods(unittest.TestCase):

    def test_print(self):
        print('START')
        app = application.Application(backend="win32").start("C:\\Test\\PDFRedirect.exe")
        print(app)
        mainWindow = app.PDFRedirect
        print(mainWindow)
        mainWindow.Wait('ready')

        sleep(2)
        printerName = mainWindow.ComboBox4
        print(printerName)
        printerName.Select('Microsoft XPS Document Writer')
        printerName.Select('Fax')
        printerName.Select('Microsoft XPS Document Writer')
        printerName.Select('Fax')

        mainWindow['...'].Click()
        dialogWindow = app.Dialog
        dialogWindow.Wait('ready')
        dialogWindow['Отмена'].Click()
        mainWindow.Close()


if __name__ == '__main__':
    unittest.main()
