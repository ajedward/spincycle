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

        # Creation de la barre de menu
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        id = 8000 # id offset pour le sous-menu de modules
        filemenu.Append(wx.ID_NEW, "New\tCtrl+N")
        self.Bind(wx.EVT_MENU, self.onNew, id=wx.ID_NEW)
        filemenu.Append(wx.ID_OPEN, "Open\tCtrl+O")
        self.Bind(wx.EVT_MENU, self.onOpen, id=wx.ID_OPEN)
        filemenu.Append(wx.ID_SAVE, "Save\tCtrl+S")
        self.Bind(wx.EVT_MENU, self.onSave, id=wx.ID_SAVE)
        filemenu.Append(wx.ID_SAVEAS, "Save As...\tShift+Ctrl+S")
        self.Bind(wx.EVT_MENU, self.onSaveAs, id=wx.ID_SAVEAS)

        filemenu.AppendSeparator()

        filemenu.Append(10000, "Load Left Turntable Sample...\tShift+Ctrl+L")
        self.Bind(wx.EVT_MENU, self.onLoadTTableLeft, id=10000)
        filemenu.Append(10001, "Load Right Turntable Sample...\tShift+Ctrl+R")
        self.Bind(wx.EVT_MENU, self.onLoadTTableRight, id=10001)

        filemenu.AppendSeparator()

        quititem = filemenu.Append(wx.ID_EXIT, "Quit\tCtrl+Q", "")
        self.Bind(wx.EVT_MENU, self.onQuit, id=wx.ID_EXIT)
        
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)


        self.panel = wx.Panel(self)
        self.timer=wx.Timer(self)
        self.timer.Start(milliseconds=5, oneShot=False)

        self.turntableL = Turntable(self.panel, pos=(50,50), size=(400,500))
        self.turntableR = Turntable(self.panel, pos=(650,50), size=(400,500))

        self.Bind(wx.EVT_TIMER,self.OnTimer)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Show()

    def OnPaint(self, evt):
        pass
        #print "TRACE: MyFrame Paint()"

    def OnTimer(self, event):
        self.turntableL.Refresh()
        self.turntableR.Refresh()

    def onNew(self, evt):
        print 'TRACE: new'
        
    def onOpen(self, evt):
        print 'TRACE: onOpen'

    def onSave(self, evt):
        print 'TRACE: save'
        
    def onSaveAs(self, evt):
        print 'TRACE: saveAs'

    def onLoadTTableLeft(self, evt):
        print 'TRACE: loadTTableLeft'
        self.__loadTable(evt, self.turntableL)

    def onLoadTTableRight(self, evt):
        print 'TRACE: loadTTableRight'
        self.__loadTable(evt, self.turntableR)
        
    def __loadTable(self, evt, turntable):
        # Choose an AIF file.
        wildcard = "Audio file (.aif)|*.aif"
        # Set up the dialog.
        dlg = wx.FileDialog(self, "Open Audio sample...", os.path.expanduser("~"), 
                            wildcard=wildcard, style=wx.FD_OPEN)
        # ShowModal() opens a modal dialog and waits for user interaction.
        # ("Open" or "Cancel" to return a value). We use the return value
        # to decide on a course of action.  The "Open" button returns the wx.ID_OK
        # constant.
        if dlg.ShowModal() == wx.ID_OK:
            # Get the path of the chosen file.
            path = dlg.GetPath()
            # Make sure that a file was chosen.
            if path == "":
                return
            # Keep the file's path in memory.
            turntable.setCurrentFilePath(path)
            # Adjust the title of the turntable
            #
            # TODO: adjust the title of the turntable. 
            # TODO: reset the turntable
            #
            # Open the sound file in 'read' mode.
            f = open(path, "r")
            # TODO: Read the binary file, choose another method if necessary.
            #text = f.read()
            # close the file.
            f.close()
            
            # TODO : process the audio file into a table.

        # Destroy the dialog.
        dlg.Destroy()

    def onQuit(self, evt):
        print 'TRACE: quit'
        # Arret du serveur audio
        s.stop()
        # Menage avant de quitter
        self.Destroy()

app = wx.App(False)
frame = MyFrame()
app.MainLoop()
