import wx
from random import randint
import math
import time
import os.path

""" 
  La class Turntable, lorsque attache a un Panel ou un Frame, affiche une table tournante qui permet plusieurs
  fonctions, tels que :
  - Demarrer/arreter (bouton moteur) complete
    TODO: ajouter un 'ease' pour que ca commence et arrete tranquillement.
  - Rotation de la table tournante.
  - Arret du disque 'vinyle' lorsque la souris est 'clique'
  - Mouvement du disque 'vinyle' lorsque la souris est bouge avec le bouton envonce
    TODO: percevoir la position sur le disque, inverser sur le cote droite, appliquer
          sur l'axe des 'X' lorsqu'on se trouve en haut ou en bas du disque
  - TODO: Verser des 'samples' en format WAV, AIF, etc. pour chaque table tournante.
  - TODO: Faders, et Crossfader.
  - TODO: Engin de granulation qui permet de controller la position dans le sample 
          et la frequence avec la manipulation des vinyles.
  - TODO: 'raideur' du cross-fade.
"""

class Turntable(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent=parent, pos=pos, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.pos = None
        self.selected = None

        # rotationsPerSecond is 33 1/3 divided by seconds per minute 
        self.rotationsPerSecond = (100/3.0) / 60.0

        self.millisAtLastPaint = None
        self.curMillis = None
        self.curRotateFactor = None

        self.currentFilePath = None

        w,h = self.GetSize()
        self.motorOnButton = wx.ToggleButton(self, id=1, label="Moteur", pos=(320,320))
        self.motorOnButton.SetValue(True)
        self.resetButton = wx.Button(self, id=2, label="Reset", pos=(320,340))
        self.dirPathCtrl = wx.TextCtrl(self, id=3, value='<set a value>', pos=(50,h-120), size=(w-100,20))
        self.fileNameCtrl = wx.TextCtrl(self, id=4, value='<set a value>', pos=(50,h-90), size=(w-200,20))
        self.revCountCtrl = wx.TextCtrl(self, id=5, value='rev 0', pos=(w-150,h-90), size=(100,20))
        
        self.motorOn = True
        self.drop = True # 'drop' in DJ talk means vinyl is being rotated by the motor of the turntable

        #print "TRACE: Rotations per second", self.rotationsPerSecond

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)

        self.Bind(wx.EVT_TOGGLEBUTTON, self.toggleMotor, id=1)
        self.Bind(wx.EVT_BUTTON, self.reset, id=2)
        
    def setCurrentFilePath(self, path):
        print "TRACE: setCurrentFilePath()"
        self.currentFilePath = path
        self.dirPathCtrl.SetValue(os.path.dirname(self.currentFilePath))
        self.fileNameCtrl.SetValue(os.path.basename(self.currentFilePath))

    def reset(self, evt):
        print "TRACE: reset()"
        self.millisAtLastPaint = None
        self.curMillis = None
        self.curRotateFactor = None

    def toggleMotor(self, evt):
        print "TRACE: toggleMotor()"
        self.motorOn = self.motorOnButton.GetValue()

    def onPaint(self, evt):

        #print "TRACE: onPaint"
        if self.curMillis == None:
            self.curMillis = self.millisAtLastPaint = int(round(time.time() * 1000))
        else:
            self.curMillis = int(round(time.time() * 1000))

        # elapsedMs are the MS since the last paint event.  We use this to increment LP rotation.
        elapsedMs = float(self.curMillis - self.millisAtLastPaint)

        #print "TRACE: elapsedMs is ", elapsedMs 

        # rotation factor since last paint.
        radRotateFactor = ((math.pi * 2.0) * (self.rotationsPerSecond * elapsedMs * 0.001))

        if self.curRotateFactor == None:
            self.curRotateFactor = 0
        elif self.drop and self.motorOn:
            self.curRotateFactor += radRotateFactor

        # update the revolution counter.
        self.revCountCtrl.SetValue('rev ' + str(round(self.curRotateFactor / (math.pi * 2),1)))
        w,h = self.GetSize()

        # ajust the width and height such that they are slightly smaller than the entire container
        h = w
        w -= (w/12)
        h -= (h/12)

        dc = wx.AutoBufferedPaintDC(self)

        # draw the vinyl album.
        dc.SetBrush(wx.Brush("#222222"))
        dc.DrawEllipse(0,0,w,h)

        # draw the label of the vinyl album
        labelW = w / 3.2
        middleXPos = w/2
        middleYPos = h/2
        dc.SetBrush(wx.Brush("#FFFFFF"))
        dc.DrawEllipse(0 + middleXPos - labelW/2,
                       0 + middleYPos - labelW/2, 
                       labelW,
                       labelW)

        # draw the spindle hole of the vinyl album
        spindleW = labelW / 8
        dc.SetBrush(wx.Brush("#000000"))
        dc.DrawEllipse(0 + middleXPos - spindleW/2,
                       0 + middleYPos - spindleW/2, 
                       spindleW,
                       spindleW)

        #draw the teal radius guide lines
        dc.SetPen(wx.Pen("#00FFFF"))
        for i in range(0,12):
            rads = i * ((2 * math.pi) / 12)
            startXLinePos = math.cos(rads + self.curRotateFactor) * (labelW/2) + middleXPos
            startYLinePos = math.sin(rads + self.curRotateFactor) * (labelW/2) + middleYPos
            endXLinePos = math.cos(rads + self.curRotateFactor) * (w/2) + middleXPos
            endYLinePos = math.sin(rads + self.curRotateFactor) * (w/2) + middleYPos
            if (i != 11):
                pass
                #disabled the sectional indicators for now, there were some refresh issues
                # that were visually distracting.
                #dc.DrawLine(startXLinePos, startYLinePos, endXLinePos, endYLinePos)
            else:
                # draw a special red marker that marks the beginning of the sample
                # (at 2:00 o'clock, 11th position counterclockwise from horizontal origin).
                penSize = 3
                dc.SetPen(wx.Pen("#FF0000", penSize))
                dc.DrawLine(startXLinePos, startYLinePos, endXLinePos, endYLinePos)
                dc.SetPen(wx.Pen("#00FFFF", 1))

        # reset pen to black, 1 pixel.
        dc.SetPen(wx.Pen("#000000", 1))

        # make sure that millisAtLastPaint is set.
        self.millisAtLastPaint = self.curMillis

        # draw the marker that indicates the 'scratch sample' begin position
        # draw the label at 2 o'clock (11/12 running counter clockwise
        # from horizontal position.
