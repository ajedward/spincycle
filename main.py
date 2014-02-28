#!/usr/bin/python

# turntables project.

# import WX Python
import wx
from pyo import *
from turntable import Turntable

# start the pyo server.
s = Server()

#!/usr/bin/python

# Set the MIDI input device number. See pm_list_devices() to obtain valid devices.
print pm_list_devices() 
s.setMidiInputDevice(3)

# start the pyo audio engine.
s.boot().start()

# declare the MyFrame class that extends wx.Frame.
class MyFrame(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY, title="TurnTables", pos=(50,50), size=(1100,700)):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        self.panel = wx.Panel(self)
        self.audio_objects = []

        self.turntableL = Turntable(self.panel, pos=(50,50), size=(400,400))
        self.turntableR = Turntable(self.panel, pos=(650,50), size=(400,400))
        self.Show()
        
    def getXY(self, x, y, node):
        self.audio_objects[node].setP1(x)
        self.audio_objects[node].setP2(y)

app = wx.App(False)
frame = MyFrame()
app.MainLoop()

