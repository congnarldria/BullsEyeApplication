#! /usr/bin/python3

from BullsEyeModules import BullsEyeObject as BE
from UI import UI_guidedMode
from UI import UI_freeMode
from UI import UI_calibrationMode
from UI import UI_btConfigMode
from tkinter import *

class ApplicationMainMenu(Frame):
    def __init__(self, BullsEye, master):
        super().__init__()
        self.BullsEye = BullsEye
        self.master = master
        self.fullscreen = True
        self.BullsEye.updateBtAddressFromFile()
        self.BullsEye.updateScoreFilterFromFile()
        self.BullsEye.updateModelDataFromCSV()
        self.BullsEye.initiateIO()
        self.BullsEye.loadIconImages()
        self.launchMainMenu()
        self.master.after(3000, lambda: self.loadingTime(self.workOrderMode_button, self.freeMode_button, self.calibrationMode_button, self.btMenu_button, self.exit_button))

    def launchMainMenu(self):
        self.master.title("Bull's Eye Gauge Application Main Menu")
        self.master.grid_propagate(0)
        self.master.configure(height=600, width=1024)
        self.master.attributes("-fullscreen", self.fullscreen)
        title_frame = Frame(self.master, width=1024, height=100, border=3)
        title_frame.grid_propagate(0)
        left_frame = Frame(self.master, width=312, height=490, border=3)
        left_frame.grid_propagate(0)
        right_frame = Frame(self.master, width=312, height=490, border=3)
        right_frame.grid_propagate(0)
        center_frame = Frame(self.master, width=400, height=490, border=3)
        center_frame.grid_propagate(0)
        terminal_frame = Frame(center_frame, border=3, relief='ridge')
        terminal_frame.grid_propagate(0)

        title_frame.grid(row=0, column=0, columnspan=3, pady=(20,0), sticky='W')
        left_frame.grid(row=1, column=0)
        center_frame.grid(row=1, column=1)
        right_frame.grid(row=1, column=2)

        title_label = Label(title_frame, text="Bull's Eye Application\nMachine Assisted Bending Solution", font='Arial 30 bold')
        self.exit_button = Button(right_frame, text='Exit', width=8, height=3, font='Arial 15 bold', command=self.exitApp)
        version_label = Label(right_frame, text='Version 4.8.2', font='Arial 12 bold')
        self.workOrderMode_button = Button(center_frame, text='Order Mode', width=11, height=3, font='Arial 19 bold', command=self.launchGuidedMode)
        self.freeMode_button = Button(center_frame, text='Free Mode', width=11, height=3, font='Arial 19 bold', command=self.launchFreeMode)
        self.calibrationMode_button = Button(center_frame, text='Calibration', width=11, height=3, font='Arial 19 bold', command=self.launchCalibrationMode)
        self.btMenu_button = Button(center_frame, text='BT menu', width=11, height=3, font='Arial 19 bold', command=self.launchBtConfigMode)

        title_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        version_label.place(relx=0.60, rely=0.95, anchor='e')
        self.exit_button.place(relx=0.60, rely=0.80, anchor='e')

        self.workOrderMode_button.grid(row=0, column=0, pady=(40, 2), padx=5)
        self.freeMode_button.grid(row=0, column=1, pady=(40, 2), padx=5)
        self.calibrationMode_button.grid(row=1, column=0, pady=(10, 2), padx=5)
        self.btMenu_button.grid(row=1, column=1, pady=(10, 2), padx=5)
        terminal_frame.grid(row=3, column=0, pady=(35, 0), columnspan=2)

        self.mainMenu_terminal = Text(terminal_frame, width=53, height=8, font='Arial 10 bold')
        terminalScb = Scrollbar(terminal_frame, orient="vertical", command=self.mainMenu_terminal.yview)
        self.mainMenu_terminal.configure(yscrollcommand=terminalScb.set)
        self.mainMenu_terminal.pack(side="left")
        terminalScb.pack(side="right")
        self.updateTerminal()

        self.workOrderMode_button.configure(state='disabled')
        self.freeMode_button.configure(state='disabled')
        self.calibrationMode_button.configure(state='disabled')
        self.btMenu_button.configure(state='disabled')
        self.exit_button.configure(state='disabled')

    def loadingTime(self, *args):
        for i in args:
            i.configure(state='normal')

    def launchGuidedMode(self):
        self.guidedModeWindow = Toplevel()
        self.guidedModeWindow.configure(height=600, width=1024)
        self.guidedModeWindow.grid_propagate(0)
        self.guidedModeWindow.wm_title("Guided Mode")
        self.guidedModeWindow.attributes("-fullscreen", self.fullscreen)
        UI_guidedMode.guidedMode(self.guidedModeWindow, self.BullsEye)

    def launchFreeMode(self):
        self.freeModeWindow = Toplevel()
        self.freeModeWindow.config(height=600, width=1024)
        self.freeModeWindow.grid_propagate(0)
        self.freeModeWindow.wm_title("Free Mode")
        self.freeModeWindow.attributes("-fullscreen", self.fullscreen)
        UI_freeMode.freeMode(self.freeModeWindow, self.BullsEye)
        
    def launchCalibrationMode(self):
        self.calibrationModeWindow = Toplevel()
        self.calibrationModeWindow.configure(height=600, width=1024)
        self.calibrationModeWindow.grid_propagate(0)
        self.calibrationModeWindow.wm_title("Calibration Mode")
        self.calibrationModeWindow.attributes("-fullscreen", self.fullscreen)
        UI_calibrationMode.calibrationMode(self.calibrationModeWindow, self.BullsEye)

    def launchBtConfigMode(self):
        self.btConfigModeWindow = Toplevel()
        self.btConfigModeWindow.configure(height=600, width=1024)
        self.btConfigModeWindow.grid_propagate(0)
        self.btConfigModeWindow.wm_title("Calibration Mode")
        self.btConfigModeWindow.attributes("-fullscreen", self.fullscreen)
        UI_btConfigMode.btConfigMode(self.btConfigModeWindow, self.BullsEye, terminal = self.mainMenu_terminal)

    def updateTerminal(self):
        if self.BullsEye.btAddressList != []:
            str1 = "Bluetooth Address Log loaded, " + str(len(self.BullsEye.btAddressList)) + " in total \n"
            str2 = "Default Address: " + self.BullsEye.btAddressDefault + '\n'
            self.mainMenu_terminal.insert(END, str1)
            self.mainMenu_terminal.see(END)
            self.mainMenu_terminal.insert(END, str2)
            self.mainMenu_terminal.see(END)
        else:
            self.mainMenu_terminal.insert(END, 'BT Address log is empty...\n')
            self.mainMenu_terminal.see(END)
            self.mainMenu_terminal.insert(END, 'No default address loaded...\n')
            self.mainMenu_terminal.see(END)
        
        self.mainMenu_terminal.insert(END, "Score Filter Settings Updated from file\n")
        self.mainMenu_terminal.insert(END, "X: %s, Y: %s, W: %s, H: %s, T: %s, Z: %s, F: %s\n" %(
                                        self.BullsEye.scoreFilterSettings[0],
                                       self.BullsEye.scoreFilterSettings[1],
                                       self.BullsEye.scoreFilterSettings[2],
                                       self.BullsEye.scoreFilterSettings[3],
                                       self.BullsEye.scoreFilterSettings[4],
                                       self.BullsEye.scoreFilterSettings[5],
                                       self.BullsEye.scoreFilterSettings[6]))
        self.mainMenu_terminal.see(END)

        if self.BullsEye.modelList:
            txt = str(len(self.BullsEye.modelList)) + ' Models imported from CSV File...\n'
            self.mainMenu_terminal.insert(END, txt)
            self.mainMenu_terminal.see(END)
        else: self.mainMenu_terminal.insert(END, 'No model data imported...\n')

        if self.BullsEye.servoController == None:
            self.mainMenu_terminal.insert(END, "Failed to connect to Servo controller...\n")
            self.mainMenu_terminal.see(END)
        if self.BullsEye.mbtModule == None:
            self.mainMenu_terminal.insert(END, "Faield to connect to Mbient BT unit...\n")
            self.mainMenu_terminal.see(END)
        if self.BullsEye.myCamera == None:
            self.mainMenu_terminal.insert(END, "Faield to connect to Camera...\n")
            self.mainMenu_terminal.see(END)

    def exitApp(self):
        self.BullsEye.btStreamActive = False
        self.BullsEye.vidStreamActive = False
        self.BullsEye.angleStreamActive = False
        if self.BullsEye.mbtModule != None:
            self.BullsEye.mbtModule.sensorFusionStop()
            self.BullsEye.mbtModule.disconnectDevice()
        self.BullsEye.updateScoreSettingFile()
        self.master.destroy()

if __name__ == "__main__":
    BullsEyeApp = BE.BullsEye()
    root = Tk()
    app = ApplicationMainMenu(BullsEyeApp, root)
    root.mainloop()