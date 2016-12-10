from ctypes import *
MessageBox = windll.user32.MessageBoxW
MessageBox(0, u"[MESSAGE]", 4)