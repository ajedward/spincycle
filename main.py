#!/usr/bin/python

# turntables project.

# import WX Python
import wx
from pyo import *
from turntable import Turntable

# start the pyo server.
s = Server()

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
        self.timer=wx.Timer(self)
        self.timer.Start(milliseconds=5, oneShot=False)

        self.turntableL = Turntable(self.panel, pos=(50,50), size=(400,400))
        self.turntableR = Turntable(self.panel, pos=(650,50), size=(400,400))

        self.Bind(wx.EVT_TIMER,self.OnTimer)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Show()

    def OnPaint(self, evt):
        print "TRACE: MyFrame Paint()"

    def OnTimer(self, event):
        self.turntableL.Update()
        self.turntableR.Update()
        self.turntableL.Refresh()
        self.turntableR.Refresh()
        
app = wx.App(False)
frame = MyFrame()
app.MainLoop()
