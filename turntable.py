import wx
from random import randint
import math

class Node:
    def __init__(self, x, y):
        self.pos = (x, y)
        
    def setPos(self, pt):
        self.pos = pt
    
    def getPos(self):
        return self.pos
        
    def contains(self, pt):
        area = wx.Rect(self.pos[0]-6, self.pos[1]-6, 13, 13)
        if area.Contains(pt):
            return True
        else:
            return False
    
class Turntable(wx.Panel):
    def __init__(self, parent, pos, size, length=0, callback=None):
        wx.Panel.__init__(self, parent=parent, pos=pos, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.pos = None
        self.selected = None
#        self.nodes = [Node(randint(20,380), randint(20,380)) for i in range(length)]
        self.callback = callback

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_MOTION, self.Motion)
        
        # HACK!
#        for i in range(length):
#            self.pos = self.nodes[i].getPos()
#            self.selected = i
#            self.OnPaint(None)
#        self.pos = self.selected = None

    def OnPaint(self, evt):
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

        #draw the blue radius guide lines
        dc.SetPen(wx.Pen("#00FFFF"))
        for i in range(0,12):
            rads = i * ((2 * math.pi) / 12)
            startXLinePos = math.cos(rads) * (labelW/2) + middleXPos
            startYLinePos = math.sin(rads) * (labelW/2) + middleYPos
            endXLinePos = math.cos(rads) * (w/2) + middleXPos
            endYLinePos = math.sin(rads) * (w/2) + middleYPos
            if (i != 11):
                dc.DrawLine(startXLinePos, startYLinePos, endXLinePos, endYLinePos)
            else:
                dc.SetPen(wx.Pen("#FF0000", 3))
                dc.DrawLine(startXLinePos, startYLinePos, endXLinePos, endYLinePos)
                dc.SetPen(wx.Pen("#00FFFF", 1))

        dc.SetPen(wx.Pen("#000000", 1))

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

#        dc.SetPen(wx.Pen("#666666"))
#        dc.SetTextForeground("#AAAAAA")
#        for i in range(0, w, 50):
#            dc.DrawLine(i, 0, i, h)
#            dc.DrawText("%.2f" % (i/float(w)), i+2, h-12)
#            #tw, th = dc.GetTextExtent("%.2f" % (i/float(w)))
#        for i in range(0, h, 50):
#            dc.DrawLine(0, i, w, i)
#            dc.DrawText("%.2f" % (1-i/float(h)), 2, i+2)
#
#        if self.pos != None:
#            dc.SetPen(wx.Pen("#AAAAAA"))
#            x = self.pos[0] / float(w)
#            y = 1 - self.pos[1] / float(h)
#            dc.DrawText("%.3f, %.3f" % (x, y), w-80, 5)
#
#            if self.selected != None:
#                self.nodes[self.selected].setPos(self.pos)
#                if self.callback != None:
#                    self.callback(x, y, self.selected)
#                dc.DrawLine(0, self.pos[1], w, self.pos[1])
#                dc.DrawLine(self.pos[0], 0, self.pos[0], h)
#            
#        dc.SetPen(wx.Pen("#FFFFFF", width=1))
#        dc.SetBrush(wx.Brush("#FF0000"))
#        for node in self.nodes:
#            dc.DrawCirclePoint(node.getPos(), radius=5)

    def MouseDown(self, evt):
        self.CaptureMouse()
        self.pos = evt.GetPosition()
        print "TRACE: mouse down, position is ", self.pos


#        for i, node in enumerate(self.nodes):
#            if node.contains(self.pos):
#                self.selected = i
#                break
#        self.Refresh()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.pos = evt.GetPosition()
            print "TRACE: mouse up, position is ", self.pos
            self.ReleaseMouse()
            self.pos = self.selected = None
            self.Refresh()

    def Motion(self, evt):
        w,h = self.GetSize()
        if self.HasCapture():
            self.pos = evt.GetPosition()
            print "TRACE: moving mouse ", self.pos
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
    app.MainLoop()#!/usr/bin/python
