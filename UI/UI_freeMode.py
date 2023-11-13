from tkinter import *
from UI import UIsharedFunctions

class freeMode(UIsharedFunctions.sharedFunctions):
    def __init__(self, master, BullsEye):
        self.master = master
        self.BullsEye = BullsEye
        self.dex = IntVar()
        self.dex.set(0)
        self.UI()
        self.targetLoft_entry.insert(END, self.BullsEye.targetLoft)
        self.targetLie_entry.insert(END, self.BullsEye.targetLie)

    def UI(self):
        self.frame = Frame(self.master)

        # Frames
        canvas_frame = Frame(self.frame, width=500, height=300, bg='white')
        # Original camera size: W, H: 640, 480
        canvas_frame.grid_propagate(0)
        streamCMD_frame = LabelFrame(self.frame, text="Cam Ctrl.", border=3, relief='ridge')
        brightness_frame = Frame(streamCMD_frame, border=5)
        motorControl_frame = LabelFrame(self.frame, text="Servo Controller", border=3, relief='ridge')
        motorControlKeyboard_frame = Frame(motorControl_frame)
        motorControlManual_frame = Frame(motorControl_frame, height=75, width=400)
        lieLoft_frame = LabelFrame(self.frame, text="Protractor", width=500, height=95, bd=1, relief='ridge')
        lieLoft_frame.grid_propagate(0)
        frameAngle_frame = LabelFrame(self.frame, text="Frame", width=500, height=80, bd=1, relief='ridge')
        frameAngle_frame.grid_propagate(0)
        btmRight_frame = Frame(self.frame)
        btdata_frame = LabelFrame(btmRight_frame, text="Bt bit", width=495, height=200, bd=1, relief='ridge')
        btdata_frame.grid_propagate(0)
        btdataButtons_frame = Frame(btdata_frame)
        lhOption_frame = Frame(btdata_frame, relief='ridge')

        # Image Canvas
        canvas = Label(canvas_frame, bg='white')
        canvas.grid(row=0, column=0)

        toolTip_canvas = Canvas(self.frame, height=300, width=150, bg='black')
        canvas_label = Label(toolTip_canvas, text='Idle', width=17, font='Arial 8 bold', bg='black', fg='white', anchor='w')
        toolTipScore_label = Label(toolTip_canvas, text="Average Scoreline", width=17, font='Arial 8 bold', bg='Black', fg='Red', anchor='w')
        toolTipZero_label = Label(toolTip_canvas, text="Zero Line", width=17, font='Arial 8 bold', bg='Black', fg='Yellow', anchor='w')
        toolTip_canvas.grid(row=0, column=0, pady=0, sticky=NW)
        canvas_label.grid(row=0, column=0, padx=5, pady=5, sticky=NW)
        toolTipScore_label.grid(row=1, column=0, pady=0, sticky=NW)
        toolTipZero_label.grid(row=2, column=0, pady=0, sticky=NW)

        # Stream control buttons
        button_streamStart = Button(streamCMD_frame, width=5, height=2, text="Stream", font='Arial 13 bold', command=lambda : self.vidStreamStart(canvas,offset=lieOffset_entry, box=False))
        button_showRaw = Button(streamCMD_frame, width=5, height=2, text="Raw", font='Arial 13 bold', command=lambda cv=canvas: self.showRaw(cv))
        button_showScore = Button(streamCMD_frame, width=5, height=2, text="Score", font='Arial 13 bold', command=lambda cv=canvas: self.showScore(cv))
        button_capture = Button(streamCMD_frame, width=5, height=2, text="Screen \n Cap", font='Arial 13 bold')
        button_capture.config(command=lambda : self.captureImg(canvas, offset=lieOffset_entry))
        button_streamStart.grid(row=0, column=0, padx=1, pady=2, sticky='')
        button_showRaw.grid(row=1, column=0, padx=1, pady=2, sticky='')
        button_showScore.grid(row=2, column=0, padx=1, pady=2, sticky='')
        button_capture.grid(row=3, column=0, padx=1, pady=2, sticky='')

        # Brightness Controller
        brightDwn_button = Button(brightness_frame, width=1, height=1, text="-", font='Arial 13 bold',
                                  command=lambda: self.brightnessAdjust('-'))
        brightUp_button = Button(brightness_frame, width=1, height=1, text="+", font='Arial 13 bold',
                                 command=lambda: self.brightnessAdjust('+'))
        brightDwn_button.grid(row=1, column=0)
        brightUp_button.grid(row=1, column=1)

        # Frame for frameAngle Data
        frameAngle_label = Label(frameAngle_frame, width=8, text='Frame', font='Arial 14 bold', bg='black', fg='white')
        lieOffset_label = Label(frameAngle_frame, width=8, text='Offset', font='Arial 14 bold', bg='black', fg='white')
        frameAngle_entry = Entry(frameAngle_frame, width=8, font='Arial 14 bold')
        lieOffset_entry = Entry(frameAngle_frame, width=8, font='Arial 14 bold')

        frameAngle_label.grid(row=0, column=0, padx=5, pady=0)
        frameAngle_entry.grid(row=0, column=1, padx=5, pady=0)
        lieOffset_label.grid(row=0, column=2, padx=5, pady=0)
        lieOffset_entry.grid(row=0, column=3, padx=5, pady=0)

        # Motor Controller
        seekAngle_entry = Entry(motorControlKeyboard_frame, width=5, font='Arial 32 bold', state='disabled')
        numpad0_button = Button(motorControlKeyboard_frame, text="0", height=2, width=14, font='Arial 12 bold', state='disabled')
        numpadDot_button = Button(motorControlKeyboard_frame, text=".", height=2, width=5, font='Arial 12 bold', state='disabled')
        numpadClear_button = Button(motorControlKeyboard_frame, text="CLEAR", height=2, width=9, font='Arial 12 bold', state='disabled')
        numpadSeek_button = Button(motorControlKeyboard_frame, text="SEEK", height=4, width=9, font='Arial 12 bold', state='disabled')

        i = 0  # Auto Generate numpad 1 to 9
        for r in range(3):
            for c in range(3):
                i = i + 1
                btn=Button(motorControlKeyboard_frame, text=i, height=2, width=4, font='Arial 12 bold', state='disabled')
                btn.config(command=lambda f=seekAngle_entry, c=i: self.keyBoardInput(f, c, limit=4))
                btn.grid(row=r, column=c, padx=0, pady=0)

        numpad0_button.config(command = lambda f=seekAngle_entry, c='0': self.keyBoardInput(f, c, limit=4))
        numpadDot_button.config(command = lambda f=seekAngle_entry, c='.': self.keyBoardInput(f, c, limit=4))
        numpadClear_button.config(command = lambda f=seekAngle_entry, c='!': self.keyBoardInput(f, c, limit=4))
        numpadSeek_button.config(command = lambda v=seekAngle_entry, f=frameAngle_entry: self.seekAngleValue(v, f, isEntry=True))

        seekAngle_entry.grid(row=0, column=3, padx=5, pady=5)
        numpadClear_button.grid(row=1, column=3, padx=5, pady=5)
        numpadSeek_button.grid(row=2, column=3, rowspan=2, padx=5, pady=5)
        numpad0_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        numpadDot_button.grid(row=3, column=2, padx=5, pady=5)
        motorControlKeyboard_frame.grid(row=0, column=0)

        manualMotor_label = Label(motorControlManual_frame, text="Step", height=2, width=8, font='Arial 13 bold', bg='black', fg='white')
        frameDwn_button = Button(motorControlManual_frame, text="--", height=2, width=2, font='Arial 12 bold', state='disabled')
        frameUp_button = Button(motorControlManual_frame, text="+", height=2, width=2, font='Arial 12 bold', state='disabled')
        hodl_button = Button(motorControlManual_frame, text="H.Off", height=2, width=4, font='Arial 12 bold', state='disabled')
        servoEnable_button = Button(motorControlManual_frame, text="Enable", height=2, width=6, font='Arial 12 bold')

        manualMotor_label.grid(row=0, column=0, padx=2, pady=1, sticky='')
        frameDwn_button.grid(row=0, column=1, padx=2, pady=1, sticky='')
        frameUp_button.grid(row=0, column=2, padx=2, pady=1, sticky='')
        hodl_button.grid(row=0, column=3, padx=2, pady=1, sticky='', rowspan=2)
        servoEnable_button.grid(row=0, column=4, padx=2, pady=1, sticky='')

        # Loft/Lie Data
        apiLoft_label = Label(lieLoft_frame, width=14, text='Loft Protractor', font='Arial 14 bold', bg='black', fg='white')
        apiLie_label = Label(lieLoft_frame, width=14, text='Lie Protractor', font='Arial 14 bold', bg='black', fg='white')
        apiLoft_entry = Entry(lieLoft_frame, width=10, font='Arial 14 bold')
        apiLie_entry = Entry(lieLoft_frame, width=10, font='Arial 14 bold')
        angleStreamStart_button = Button(lieLoft_frame, text="Stream\nStart", font='Arial 14 bold', padx=1, width=7, height=2)
        captureAngle_button = Button(lieLoft_frame, text="Cap", font='Arial 13 bold', padx=1, width=5, height=2)
        setMCREF_button = Button(lieLoft_frame, text="MC\nREF", font='Arial 13 bold', padx=1, width=5, height=2,
                                 command=lambda li = apiLie_entry, lo=apiLoft_entry, fr=frameAngle_entry: self.setMCREF(li, lo, fr))
        apiLoft_label.grid(row=0, column=0, padx=5, pady=5, sticky='')
        apiLie_label.grid(row=1, column=0, padx=5, pady=5, sticky='')
        apiLoft_entry.grid(row=0, column=1, padx=5, pady=5, sticky='')
        apiLie_entry.grid(row=1, column=1, padx=5, pady=5, sticky='')
        captureAngle_button.grid(row=0, column=3, padx=3, rowspan=2, sticky='')
        angleStreamStart_button.grid(row=0, column=4, padx=3, rowspan=2, sticky='')
        setMCREF_button.grid(row=0, column=5, padx=3, rowspan=2, sticky='')

        # Exit Button
        exitApp_button = Button(self.frame, height=1, width=35, text="Main Menu", font='Arial 18 bold', padx=1, command=lambda m=self.master: self.exitMenu(m))

        # Frame for BT Data
        rh_button = Radiobutton(lhOption_frame, text='RH', width=5, variable=self.dex, value=0, indicator=0)
        lh_button = Radiobutton(lhOption_frame, text='LH', width=5, variable=self.dex, value=1, indicator=0)

        loft_label = Label(btdata_frame, width=12, text='Loft', font='Arial 14 bold', bg='black', fg='white')
        lie_label = Label(btdata_frame, width=12, text='Lie', font='Arial 14 bold', bg='black', fg='white')
        measured_label = Label(btdata_frame, width=10, text='Actual', font='Arial 14 bold', bg='black', fg='white')
        target_label = Label(btdata_frame, width=10, text='Target', font='Arial 14 bold', bg='black', fg='white')
        diff_label = Label(btdata_frame, width=10, text='Diff', font='Arial 14 bold', bg='black', fg='white')
        btHeading_label = Label(btdata_frame, width=12, text='Heading', font='Arial 14 bold', bg='black', fg='white')

        btLoft_entry = Entry(btdata_frame, width=10, font='Arial 14 bold')
        btLie_entry = Entry(btdata_frame, width=10, font='Arial 14 bold')
        self.targetLoft_entry = Entry(btdata_frame, width=10, font='Arial 14 bold')
        self.targetLie_entry = Entry(btdata_frame, width=10, font='Arial 14 bold')
        diffLoft_entry = Entry(btdata_frame, width=10, font='Arial 14 bold')
        diffLie_entry = Entry(btdata_frame, width=10, font='Arial 14 bold')
        btHeading_entry = Entry(btdata_frame, width=10, font='Arial 14 bold')

        btStreamStart_button = Button(btdataButtons_frame, height=2, width=8, text="Stream\nStart", font='Arial 12 bold', padx=1)
        btTareValueZero_button = Button(btdataButtons_frame, height=2, width=8, text="Tare\nZero", font='Arial 12 bold', padx=1, command=self.btTareToZero)
        btTareValueLieLoft_button = Button(btdataButtons_frame, height=2, width=8, text="Tare\nLie Loft", font='Arial 12 bold', padx=1, command=self.btTareToProtractor)
        btMenu_button = Button(btdataButtons_frame, height=2, width=8, text="Set\nTarget", font='Arial 12 bold', padx=1, command=self.btTargetMenu)

        BTmainEntry = (btLoft_entry, btLie_entry, btHeading_entry)
        BTdiffEntry = (diffLoft_entry, diffLie_entry)
        btStreamStart_button.config(command=lambda: self.btStreamStart(BTmainEntry,
            diffEntry = BTdiffEntry, toggle=btStreamStart_button, frameEntry=frameAngle_entry))
        angleStreamStart_button.config(command=lambda li = apiLie_entry, lo=apiLoft_entry, fr=frameAngle_entry:
            self.angleStreamStart(li, lo, fr, btStreamButton=btStreamStart_button))
        captureAngle_button.config(command=lambda li = apiLie_entry, lo=apiLoft_entry, fr=frameAngle_entry:
            self.captureAngle(li, lo, fr, btStreamButton=btStreamStart_button))
        lhOption_frame.grid(row=0, column=0, padx=3, pady=2)
        rh_button.grid(row=0, column=0, padx=3, pady=2)
        lh_button.grid(row=0, column=1, padx=3, pady=2)
        measured_label.grid(row=0, column=1, padx=6, pady=2, sticky=NW)
        target_label.grid(row=0, column=2, padx=6, pady=2, sticky=NW)
        diff_label.grid(row=0, column=3, padx=6, pady=2, sticky=NW)
        loft_label.grid(row=1, column=0, padx=6, pady=2, sticky=NW)
        lie_label.grid(row=2, column=0, padx=6, pady=2, sticky=NW)
        btHeading_label.grid(row=3, column=0, padx=6, pady=2, sticky=NW)

        btLoft_entry.grid(row=1, column=1, padx=6, pady=2, sticky=NW)
        btLie_entry.grid(row=2, column=1, padx=6, pady=2, sticky=NW)
        self.targetLoft_entry.grid(row=1, column=2, padx=6, pady=2, sticky=NW)
        self.targetLie_entry.grid(row=2, column=2, padx=6, pady=2, sticky=NW)
        diffLoft_entry.grid(row=1, column=3, padx=6, pady=2, sticky=NW)
        diffLie_entry.grid(row=2, column=3, padx=6, pady=2, sticky=NW)
        btHeading_entry.grid(row=3, column=1, padx=6, pady=2, sticky=NW)

        btdataButtons_frame.grid(row=4, column=0, columnspan=4)
        btStreamStart_button.grid(row=4, column=0, padx=8, pady=1, sticky='')
        btTareValueZero_button.grid(row=4, column=2, padx=8, pady=1, sticky='')
        btTareValueLieLoft_button.grid(row=4, column=3, padx=8, pady=1, sticky='')
        btMenu_button.grid(row=4, column=4, padx=8, pady=1, sticky='')

        #Button Command Config
        frameDwn_button.config(command=lambda d='-', f=frameAngle_entry: self.motorRotate(d, f))
        frameUp_button.config(command=lambda d='+', f=frameAngle_entry: self.motorRotate(d, f))
        hodl_button.config(command=lambda b=hodl_button: self.toggleHoldOff(b))
        keyboardButtons = motorControlKeyboard_frame.winfo_children()
        servoRelatedButtons = (frameDwn_button, frameUp_button, hodl_button, *keyboardButtons)
        disableButtons = (captureAngle_button, angleStreamStart_button, setMCREF_button, btStreamStart_button,
                          btTareValueZero_button, btTareValueLieLoft_button)
        servoEnable_button.config(command=lambda b=servoEnable_button, c=servoRelatedButtons, d=disableButtons: self.enableMotorControls(b, c, d))

        # Main Menu Frame Insert
        # Top Half
        canvas_frame.grid(row=0, column=0, padx=5, pady=5, sticky=NW)
        streamCMD_frame.grid(row=0, column=1, padx=0, pady=5, sticky=NW)
        brightness_frame.grid(row=5, column=0, padx=2, pady=5, sticky=NW)
        motorControl_frame.grid(row=0, column=2, padx=2, pady=(5, 0), sticky=NW)
        motorControlManual_frame.grid(row=4, column=0, padx=2, pady=2, sticky=NW, columnspan=4)

        # Bottom left
        frameAngle_frame.grid(row=1, column=0, padx=5, pady=0, sticky='NW', columnspan=2)
        lieLoft_frame.grid(row=2, column=0, padx=5, pady=0, sticky='NW', columnspan=2)
        exitApp_button.grid(row=3, column=0, padx=5, pady=5, sticky='', columnspan=1)

        # Bottom Right
        btmRight_frame.grid(row=1, column=1, padx=5, pady=1, sticky=NW, columnspan=2, rowspan=3)
        btdata_frame.grid(row=0, column=1, padx=5, pady=1, sticky=NW)

        self.frame.grid(row=0, column=0)

        self.master.after(200, self.readFrame(frameAngle_entry))

    def btTargetMenu(self):
        self.btSetTargetMenu = Toplevel(width=380, height=490)
        self.btSetTargetMenu.grid_propagate(0)
        self.btSetTargetMenu.wm_title("Set Target Menu")
        self.btSetTargetMenu.attributes("-fullscreen", False)

        target_frame = Frame(self.btSetTargetMenu, bd=3, relief='ridge', height=90, width=360)
        target_frame.grid_propagate(0)
        setTargetKeyboard_frame = Frame(self.btSetTargetMenu, bd=3, relief='ridge', height=310, width=360)
        setTargetKeyboard_frame.grid_propagate(0)
        setTarget_frame = Frame(setTargetKeyboard_frame)

        ###Target Lie Loft
        targetLoft_label = Label(target_frame, width=12, text='Target Loft', font='Arial 14 bold', bg='black', fg='white')
        targetLie_label = Label(target_frame, width=12, text='Target Lie', font='Arial 14 bold', bg='black', fg='white')
        targetLoft_entry = Entry(target_frame, width=10, font='Arial 14 bold')
        targetLie_entry = Entry(target_frame, width=10, font='Arial 14 bold')

        targetLoft_label.grid(row=0, column=0, padx=5, pady=5)
        targetLoft_entry.grid(row=0, column=1, padx=5, pady=5)
        targetLie_label.grid(row=1, column=0, padx=5, pady=5)
        targetLie_entry.grid(row=1, column=1, padx=5, pady=5)

        target_entry = Entry(setTargetKeyboard_frame, width=10, font='Arial 32 bold')

        i = 0  # Auto Generate numpad 1 to 9
        for r in range(3):
            for c in range(3):
                i = i + 1
                b = Button(setTargetKeyboard_frame, text=i, height=2, width=4, font='Arial 12 bold')
                b.grid(row=(r + 1), column=c, padx=0, pady=0)
                b.config(command=lambda i=i: self.keyBoardInput(target_entry, i))

        numpad0_button = Button(setTargetKeyboard_frame, text="0", height=2, width=14, font='Arial 12 bold')
        numpadDot_button = Button(setTargetKeyboard_frame, text=".", height=2, width=4, font='Arial 12 bold')
        numpadClear_button = Button(setTargetKeyboard_frame, text="CLR", height=4, width=8, font='Arial 12 bold')
        setTargetLoft_button = Button(setTargetKeyboard_frame, text="Set Loft\nTarget", height=2, width=8, font='Arial 12 bold')
        setTargetLie_button = Button(setTargetKeyboard_frame, text="Set Lie\nTarget", height=2, width=8, font='Arial 12 bold')

        numpad0_button.config(command=lambda e=target_entry: self.keyBoardInput(e, '0'))
        numpadDot_button.config(command=lambda e=target_entry: self.keyBoardInput(e, '.'))
        numpadClear_button.config(command=lambda e=target_entry: self.keyBoardInput(e, '!'))
        setTargetLoft_button.config(command=lambda e=target_entry, lo=targetLoft_entry: self.setTargetLoft(e, lo))
        setTargetLie_button.config(command=lambda e=target_entry, li=targetLie_entry: self.setTargetLie(e, li))

        target_entry.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
        numpadClear_button.grid(row=3, column=3, padx=5, pady=5, rowspan=2)
        numpad0_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        numpadDot_button.grid(row=4, column=2, padx=5, pady=5)
        setTarget_frame.grid(row=5, column=0, columnspan=3)
        setTargetLoft_button.grid(row=1, column=3, padx=5, pady=5)
        setTargetLie_button.grid(row=2, column=3, padx=5, pady=5)

        exit_button = Button(self.btSetTargetMenu, text="Save & Exit", height=2, width=16, font='Arial 12 bold', command=self.exitBtTargetMenu)

        target_frame.grid(row=0, column=0, padx=5, pady=5, sticky=NW)
        setTargetKeyboard_frame.grid(row=1, column=0, padx=5, pady=5, sticky=NW)
        exit_button.grid(row=2, column=0, padx=5, pady=10, sticky='')

        targetLoft_entry.delete(0, END)
        targetLoft_entry.insert(END, self.BullsEye.targetLoft)
        targetLie_entry.delete(0, END)
        targetLie_entry.insert(END, self.BullsEye.targetLie)

    def setTargetLoft(self, entry, entryLoft):
        try:
            loft = round(float(entry.get()), 1)
        except:
            entry.delete(0, END)
            entry.insert(END, 'ERROR')
            return
        self.BullsEye.targetLoft = loft
        entry.delete(0, END)
        entryLoft.delete(0, END)
        entryLoft.insert(END, self.BullsEye.targetLoft)

    def setTargetLie(self, entry, entryLie):
        try:
            lie = round(float(entry.get()), 1)
        except:
            entry.delete(0, END)
            entry.insert(END, 'ERROR')
            return
        self.BullsEye.targetLie = lie
        entry.delete(0, END)
        entryLie.delete(0, END)
        entryLie.insert(END, self.BullsEye.targetLie)

    def exitBtTargetMenu(self):
        self.btSetTargetMenu.destroy()
        self.targetLie_entry.delete(0, END)
        self.targetLie_entry.insert(END, self.BullsEye.targetLie)
        self.targetLoft_entry.delete(0, END)
        self.targetLoft_entry.insert(END, self.BullsEye.targetLoft)