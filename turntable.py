import wx
from random import randint
import math
import time

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
        self.origRotateFactor = None

        
        self.motorOn = True
        self.drop = True # 'drop' in DJ talk means vinyl is being rotated by the motor of the turntable

        print "Rotations per second", self.rotationsPerSecond

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_MOTION, self.Motion)
        
    def OnPaint(self, evt):

        #print "TRACE: OnPaint"
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
            self.curRotateFactor = self.origRotateFactor = 0
        elif self.drop:
            self.curRotateFactor += radRotateFactor

        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        # draw the vinyl album.
        dc.SetBrush(wx.Brush("#444444"))
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

    def MouseDown(self, evt):
        self.drop = False
        self.CaptureMouse()
        self.pos = evt.GetPosition()
        print "TRACE: mouse down, position is ", self.pos


    def MouseUp(self, evt):
        if self.HasCapture():
            self.drop = True
            self.pos = evt.GetPosition()
            print "TRACE: mouse up, position is ", self.pos
            self.ReleaseMouse()
            self.pos = self.selected = None
            self.Refresh()

    def Motion(self, evt):
        w,h = self.GetSize()
        if self.HasCapture():
            (xPos, yPos) = evt.GetPosition()
            print "TRACE: moving mouse ", (xPos, yPos)

            # index zero is xPos, index 1 is yPos
            #xPos = self.pos[0]
            #yPos = self.pos[1]

            # if yDiff is negative, we are moving down.  If yDiff is positive, we are going up.
            yDiff = yPos - self.pos[1]

            directionString = "NOWHERE"

            if yDiff < 0:
                directionString = "UP"
            elif yDiff > 0:
                directionString = "DOWN"

            print "TRACE: we are going ", directionString

            self.curRotateFactor += (-yDiff * 2 * math.pi) / 300

            self.pos = evt.GetPosition()
            if self.pos[0] < 0:
                self.pos[0] = 0
            elif self.pos[0] > w:
                self.pos[0] = w
            if self.pos[1] < 0:
                self.pos[1] = 0
            elif self.pos[1] > h:
                self.pos[1] = h
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
