from tkinter import *
import threading
from UI import UIsharedFunctions

class btConfigMode(UIsharedFunctions.sharedFunctions):
    def __init__(self, master, BullsEye, **kwargs):
        self.master = master
        self.BullsEye = BullsEye
        if 'terminal' in kwargs:
            self.mainTerminal = kwargs['terminal']
        self.BullsEye.angleStreamActive = False
        self.BullsEye.vidStreamActive = False
        self.BullsEye.btStreamActive = False
        self.UI()

    def UI(self):
        self.frame = Frame(self.master)
        self.addressList_frame = LabelFrame(self.frame, border=3, relief='ridge', width=430, height=200, text='BT Address Log')
        self.addressList_frame.grid_propagate(0)
        addDevice_frame = LabelFrame(self.frame, border=3, relief='ridge', width=1020, height=390, text='Add Device')
        addDevice_frame.grid_propagate(0)
        display_frame = Frame(addDevice_frame)
        kb_frame = Frame(addDevice_frame)
        btTesting_frame = LabelFrame(self.frame, text='BT Testing', border=3, relief='ridge', height=200, width=500)
        btTesting_frame.grid_propagate(0)
        btTestingButtons_frame = Frame(btTesting_frame)
    
        self.loadAddressListFrame()
    
        self.display_entry = Entry(display_frame, width=20, font='Arial 23 bold')
        self.display_entry.pack(side=LEFT, padx=(2, 10))
    
        self.letterMap = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
        for i in range(0, 10):
            Button(kb_frame, text=i, height=3, width=6, font='Arial 14 bold', command=lambda f=self.display_entry, c=i: self.keyBoardInput(f, c, limit=12)).grid(row=0, column=i, pady=2, padx=5)
            i = i + 1
        for i in range(0, 10):
            letter = self.letterMap[i]
            Button(kb_frame, text=letter, height=3, width=6, font='Arial 14 bold', command=lambda f=self.display_entry, c=self.letterMap[i]: self.keyBoardInput(f, c, limit=12)).grid(row=1, column=i, pady=2, padx=5)
            i = i + 1
        for i in range(10, 20):
            letter = self.letterMap[i]
            Button(kb_frame, text=letter, height=3, width=6, font='Arial 14 bold', command=lambda f=self.display_entry, c=self.letterMap[i]: self.keyBoardInput(f, c, limit=12)).grid(row=2, column=i - 10, pady=2, padx=5)
            i = i + 1
        for i in range(20, 26):
            letter = self.letterMap[i]
            Button(kb_frame, text=letter, height=3, width=6, font='Arial 14 bold', command=lambda f=self.display_entry, c=self.letterMap[i]: self.keyBoardInput(f, c, limit=12)).grid(row=3, column=i - 20, pady=2, padx=5)
            i = i + 1
        add_button = Button(kb_frame, text='ADD', width=16, height=3, font='Arial 13 bold', command=self.enterNewBtAddress)
        add_button.grid(row=3, column=6, columnspan=2)
        clear_button = Button(kb_frame, text='CLR', width=16, height=3, font='Arial 13 bold', command=lambda f=self.display_entry, c='!': self.keyBoardInput(f, c))
        clear_button.grid(row=3, column=8, columnspan=2)

        connectDefault_button = Button(btTestingButtons_frame, text='Connect\nDefault', width=8, height=3, font='Arial 13 bold', command=self.connectDefault)
        disconnect_button = Button(btTestingButtons_frame, text='Disconnect\nDevice', width=8, height=3, font='Arial 13 bold', command=self.disconnectDevice)
        streamStart_button = Button(btTestingButtons_frame, text='Stream\nStart', width=8, height=3, font='Arial 13 bold', command=self.btConfigStreamStart)
        streamEnd_button = Button(btTestingButtons_frame, text='Stream\nEnd', width=8, height=3, font='Arial 13 bold', command=self.btConfigStreamEnd)
    
        heading_label = Label(btTesting_frame, text='Heading', width=10, height=1, font='Arial 13 bold')
        self.heading_entry = Entry(btTesting_frame, width=10, font='Arial 13 bold')
        pitch_label = Label(btTesting_frame, text='Pitch', width=10, height=1, font='Arial 13 bold')
        self.pitch_entry = Entry(btTesting_frame, width=10, font='Arial 13 bold')
        roll_label = Label(btTesting_frame, text='Roll', width=10, height=1, font='Arial 13 bold')
        self.roll_entry = Entry(btTesting_frame, width=10, font='Arial 13 bold')
        yaw_label = Label(btTesting_frame, text='Yaw', width=10, height=1, font='Arial 13 bold')
        self.yaw_entry = Entry(btTesting_frame, width=10, font='Arial 13 bold')

        heading_label.grid(row=0, column=0)
        self.heading_entry.grid(row=1, column=0)
        pitch_label.grid(row=0, column=1)
        self.pitch_entry.grid(row=1, column=1)
        roll_label.grid(row=0, column=2)
        self.roll_entry.grid(row=1, column=2)
        yaw_label.grid(row=0, column=3)
        self.yaw_entry.grid(row=1, column=3)

        connectDefault_button.grid(row=0, column=0, padx=5)
        disconnect_button.grid(row=0, column=1, padx=5)
        streamStart_button.grid(row=0, column=2, padx=5)
        streamEnd_button.grid(row=0, column=3, padx=5)

        exit_button = Button(self.frame, text='Exit', width=2, height=7, font='Arial 16 bold', command=lambda m=self.master: self.exitMenu(m))
        
        self.addressList_frame.grid(row=1, column=0)
        addDevice_frame.grid(row=0, column=0, columnspan=3)
        display_frame.grid(row=0, column=0, sticky='')
        kb_frame.grid(row=1, column=0, sticky='', padx=(20, 0))
        btTesting_frame.grid(row=1, column=1)
        btTestingButtons_frame.grid(row=2, column=0, columnspan=4, padx=1, pady=5)
        exit_button.grid(row=1, column=2, pady=(10, 0))
        self.frame.grid(row=0, column=0)
    
    def loadAddressListFrame(self):
        # Large Frame > Canvas > Subframe .... Use subframe to create Window in canvas
        # This is the only way to allow scrolling inside a canvas
        addressList_canvas = Canvas(self.addressList_frame, height=170, width=350)
        addressListSub_frame = Frame(addressList_canvas)
        addressList_canvas.create_window(0, 0, window=addressListSub_frame, anchor='nw')
        scrollUp_button = Button(self.addressList_frame, text='▲\n▲', height=2, width=1)
        scrollDwn_button = Button(self.addressList_frame, text='▼\n▼', height=2, width=1)

        # Populate Address log
        if len(self.BullsEye.btAddressList) > 0:
            text = "Default: " + str(self.BullsEye.btAddressList[self.BullsEye.defaultIndex])
        else:
            text = "No Saved Addressess"
        self.defaultAddress_label = Label(addressListSub_frame, text=text, width=33, height=1, font='Arial 13 bold', bg='white')
        self.defaultAddress_label.grid(row=0, column=0, columnspan=3, padx=10, sticky='W')
    
        for i in range(len(self.BullsEye.btAddressList)):
            address = self.BullsEye.btAddressList[i]
            Label(addressListSub_frame, text=address, width=20, height=1, font='Arial 13 bold', bg='white').grid(row=i + 1, column=0, padx=2, pady=5, sticky='w')
            Button(addressListSub_frame, text="Set", width=4, height=1, font='Arial 13 bold', command=lambda i=i: self.setDefaultAddress(i)).grid(row=i + 1, column=1, padx=2, pady=5)
            Button(addressListSub_frame, text="DEL", width=4, height=1, font='Arial 13 bold', command=lambda i=i: self.deleteAddress(i)).grid(row=i + 1, column=2, padx=2, pady=5)
            i = i + 1
            
        self.frame.update()
        scrollUp_button.grid(row=0, column=1, padx=(20, 5))
        scrollDwn_button.grid(row=1, column=1, padx=(20, 5))
        addressList_canvas.configure(scrollregion=addressList_canvas.bbox('all'))
        scrollUp_button.config(command=lambda: addressList_canvas.yview_scroll(-2, 'units'))
        scrollDwn_button.config(command=lambda: addressList_canvas.yview_scroll(2, 'units'))
        addressList_canvas.grid(row=0, column=0, rowspan=2)
        
    def refreshAddressListFrame(self):
        childList = self.addressList_frame.winfo_children()
        for child in childList:
            child.destroy()
        self.loadAddressListFrame()
        
    def enterNewBtAddress(self):
        address = self.display_entry.get()
        if len(address) <12 or ':' in address:
            return
        b1 = address[0:2]
        b2 = address[2:4]
        b3 = address[4:6]
        b4 = address[6:8]
        b5 = address[8:10]
        b6 = address[10:12]
        address = b1+':'+b2+':'+b3+':'+b4+':'+b5+':'+b6
        self.display_entry.delete(0, END)
        self.display_entry.insert(END, address)
        self.BullsEye.btAddressList.append(address)
        self.BullsEye.updateBtAddressFile()
        self.refreshAddressListFrame()
    
    def deleteAddress(self, index):
        if index < self.BullsEye.defaultIndex:
            self.BullsEye.defaultIndex=self.BullsEye.defaultIndex-1
        elif index == self.BullsEye.defaultIndex and self.BullsEye.defaultIndex != 0:
            self.BullsEye.defaultIndex=0
        elif index == self.BullsEye.defaultIndex and self.BullsEye.defaultIndex == 0:
            self.BullsEye.defaultIndex=-1
        self.BullsEye.btAddressList.pop(index)
        self.BullsEye.updateBtAddressFile()
        self.refreshAddressListFrame()
    
    def setDefaultAddress(self, index):
        self.BullsEye.defaultIndex = index
        self.BullsEye.updateBtAddressFile()
        self.refreshAddressListFrame()
        
    def connectDefault(self):
        self.BullsEye.btStreamActive = False
        if self.BullsEye.mbtModule != None:
            if self.BullsEye.btAddressDefault == self.BullsEye.mbtModule.address:
                self.msg('Already Connected to address...')
                return
            self.BullsEye.mbtModule.sensorFusionStop()
            self.BullsEye.mbtModule.disconnectDevice()
            self.BullsEye.mbtModule = None
        
        state=self.BullsEye.connectBT(self.BullsEye.btAddressDefault)
        if state==0:
            txt = 'Connection Failed'
            currDevMsg = 'Connected to ' + str(self.BullsEye.mbtModule)
            self.msg(txt + '\n' + currDevMsg)
        elif state==1:
            txt = 'Connection Successful!'
            currDevMsg = 'Connected to ' + str(self.BullsEye.mbtModule)
            self.msg(txt + '\n' + currDevMsg)

    def disconnectDevice(self):
        self.BullsEye.mbtModule.sensorFusionStop()
        self.BullsEye.mbtModule.disconnectDevice()
        self.BullsEye.mbtModule = None
        self.msg("Device disconnected...")
        
    def btConfigStreamStart(self):
        if self.BullsEye.mbtModule == None:
            self.msg("No device connected")
            return
        
        if self.BullsEye.btStreamActive == True:
            return
        
        self.BullsEye.btStreamActive = True
        self.BullsEye.mbtModule.sensorFusionStart()
        btStreamThread = threading.Thread(target=self.btConfigStream)
        btStreamThread.start()
        self.master.update_idletasks()
        return
    
    def btConfigStream(self):
        c=0
        while self.BullsEye.btStreamActive == True:
            if c > 40:
                head, pitch, roll, yaw = self.BullsEye.mbtModule.dataReturn()
                print(head)
                self.heading_entry.delete(0, END)
                self.pitch_entry.delete(0, END)
                self.roll_entry.delete(0, END)
                self.yaw_entry.delete(0, END)
                self.heading_entry.insert(END, round(head, 2))
                self.pitch_entry.insert(END, round(pitch, 2))
                self.roll_entry.insert(END, round(roll, 2))
                self.yaw_entry.insert(END, round(yaw, 2))
                c=0
            c = c + 1
            self.master.update_idletasks()
            
    def btConfigStreamEnd(self):
        self.BullsEye.btStreamActive = False
        
    def exitMenu(self, master):
        self.BullsEye.btStreamActive = False
        self.BullsEye.angleStreamActive = False
        self.BullsEye.vidStreamActive = False
        master.destroy()
        if hasattr(self, 'mainTerminal'):
            if self.BullsEye.mbtModule != None:
                self.mainTerminal.insert(END, "Currently connected to %s \n"%(self.BullsEye.mbtModule.address))
                self.mainTerminal.see(END)
            else:
                self.mainTerminal.insert(END, "No Device Connected\n")
                self.mainTerminal.see(END)
        
        