#        rads = 11 * ((2 * math.pi) / 12)
#        dc.SetBrush(wx.Brush("#FF0000"))
#        startLabelW = 30
#        startLabelH = 10
#        dc.DrawRectangle(middleXPos + labelW/2,
#                         middleYPos - startLabelH/2, 
#                         startLabelW,
#                         startLabelH)

    def onMouseDown(self, evt):
        self.drop = False
        self.CaptureMouse()
        self.pos = evt.GetPosition()
        print "TRACE: mouse down, position is ", self.pos


    def onMouseUp(self, evt):
        if self.HasCapture():
            self.drop = True
            self.pos = evt.GetPosition()
            print "TRACE: mouse up, position is ", self.pos
            self.ReleaseMouse()
            self.pos = self.selected = None
            self.Refresh()

    def onMotion(self, evt):
        w,h = self.GetSize()
        if self.HasCapture():
            (xPos, yPos) = evt.GetPosition()
            print "TRACE: moving mouse ", (xPos, yPos)

            # if yDiff is negative, we are moving down.  If yDiff is positive, we are going up.
            yDiff = yPos - self.pos[1]

            directionString = "NOWHERE"

            if yDiff < 0:
                directionString = "UP"
            elif yDiff > 0:
                directionString = "DOWN"

            print "TRACE: we are going ", directionString

            self.curRotateFactor += (-yDiff * 2 * math.pi) / 300

            self.pos = (xPos, yPos)
            self.Refresh()

if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self, parent=None, id=wx.ID_ANY, title="Interface 2D", pos=(50,50), size=(500,500)):
            wx.Frame.__init__(self, parent, id, title, pos, size)
            self.panel = wx.Panel(self)
            self.turntable = Turntable(self.panel, pos=(50,50), size=(150,150), callback=self.getXY)
            self.Show()
            
        def getXY(self, x, y):
            print x, y

    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
