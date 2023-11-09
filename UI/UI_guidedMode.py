from tkinter import *
from UI import UIsharedFunctions

class guidedMode(UIsharedFunctions.sharedFunctions):
    def __init__(self, master, BullsEye):
        self.master = master
        self.BullsEye = BullsEye

        #BT Pod LH/RH Radio Button Variables
        self.dex = IntVar()

        #Target Lie/Loft Offset Variables
        self.tgtLieOffset = 0
        self.tgtLoftOffset = 0

        #lock offset variable
        self.lockOffsetStatus = False

        self.UI()
        self.updateCurrentClub(self.BullsEye.currentModel.clubs[self.BullsEye.currentClubIndex])
        self.updateOffSetValues('loft', 0)
        self.updateOffSetValues('lie', 0)
        self.frameAngle_entry.insert(END, self.BullsEye.frame)
    
    #Fullscreen Mode: Stream video of clubface to capture offset
    def fullscreen_menu(self):
        self.fullscreenUI = Toplevel()
        self.fullscreenUI.configure(height=600, width=1024)
        self.fullscreenUI.attributes("-fullscreen", True)
        self.fullscreenUI.grid_propagate(0)
        self.fullscreenUI.wm_title("Club Face Video Stream")
        
        canvas_frame = Frame(self.fullscreenUI, width=750, height=450, bg='white')
        canvas_frame.grid_propagate(0)
        canvas = Label(self.fullscreenUI, bg='white')
        
        rightside_frame = Frame(self. fullscreenUI, bd=1, relief='ridge')
        modelID_label = Label(rightside_frame, width=12, text="Model ID", bg="Black", fg='White', font='arial 16 bold')
        self.modelIDFullscreen_entry = Entry(rightside_frame, width=12, font='arial 16 bold')
        clubID_label = Label(rightside_frame, width=12, text="Club ID", bg="Black", fg='White', font='arial 16 bold')
        self.clubIDFullscreen_entry = Entry(rightside_frame, width=12, font='arial 16 bold')
        scoreOffset_label = Label(rightside_frame, width=12, text="Score Offset", bg="Black", fg='White', font='arial 16 bold')
        self.scoreOffsetFullscreen_entry = Entry(rightside_frame, width=12, font='arial 16 bold')
        streamStart_button = Button(rightside_frame, text="Stream", font='arial 16 bold', width=12, height=2)
        capture_button = Button(rightside_frame, text="Capture", font='arial 16 bold', width=12, height=2)
        brightUp_button = Button(rightside_frame)
        brightUp_button.config(image=self.BullsEye.brightUp)
        brightDwn_button = Button(rightside_frame)
        brightDwn_button.config(image=self.BullsEye.brightDwn)
        exit_button = Button(rightside_frame, text='EXIT', font='arial 16 bold', width=12, height=2)

        canvas_frame.grid(row=0, column=0, padx=5, pady=10, rowspan=2)
        canvas.grid(row=0, column=0)
        rightside_frame.grid(row=0, column=1, padx=5, pady=10)
        modelID_label.grid(row=0, column=0, pady=5, columnspan=2)
        self.modelIDFullscreen_entry.grid(row=1, column=0, pady=5, columnspan=2)
        clubID_label.grid(row=2, column=0, pady=5, columnspan=2)
        self.clubIDFullscreen_entry.grid(row=3, column=0, pady=5, columnspan=2)
        scoreOffset_label.grid(row=4, column=0, pady=5, columnspan=2)
        self.scoreOffsetFullscreen_entry.grid(row=5, column=0, pady=5, columnspan=2)
        streamStart_button.grid(row=6, column=0, padx=3, pady=3, columnspan=2)
        capture_button.grid(row=7, column=0, padx=3, pady=3, columnspan=2)
        brightUp_button.grid(row=8, column=0, padx=3, pady=3)
        brightDwn_button.grid(row=8, column=1, padx=3, pady=3)
        exit_button.grid(row=9, column=0, pady=5, columnspan=2)

        streamStart_button.config(command=lambda cv=canvas: self.vidStreamStart(cv, offset=self.scoreOffsetFullscreen_entry ,box=True, resize=(750, 450)))
        capture_button.config(command=lambda cv=canvas: self.captureImg(cv, offset=self.scoreOffsetFullscreen_entry, resize=(750, 450)))
        brightUp_button.config(command=lambda val='+': self.brightnessAdjust(val))
        brightDwn_button.config(command=lambda val='-': self.brightnessAdjust(val))
        exit_button.config(command=self.exitFullscreen)
        self.updateFullscreenModelData()
        self.fullscreenUI.after(20, lambda cv=canvas: self.vidStreamStart(cv,offset=self.scoreOffsetFullscreen_entry, box=True, resize=(750, 450)))

    def UI(self):
        self.frame = Frame(self.master)
        width, height = 490, 150
        left_frame = Frame(self.frame)
        topRight_frame = Frame(self.frame)
        btmRight_frame = Frame(self.frame)
        
        clubSetup_frame = LabelFrame(left_frame, text="Club Setup", width=width, height=255, bd=1, relief='ridge')
        clubSetup_frame.grid_propagate(0)
        clubSelection_frame = Frame(clubSetup_frame, width=width-2, height=115)
        clubSelection_frame.grid_propagate(0)
        lieLoft_frame = Frame(clubSetup_frame, width=width-2, height=115)
        lieLoft_frame.grid_propagate(0)
        
        data_frame = Frame(left_frame, width=width, height=260, bd=1, relief='ridge')
        data_frame.grid_propagate(0)

        
        self.btdata_frame = Frame(data_frame, width=width-10, height=190, bd=1, relief='ridge')
        self.btdata_frame.grid_propagate(0)
        
        self.protdata_frame = Frame(data_frame, width=width-10, height=190, bd=1, relief='ridge')
        self.protdata_frame.grid_propagate(0)
        
        scoreLine_frame = LabelFrame(topRight_frame, text="Scoreline Detection", width=500, height=95, bd=1, relief='ridge')
        scoreLine_frame.grid_propagate(0)
        bullsEyeIndicator_frame = Frame(btmRight_frame, bd=1, relief='ridge', bg="#D1D3D4")
        exit_frame = Frame(btmRight_frame, width=120, height=210, bd=1, relief='ridge')

        left_frame.grid(row=0, column=0, rowspan=2)
        clubSetup_frame.grid(row=0, column=0, padx=10, pady=10)
        clubSelection_frame.grid(row=0, column=0, pady=(2, 1), sticky='N')
        lieLoft_frame.grid(row=1, column=0, pady=(1, 2), sticky='N')
        data_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        self.btdata_frame.grid(row=1, column=0, columnspan=2, padx=5)
        topRight_frame.grid(row=0, column=1)
        btmRight_frame.grid(row=1, column=1, sticky='W')
        scoreLine_frame.grid(row=0, column=0, padx=5, pady=2)
        bullsEyeIndicator_frame.grid(row=0, column=0, padx=5, pady=2, sticky='W')
        exit_frame.grid(row=0, column=1, padx=5, pady=2)
        self.frame.grid(row=0, column=0)

        #Club Selection Menu
        modelID_label = Label(clubSelection_frame, width=10, text="Model ID", bg="Black", fg='White', font='Arial 18 bold')
        self.modelID_entry = Entry(clubSelection_frame, width=16, font='Arial 18 bold')
        clubID_label = Label(clubSelection_frame, width=10, text="Club ID", bg="Black", fg='White', font='Arial 18 bold')
        self.clubID_entry = Entry(clubSelection_frame, width=16, font='Arial 18 bold')
        modelSelection_button = Button(clubSelection_frame, text="Model\nSelect", height=2, width=5, font='Arial 17 bold',
                                       command=self.initSelectModelWindow)
        dexterity_label = Label(clubSelection_frame, width=10, text="Dexterity", bg="Black", fg='White', font='Arial 18 bold')
        rh_button = Radiobutton(clubSelection_frame, text='RIGHT', width=6, font="Arial 20 bold",
                                variable=self.dex, value=0, indicator=0)
        lh_button = Radiobutton(clubSelection_frame, text='LEFT', width=6, font="Arial 20 bold",
                                variable=self.dex, value=1, indicator=0)

        modelID_label.grid(row=0, column=0, padx=5, pady=2)
        self.modelID_entry.grid(row=0, column=1, padx=10, pady=2, columnspan=2)
        clubID_label.grid(row=1, column=0, padx=5, pady=2)
        self.clubID_entry.grid(row=1, column=1, padx=10, pady=2, columnspan=2)
        modelSelection_button.grid(row=0, column=3, padx=2, pady=2, rowspan=2)
        dexterity_label.grid(row=2, column=0, padx=5, pady=2)
        rh_button.grid(row=2, column=1, padx=2, pady=2)
        lh_button.grid(row=2, column=2, padx=2, pady=2)

        #Lie Loft Values Frame
        modelLie_label = Label(lieLoft_frame, text="LIE", width=6, font='Arial 18 bold', bg='Black', fg='White')
        self.modelLie_entry = Entry(lieLoft_frame, width=6, font='Arial 18 bold')
        modelLoft_label = Label(lieLoft_frame, text="LOFT", width=6, font='Arial 18 bold', bg='Black', fg='White')
        self.modelLoft_entry = Entry(lieLoft_frame, width=6, font='Arial 18 bold')
        offset_label = Label(lieLoft_frame, text="Offset", width=6, font='Arial 18 bold', bg='Black', fg='White')
        self.offsetLie_entry = Entry(lieLoft_frame, width=6, font='Arial 18 bold')
        self.offsetLoft_entry = Entry(lieLoft_frame, width=6, font='Arial 18 bold')
        lockOffset_button = Button(lieLoft_frame, width=5, height=2, font='Arial 16 bold', text='Lock\nOffset')
        lieDwn_button = Button(lieLoft_frame, text='LIE-', width=6, font='Arial 14 bold',
                               command=lambda field='lie', val=-0.5: self.updateOffSetValues(field, val))
        lieUp_button = Button(lieLoft_frame, text='LIE+', width=6, font='Arial 14 bold',
                              command=lambda field='lie', val=0.5: self.updateOffSetValues(field, val))
        loftDwn_button = Button(lieLoft_frame, text='LOFT-', width=6, font='Arial 14 bold',
                                command=lambda field='loft', val=-0.5: self.updateOffSetValues(field, val))
        loftUp_button = Button(lieLoft_frame, text='LOFT+', width=6, font='Arial 14 bold',
                               command=lambda field='loft', val=0.5: self.updateOffSetValues(field, val))

        modelLie_label.grid(row=0, column=0, padx=3, pady=2)
        self.modelLie_entry.grid(row=0, column=1, padx=3, pady=2)
        modelLoft_label.grid(row=0, column=2, padx=3, pady=2)
        self.modelLoft_entry.grid(row=0, column=3, padx=3, pady=2)
        offset_label.grid(row=1, column=0, padx=3, pady=2)
        self.offsetLie_entry.grid(row=1, column=1, padx=3, pady=2)
        self.offsetLoft_entry.grid(row=1, column=3, padx=3, pady=2)
        lockOffset_button.grid(row=0, column=4, padx=2, pady=2, rowspan=2)
        lieDwn_button.grid(row=2, column=0, padx=3, pady=2)
        lieUp_button.grid(row=2, column=1, padx=3, pady=2)
        loftDwn_button.grid(row=2, column=2, padx=3, pady=2)
        loftUp_button.grid(row=2, column=3, padx=3, pady=2)

        offsetButtons = (lieDwn_button, lieUp_button, loftDwn_button, loftUp_button)
        lockOffset_button.configure(command=lambda bt1=lockOffset_button, bt2=offsetButtons: self.toggleOffsetLock(bt1, bt2))

        #Tabscreen Control Buttons
        showBT_button = Button(data_frame, text="BT Puck", font='Arial 20 bold', command=self.showBT)
        showProt_button = Button(data_frame, text="Protractor", font='Arial 20 bold', command=self.showProt)
        showBT_button.grid(row=0, column=0, padx=(5, 2), pady=5)
        showProt_button.grid(row=0, column=1, padx=(2, 5), pady=5)

        #Frame for Protractor Data
        protractor_label = Label(self.protdata_frame, width=8, text='Prot.', font='Arial 16 bold', bg='black', fg='white')
        actual_label = Label(self.protdata_frame, width=6, text='Actual', font='Arial 16 bold', bg='black', fg='white')
        target_label = Label(self.protdata_frame, width=6, text='Target', font='Arial 16 bold', bg='black', fg='white')
        diff_label = Label(self.protdata_frame, width=6, text='Diff', font='Arial 16 bold', bg='black', fg='white')

        loft_label = Label(self.protdata_frame, width=8, text='Loft', font='Arial 16 bold', bg='black', fg='white')
        lie_label = Label(self.protdata_frame, width=8, text='Lie', font='Arial 16 bold', bg='black', fg='white')
        self.loft_entry = Entry(self.protdata_frame, width=6, font='Arial 16 bold')
        self.lie_entry = Entry(self.protdata_frame, width=6, font='Arial 16 bold')
        self.protTargetLoft_entry = Entry(self.protdata_frame, width=6, font='Arial 16 bold')
        self.protTargetLie_entry = Entry(self.protdata_frame, width=6, font='Arial 16 bold')
        self.diffLoftProt_entry = Entry(self.protdata_frame, width=6, font='Arial 16 bold')
        self.diffLieProt_entry = Entry(self.protdata_frame, width=6, font='Arial 16 bold')
        self.frameAngle_entry = Entry() #Not shown on Grid, needed for angleStreamStart() function
        prevClub_button = Button(self.protdata_frame, height=2, width=8, text="Prev\nClub", font='Arial 12 bold', padx=1,
                command=self.previousClub)
        nextClub_button = Button(self.protdata_frame, height=2, width=8, text="Next\nClub", font='Arial 12 bold', padx=1,
                command=self.nextClub)

        self.protStreamStart_button = Button(self.protdata_frame, text="Stream\nStart", font='Arial 12 bold', padx=1, width=8, height=2)
        self.protStreamStart_button.configure(command= lambda: self.angleStreamStart(
                                  self.lie_entry, self.loft_entry, self.frameAngle_entry,
                                  diff=(self.diffLieProt_entry, self.diffLoftProt_entry),
                                  btStreamButton=self.btStreamStart_button,
                                  toggle=self.protStreamStart_button,
                                  indicator=self.bullsEye_canvas))
        setMCREF_button = Button(self.protdata_frame, text="MC\nREF", font='Arial 12 bold', padx=1, width=8, height=2,
            command=lambda: self.setMCREF(self.lie_entry, self.loft_entry, self.frameAngle_entry))

        protractor_label.grid(row=0, column=0, padx=6, pady=2)
        actual_label.grid(row=0, column=1, padx=6, pady=2, sticky='')
        target_label.grid(row=0, column=2, padx=6, pady=2, sticky='')
        diff_label.grid(row=0, column=3, padx=6, pady=2, sticky='')
        loft_label.grid(row=1, column=0, padx=6, pady=2, sticky='')
        lie_label.grid(row=2, column=0, padx=6, pady=2, sticky='')
        self.loft_entry.grid(row=1, column=1, padx=6, pady=8, sticky='')
        self.lie_entry.grid(row=2, column=1, padx=6, pady=8, sticky='')
        self.protTargetLoft_entry.grid(row=1, column=2, padx=6, pady=8, sticky='')
        self.protTargetLie_entry.grid(row=2, column=2, padx=6, pady=8, sticky='')
        self.diffLoftProt_entry.grid(row=1, column=3, padx=6, pady=8, sticky='')
        self.diffLieProt_entry.grid(row=2, column=3, padx=6, pady=8, sticky='')
        prevClub_button.grid(row=3, column=2, padx=6, pady=1, sticky='')
        nextClub_button.grid(row=3, column=3, padx=6, pady=1, sticky='')
                
        self.protStreamStart_button.grid(row=0, column=4, padx=6, pady=1, rowspan=2)
        setMCREF_button.grid(row=2, column=4, padx=6, pady=1, rowspan=2)

        #Frame for BT Data
        puck_label = Label(self.btdata_frame, width=8, text='Puck', font='Arial 16 bold', bg='black', fg='white')
        loft_label = Label(self.btdata_frame, width=8, text='Loft', font='Arial 16 bold', bg='black', fg='white')
        lie_label = Label(self.btdata_frame, width=8, text='Lie', font='Arial 16 bold', bg='black', fg='white')
        btHeading_label = Label(self.btdata_frame, width=8, text='Heading', font='Arial 16 bold', bg='black', fg='white')
        measured_label = Label(self.btdata_frame, width=6, text='Actual', font='Arial 16 bold', bg='black', fg='white')
        target_label = Label(self.btdata_frame, width=6, text='Target', font='Arial 16 bold', bg='black', fg='white')
        diff_label = Label(self.btdata_frame, width=6, text='Diff', font='Arial 16 bold', bg='black', fg='white')
        self.btLoft_entry = Entry(self.btdata_frame, width=6, font='Arial 16 bold')
        self.btLie_entry = Entry(self.btdata_frame, width=6, font='Arial 16 bold')
        self.targetLoft_entry = Entry(self.btdata_frame, width=6, font='arial 16 bold')
        self.targetLie_entry = Entry(self.btdata_frame, width=6, font='arial 16 bold')
        self.diffLoft_entry = Entry(self.btdata_frame, width=6, font='arial 16 bold')
        self.diffLie_entry = Entry(self.btdata_frame, width=6, font='arial 16 bold')
        self.btHeading_entry = Entry(self.btdata_frame, width=6, font='arial 16 bold')
        self.btStreamStart_button = Button(self.btdata_frame, height=2, width=8, text="Stream\nStart", font='Arial 12 bold', padx=1)
        #btStreamStart_button command configed further below 
        btTareValueZero_button = Button(self.btdata_frame, height=2, width=8, text="Tare\nZero", font='Arial 12 bold', padx=1,
                                        command=self.btTareToZero)
        prevClub_button = Button(self.btdata_frame, height=2, width=8, text="Prev\nClub", font='Arial 12 bold', padx=1,
                                 command=self.previousClub)
        nextClub_button = Button(self.btdata_frame, height=2, width=8, text="Next\nClub", font='Arial 12 bold', padx=1,
                                 command=self.nextClub)

        puck_label.grid(row=0, column=0, padx=6, pady=2)
        measured_label.grid(row=0, column=1, padx=6, pady=2)
        target_label.grid(row=0, column=2, padx=6, pady=2, sticky='')
        diff_label.grid(row=0, column=3, padx=6, pady=2, sticky='')
        loft_label.grid(row=1, column=0, padx=6, pady=2, sticky='')
        lie_label.grid(row=2, column=0, padx=6, pady=2, sticky='')
        btHeading_label.grid(row=3, column=0, padx=6, pady=2, sticky='')
        self.btLoft_entry.grid(row=1, column=1, padx=6, pady=8, sticky='')
        self.btLie_entry.grid(row=2, column=1, padx=6, pady=8, sticky='')
        self.btHeading_entry.grid(row=3, column=1, padx=6, pady=8, sticky='')
        self.targetLoft_entry.grid(row=1, column=2, padx=6, pady=8, sticky='')
        self.targetLie_entry.grid(row=2, column=2, padx=6, pady=8, sticky='')
        self.diffLoft_entry.grid(row=1, column=3, padx=6, pady=8, sticky='')
        self.diffLie_entry.grid(row=2, column=3, padx=6, pady=8, sticky='')
        self.btStreamStart_button.grid(row=0, column=4, padx=6, pady=1, sticky='', rowspan=2)
        btTareValueZero_button.grid(row=2, column=4, padx=8, pady=1, sticky='', rowspan=2)
        prevClub_button.grid(row=3, column=2, padx=6, pady=1, sticky='')
        nextClub_button.grid(row=3, column=3, padx=6, pady=1, sticky='')

        self.BTmainEntry = (self.btLoft_entry, self.btLie_entry, self.btHeading_entry)
        self.BTdiffEntry = (self.diffLoft_entry, self.diffLie_entry)

        self.btStreamStart_button.config(command=lambda:
            self.btStreamStart(self.BTmainEntry,
                               diffEntry=self.BTdiffEntry,
                               toggle=self.btStreamStart_button,
                               indicator=self.bullsEye_canvas,
                               angleStreamButton=self.protStreamStart_button))

        #Score detection && Servo Controller
        scoreOffset_label = Label(scoreLine_frame, text="Score", height=1, width=5, font='Arial 14 bold', bg='Black', fg='White')
        self.scoreOffset_entry = Entry(scoreLine_frame, width=5, font='Arial 14 bold')
        captureOffset_button = Button(scoreLine_frame, text='Cap.\nOffset', height=2, width=4, font='Arial 14 bold')
        fullscreen_button = Button(scoreLine_frame, text='Full\nScreen', height=2, width=4, font='Arial 14 bold')

        captureOffset_button.configure(command=lambda cv=None: self.captureImg(None, offset=self.scoreOffset_entry))
        fullscreen_button.configure(command=self.fullscreen_menu)

        frameAngle_label = Label(scoreLine_frame, text="Frame", height=1, width=6, font='Arial 14 bold', bg='Black', fg='White')
        self.frameAngle_entry = Entry(scoreLine_frame, width=6, font='Arial 14 bold')
        servoLeft_button = Button(scoreLine_frame, command=lambda d='+', f=self.frameAngle_entry: self.motorRotate(d, f))
        servoLeft_button.config(image=self.BullsEye.servoWeak)
        servoLeft_button.config(state='disabled')
        servoRight_button = Button(scoreLine_frame, command=lambda d='-', f=self.frameAngle_entry: self.motorRotate(d, f))
        servoRight_button.config(image=self.BullsEye.servoStrong)
        servoRight_button.config(state='disabled')
        enable_button = Button(scoreLine_frame, text="Enable\nFrame", height=2, width=5, font='Arial 13 bold')
        enable_button.config(command=lambda: self.enableMotorControls(enable_button,
                                                              (servoRight_button, servoLeft_button),
                                                              (self.btStreamStart_button, self.protStreamStart_button)))
        
        scoreOffset_label.grid(row=0, column=0, padx=1, pady=0)
        self.scoreOffset_entry.grid(row=1, column=0, padx=1, pady=2)
        captureOffset_button.grid(row=0, column=1, padx=1, pady=0, rowspan=2)
        fullscreen_button.grid(row=0, column=2, padx=1, pady=0, rowspan=2)
        frameAngle_label.grid(row=0, column=3, padx=3, pady=0)
        self.frameAngle_entry.grid(row=1, column=3, padx=3, pady=2)
        servoLeft_button.grid(row=0, column=4, padx=3, pady=0, rowspan=2)
        servoRight_button.grid(row=0, column=5, padx=3, pady=0, rowspan=2)
        enable_button.grid(row=0, column=6, padx=3, pady=0, rowspan=2)
        
        #BullsEye Display
        self.bullsEye_canvas = Canvas(bullsEyeIndicator_frame, height=410, width=410)
        self.bullsEye_canvas.create_image(205, 205, image=self.BullsEye.bullsEyeIndicator)
        self.bullsEye_canvas.grid(row=0, column=0)

        # Exit Frame
        exitApp_button = Button(exit_frame, command=lambda m=self.master: self.exitMenu(m))
        exitApp_button.config(image=self.BullsEye.mainMenu)
        exitApp_button.grid(row=0, column=0, padx=1, pady=10)
        
    def showBT(self):
        self.protdata_frame.grid_forget()
        self.btdata_frame.grid_propagate(0)
        self.btdata_frame.grid(row=1, column=0, columnspan=2, padx=5, sticky='N')
        
    def showProt(self):
        self.btdata_frame.grid_forget()
        self.protdata_frame.grid_propagate(0)
        self.protdata_frame.grid(row=1, column=0, columnspan=2, padx=5, sticky='N')

    def initSelectModelWindow(self):
        self.turnOffStream()
        self.selectModelWindow = Toplevel(height=600, width=1024, bd=2, relief='ridge')
        self.selectModelWindow.attributes('-fullscreen', True)
        self.selectModelWindow.grid_propagate(0)
        modelList_frame = LabelFrame(self.selectModelWindow, text='Model Selection', border=3, relief='ridge',
                                     height=600, width=300)
        modelList_frame.pack_propagate(0)
        modelList_canvas = Canvas(modelList_frame, height=550, width=250)
        modelList_subFrame = Frame(modelList_canvas)
        modelListUp_button = Button(modelList_frame, text='UP', width=3, height=6)
        modelListDwn_button = Button(modelList_frame, text='DWN', width=3, height=6)
        modelList_canvas.create_window(0, 0, window=modelList_subFrame, anchor='nw')
        self.clubList_frame = LabelFrame(self.selectModelWindow, text='Club Selection', border=3, relief='ridge')
        self.right_frame = Frame(self.selectModelWindow, height=550, width=150)

        i=0
        for model in self.BullsEye.modelList.values():
            label = Label(modelList_subFrame, text=model.modelID)
            label.grid(row=i, column=0, padx=5, pady=5)
            button = Button(modelList_subFrame, text='Select', height=2)
            button.config(command=lambda a=model: self.loadClubList(a))
            button.grid(row=i, column=1, padx=5, pady=5)
            i = i+1

        exit_button = Button(self.right_frame, text='Exit', font='Arial 15 bold', height=2, width=10,
                             command=self.exitModelSelectWindow)

        self.frame.update()
        modelList_canvas.configure(scrollregion=modelList_canvas.bbox('all'))
        modelListUp_button.configure(command=lambda: modelList_canvas.yview_scroll(-7, 'units'))
        modelListDwn_button.configure(command=lambda: modelList_canvas.yview_scroll(7, 'units'))
        modelList_canvas.grid(row=0, column=0, rowspan=2)
        modelListUp_button.grid(row=0, column=1, padx=5)
        modelListDwn_button.grid(row=1, column=1, padx=5)
        modelList_frame.grid(row=0, column=0, sticky='n')
        self.clubList_frame.grid(row=0, column=1, padx=5,  sticky='n')
        self.right_frame.grid(row=0, column=2, sticky='n')
        exit_button.grid(row=1, column=0, pady=10)

        self.loadClubList(self.BullsEye.currentModel)
        self.currentClubWindow()
        self.updateSelectWindowCurrentValues()

    def loadClubList(self, model):
        #model is a model object from model class
        for child in self.clubList_frame.winfo_children():
            child.destroy()

        clubList_canvas = Canvas(self.clubList_frame, height=550, width=255)
        clubList_subFrame = Frame(clubList_canvas)
        clubListUp_button = Button(self.clubList_frame, text='UP', width=3, height=6)
        clubListDwn_button = Button(self.clubList_frame, text='DWN', width=3, height=6)
        clubList_canvas.create_window(0, 0, window=clubList_subFrame, anchor='nw')

        modelFrame = Frame(clubList_subFrame)
        modelFrame.grid(row=0, column=0, columnspan=4)
        self.clubList_frame.configure(text=model.modelID)
        Label(clubList_subFrame, text='Club#', font='Arial 12 bold', width=9).grid(row=1, column=0, padx=5, pady=5)
        Label(clubList_subFrame, text='Lie', font='Arial 12 bold', width=4).grid(row=1, column=1, padx=5, pady=5)
        Label(clubList_subFrame, text='Loft', font='Arial 12 bold', width=4).grid(row=1, column=2, padx=5, pady=5)

        i = 0
        for club in model.clubs:
            Label(clubList_subFrame, text=club.clubID, width=9).grid(row=i+2, column=0, padx=2, pady=5)
            Label(clubList_subFrame, text=club.lie, width=4).grid(row=i+2, column=1, padx=2, pady=5)
            Label(clubList_subFrame, text=club.loft, width=4).grid(row=i+2, column=2, padx=2, pady=5)
            setButton = Button(clubList_subFrame, text='Set', width=5, height=2, padx=1, pady=5)
            setButton.config(command=lambda c=club: self.updateCurrentClub(c))
            setButton.grid(row=i+2, column=3, padx=2, pady=5)
            i = i + 1

        self.frame.update()
        clubList_canvas.configure(scrollregion=clubList_canvas.bbox('all'))
        clubListUp_button.configure(command=lambda: clubList_canvas.yview_scroll(-7, 'units'))
        clubListDwn_button.configure(command=lambda: clubList_canvas.yview_scroll(7, 'units'))
        clubList_canvas.grid(row=0, column=0, rowspan=2)
        clubListUp_button.grid(row=0, column=1, padx=3)
        clubListDwn_button.grid(row=1, column=1, padx=3)

    def currentClubWindow(self):
        frame = LabelFrame(self.right_frame, text='Current Club')
        modelID_label = Label(frame, text='Model', width=6, font='Arial 13 bold', fg='white', bg='black')
        clubID_label = Label(frame, text='Club', width=6, font='Arial 13 bold', fg='white', bg='black')
        self.modelIDSelectWindow_entry = Entry(frame, width=15, font='Arial 13 bold')
        self.clubIDSelectWindow_entry = Entry(frame, width=15, font='Arial 13 bold')
        lieloft_frame = Frame(frame)
        lie_label = Label(lieloft_frame, text='Lie', width=5, font='Arial 13 bold', fg='white', bg='black')
        loft_label = Label(lieloft_frame, text='Loft', width=5, font='Arial 13 bold', fg='white', bg='black')
        self.lieSelectWindow_entry = Entry(lieloft_frame, width=5, font='Arial 13 bold')
        self.loftSelectWindow_entry = Entry(lieloft_frame, width=5, font='Arial 13 bold')

        frame.grid(row=0, column=0)
        modelID_label.grid(row=0, column=0)
        clubID_label.grid(row=1, column=0)
        self.modelIDSelectWindow_entry.grid(row=0, column=1)
        self.clubIDSelectWindow_entry.grid(row=1, column=1)
        lieloft_frame.grid(row=2, column=0, columnspan=4)
        lie_label.grid(row=2, column=0)
        loft_label.grid(row=2, column=2)
        self.lieSelectWindow_entry.grid(row=2, column=1)
        self.loftSelectWindow_entry.grid(row=2, column=3)

    def updateCurrentClub(self, club):
        self.BullsEye.currentModel = self.BullsEye.modelList[club.modelID]
        self.BullsEye.currentClubIndex = self.BullsEye.currentModel.clubs.index(club)
        if hasattr(self, 'selectModelWindow'):
            if self.selectModelWindow.winfo_exists():
                self.updateSelectWindowCurrentValues()
        self.updateGuidedModeMenuModelData()

    def nextClub(self):
        clubList = self.BullsEye.currentModel.clubs
        if self.BullsEye.currentClubIndex + 1 < len(clubList):
            club = clubList[self.BullsEye.currentClubIndex + 1]
            self.updateCurrentClub(club)
        else: self.updateCurrentClub(clubList[0])
        self.turnOffStream()
        self.seekAngleValue(self.BullsEye.currentModel.clubs[self.BullsEye.currentClubIndex].loft, self.frameAngle_entry)

    def previousClub(self):
        clubList = self.BullsEye.currentModel.clubs
        if self.BullsEye.currentClubIndex > 0:
            club = clubList[self.BullsEye.currentClubIndex - 1]
            self.updateCurrentClub(club)
        else: self.updateCurrentClub(clubList[len(clubList)-1])
        self.turnOffStream()
        self.seekAngleValue(self.BullsEye.currentModel.clubs[self.BullsEye.currentClubIndex].loft,self.frameAngle_entry)
    
    def turnOffStream(self):
        if self.BullsEye.btStreamActive is True:
            self.btStreamEnd(self.BTmainEntry,
                               diffEntry=self.BTdiffEntry,
                               toggle=self.btStreamStart_button,
                               indicator=self.bullsEye_canvas,
                               angleStreamButton=self.protStreamStart_button)
        if self.BullsEye.angleStreamActive is True:
            self.captureAngle(self.lie_entry, self.loft_entry, self.frameAngle_entry,
                                  diff=(self.diffLie_entry, self.diffLoft_entry),
                                  btStreamButton=self.btStreamStart_button,
                                  toggle=self.protStreamStart_button,
                                  indicator=self.bullsEye_canvas)
    
    def updateOffSetValues(self, var, increment):
        if var == "loft":
            self.tgtLoftOffset = float(self.tgtLoftOffset) + increment
            self.offsetLoft_entry.delete(0, END)
            if self.tgtLoftOffset>=0: self.offsetLoft_entry.insert(END, '+')
            self.offsetLoft_entry.insert(END, self.tgtLoftOffset)
        elif var == "lie":
            self.tgtLieOffset = float(self.tgtLieOffset) + increment
            self.offsetLie_entry.delete(0, END)
            if self.tgtLieOffset >= 0: self.offsetLie_entry.insert(END, '+')
            self.offsetLie_entry.insert(END, self.tgtLieOffset)
        self.updateTargetLieLoft()

    def updateSelectWindowCurrentValues(self):
        clubObj = self.BullsEye.currentModel.clubs[self.BullsEye.currentClubIndex]
        self.modelIDSelectWindow_entry.delete(0, END)
        self.clubIDSelectWindow_entry.delete(0, END)
        self.lieSelectWindow_entry.delete(0, END)
        self.loftSelectWindow_entry.delete(0, END)

        self.modelIDSelectWindow_entry.insert(END, self.BullsEye.currentModel.modelID)
        self.clubIDSelectWindow_entry.insert(END, clubObj.clubID)
        self.lieSelectWindow_entry.insert(END, clubObj.lie)
        self.loftSelectWindow_entry.insert(END, clubObj.loft)

    def updateGuidedModeMenuModelData(self):
        clubObj = self.BullsEye.currentModel.clubs[self.BullsEye.currentClubIndex]
        self.modelID_entry.delete(0, END)
        self.clubID_entry.delete(0, END)
        self.modelLoft_entry.delete(0, END)
        self.modelLie_entry.delete(0, END)
        self.modelID_entry.insert(END, self.BullsEye.currentModel.modelID)
        self.clubID_entry.insert(END, clubObj.clubID)
        self.modelLoft_entry.insert(END, clubObj.loft)
        self.modelLie_entry.insert(END, clubObj.lie)
        self.updateTargetLieLoft()

    def updateFullscreenModelData(self):
        clubObj = self.BullsEye.currentModel.clubs[self.BullsEye.currentClubIndex]
        self.modelIDFullscreen_entry.delete(0, END)
        self.clubIDFullscreen_entry.delete(0, END)
        self.modelIDFullscreen_entry.insert(END, self.BullsEye.currentModel.modelID)
        self.clubIDFullscreen_entry.insert(END, clubObj.clubID)

    def updateTargetLieLoft(self):
        clubObj = self.BullsEye.currentModel.clubs[self.BullsEye.currentClubIndex]
        lie = float(clubObj.lie) + float(self.tgtLieOffset)
        loft = float(clubObj.loft) + float(self.tgtLoftOffset)
        self.BullsEye.targetLoft = loft
        self.BullsEye.targetLie = lie
        self.targetLie_entry.delete(0, END)
        self.targetLoft_entry.delete(0, END)
        self.targetLie_entry.insert(END, lie)
        self.targetLoft_entry.insert(END, loft)
        self.protTargetLoft_entry.delete(0, END)
        self.protTargetLie_entry.delete(0, END)
        self.protTargetLoft_entry.insert(END, loft)
        self.protTargetLie_entry.insert(END, lie)
    
    def exitModelSelectWindow(self):
        self.selectModelWindow.destroy()
        self.updateGuidedModeMenuModelData()
        self.seekAngleValue(self.BullsEye.currentModel.clubs[self.BullsEye.currentClubIndex].loft, self.frameAngle_entry)

    def exitFullscreen(self):
        self.BullsEye.vidStreamActive = False
        self.fullscreenUI.destroy()
        if self.BullsEye.lieOffset:
            self.scoreOffset_entry.delete(0, END)
            self.scoreOffset_entry.insert(END, self.BullsEye.lieOffset)
        else:
            self.scoreOffset_entry.delete(0, END)
            self.scoreOffset_entry.insert(END, 0.0)
        if self.BullsEye.btStreamActive or self.BullsEye.angleStreamActive: return
        else: self.btStreamStart(self.BTmainEntry, diffEntry=self.BTdiffEntry, toggle=self.btStreamStart_button,
                                 indicator=self.bullsEye_canvas, angleStreamButton=self.protStreamStart_button)

    def toggleOffsetLock(self, buttonSelf, offsetButtons):
        if self.lockOffsetStatus == False:
            self.lockOffsetStatus = True
            buttonSelf.configure(text="Unlock\nOffset")
            for button in offsetButtons:
                button.configure(state='disabled')
        elif self.lockOffsetStatus == True:
            self.lockOffsetStatus = False
            buttonSelf.configure(text="Lock\nOffset")
            for button in offsetButtons:
                button.configure(state='normal')

