import wx
import os
import binascii
import wx.richtext as rt
SB_INFO = 0
ID_SAVE=103
ID_SAVEAS=104
class AsciiFrame(wx.Frame):
    stockUndo = []
    stockRedo = []
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "MyHexEditor",
                size=(800,600))
        
        self.initStatusBar()
        self.createMenuBar()
        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        wx.CallAfter(self.rtc.SetFocus)
        self.count=5
        self.dirName = ""
        self.fileName = ""
        self.Refresh(True, self.rtc.GetRect())
      
    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])
    def menuData(self):
        return [("&File", (
                    ("&New", "New file", self.OnNew),
                    ("Re&fresh", "Open file", self.OnOpen),
                    ("&Save", "Save file", self.OnSave),
                    ("&Save As","Save file as", self.OnSaveAs),
                    ("", "", ""),
                    ("&Quit", "Quit", self.OnCloseWindow))),
                 ("&Edit", (
                     ("&Copy", "Copy the selection and put it on Clipboard ", self.OnCopy),
                    ("&Paste", "Insert Clipboard contents", self.OnPaste),
                    ("&Redo", "Redo the last action", self.OnRedo),
                    ("", "", ""),
                     ("&Undo","Undo the last action",self.OnUndo)))]
                
            
   

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler,
                       kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)

   
    def OnOpen(self, event):
       # wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=False)
        #dlg = wx.FileDialog(self, "Choose a filename",
                            #wildcard=wildcard,
         #                   style=wx.OPEN)
       # if dlg.ShowModal() == wx.ID_OK:
        #    path = dlg.GetPath()
         #   if path:
          #      fileType = types[dlg.GetFilterIndex()]
                myascii()
                self.rtc.LoadFile('ascii1.txt')
       # dlg.Destroy()
    def OnSave(self, event):
        if (self.fileName != "") and (self.dirName != ""):
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'w')
                f.write(self.rtc.GetValue())
                self.PushStatusText("Saved file: " + str(self.rtb.GetLastPosition()) +
                                    " characters.", SB_INFO)
                f.close()
                return True
            except:
                self.PushStatusText("Error in saving file.", SB_INFO)
                return False
        else:
            ### - If no name yet, then use the OnFileSaveAs to get name/directory
            return self.OnSaveAs(event)
    def OnSaveAs(self,event):
        ret = False
        dlg = wx.FileDialog(self, "Save As", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|All Files|*.*", wx.SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            ### - Use the OnFileSave to save the file
            if self.OnSave(event):
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                ret = True
        dlg.Destroy()
        return ret
    def OnCloseWindow(self, event):
        self.Destroy()
    def OnCopy(self, event): 
        widget = self.FindFocus()
        self.copied = widget.GetStringSelection()

    def OnPaste(self, event): 
        widget = self.FindFocus()
        widget.WriteText(self.copied)
    
    def OnUndo(self, event): 
         self.rtc.Undo()  
    
    def OnRedo(self,event):
         self.rtc.Redo()
    def OnNew(self,event):
          self.dlg1 = HexFrame(self)
          self.dlg1.Show(True)
    
        
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)
#number = ord(char)
def myascii():
    #file = open(filename, 'r')
    #hexfile=open('hex1.txt', 'w')
    asciifile=open('ascii1.txt', 'w')
    #while 1:
     #   char = file.read(1)          # read by character
      #  if not char: break
       # vil=toHex(char)
        #val=binascii.a2b_hex(char)
        #hexfile.write(vil)
    #st=toStr(val)
    #hexfile.close()
    hexfile=open('hex1.txt', 'r')
    while 1:
        chir=hexfile.read(2)
        if not chir: break
        val=binascii.a2b_hex(chir)
        asciifile.write(val)
    asciifile.close()
    hexfile.close()
   # file.close()




if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame =AsciiFrame(None)
    frame.Show(True)
    app.MainLoop()

