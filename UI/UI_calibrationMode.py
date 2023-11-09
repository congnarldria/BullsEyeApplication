from tkinter import *
from UI import UIsharedFunctions
from os import listdir
import math


class calibrationMode(UIsharedFunctions.sharedFunctions):
    def __init__(self, master, BullsEye):
        self.master = master
        self.BullsEye = BullsEye
        self.BullsEye.angleStreamActive = False
        self.BullsEye.vidStreamActive = False
        self.BullsEye.btStreamActive = False
        self.instructionImgNo = 0
        self.importInstructionImages()
        self.UI()

    def importInstructionImages(self):
        self.instructionsBack = self.getImage("/home/pi/BullsEyeApplication/UI/icons/instructionsBack.png",
                                              resize=(60, 110))
        self.instructionsNext = self.getImage("/home/pi/BullsEyeApplication/UI/icons/instructionsNext.png",
                                              resize=(60, 110))
        self.instructionImages = []
        imgPathList = listdir("/home/pi/BullsEyeApplication/UI/icons/calModeInstructions/")
        imgPathList.sort()
        for imgName in imgPathList:
            imgPath = "/home/pi/BullsEyeApplication/UI/icons/calModeInstructions/" + imgName
            img = self.getImage(imgPath)
            self.instructionImages.append(img)

    def UI(self):
        self.frame = Frame(self.master)

        # Frames
        left_frame = Frame(self.frame, width=500, height=460)
        left_frame.grid_propagate(0)
        right_frame = Frame(self.frame, width=500, height=460)
        right_frame.grid_propagate(0)
        bottom_frame = Frame(self.frame, width=1014, height=140)
        bottom_frame.grid_propagate(0)

        canvas_frame = Frame(left_frame, width=500, height=300, bg='white')
        canvas_frame.grid_propagate(0)

        lieCal_frame = LabelFrame(left_frame, text="Lie Angle Calirbation", width=500, height=140, bd=1, relief='ridge')
        lieCal_frame.grid_propagate(0)

        cameraControl_frame = Frame(lieCal_frame)
        scoreline_frame = Frame(lieCal_frame)

        boundBox_frame = LabelFrame(bottom_frame, text='Image Recognition Controls', width=750, height=135, bd=1,
                                    relief='ridge')
        boundBox_frame.grid_propagate(0)

        instructions_frame = LabelFrame(right_frame, text="Instructions", width=500, height=170, bd=1, relief='ridge')
        instructions_frame.grid_propagate(0)

        calStickVal_frame = LabelFrame(right_frame, text="Calibration Stick Value", width=245, height=95, bd=1,
                                       relief='ridge')
        calStickVal_frame.grid_propagate(0)

        motorControl_frame = LabelFrame(right_frame, text="Servo Controller", width=245, height=95, bd=1,
                                        relief='ridge')
        motorControl_frame.grid_propagate(0)

        loftCal_frame = LabelFrame(right_frame, text="Loft Calibration", width=500, height=160, bd=1, relief='ridge')
        loftCal_frame.grid_propagate(0)

        # Inserting Frame Objects
        left_frame.grid(row=0, column=0, padx=5)
        right_frame.grid(row=0, column=1, padx=5)
        bottom_frame.grid(row=1, column=0, padx=5, columnspan=2, sticky='W')
        canvas_frame.grid(row=0, column=0, pady=2)
        lieCal_frame.grid(row=1, column=0, pady=(2, 0))
        boundBox_frame.grid(row=0, column=0, sticky='W')

        cameraControl_frame.grid(row=0, column=0, padx=5, pady=0, sticky='W')
        scoreline_frame.grid(row=1, column=0, padx=5, pady=0)

        instructions_frame.grid(row=0, column=0, pady=5, columnspan=2)
        calStickVal_frame.grid(row=1, column=0, padx=(0, 2), pady=3)
        motorControl_frame.grid(row=1, column=1, padx=(2, 0), pady=3)
        loftCal_frame.grid(row=2, column=0, pady=(5, 0), columnspan=2)

        # Canvas for Image
        canvas = Label(canvas_frame, bg='white')
        canvas.grid(row=0, column=0, sticky=N)

        # Camera Controls
        stream_button = Button(cameraControl_frame, text="Stream", height=2, width=6, font='Arial 12 bold')
        capture_button = Button(cameraControl_frame, text="Capture", height=2, width=6, font='Arial 12 bold')
        brightDwn_button = Button(cameraControl_frame, command=lambda v='-': self.brightnessAdjust(v))
        brightDwn_button.configure(image=self.BullsEye.brightDwn)
        brightUp_button = Button(cameraControl_frame, command=lambda v='+': self.brightnessAdjust(v))
        brightUp_button.configure(image=self.BullsEye.brightUp)
        stream_button.grid(row=0, column=0, padx=5, pady=2)
        capture_button.grid(row=0, column=1, padx=5, pady=2)
        brightDwn_button.grid(row=0, column=2, padx=5, pady=2)
        brightUp_button.grid(row=0, column=3, padx=5, pady=2)

        # Scoreline Lie Offset Values
        zeroLine_label = Label(scoreline_frame, text="ZeroLine", height=1, width=9, font='Arial 12 bold', bg='black',
                               fg='white')
        self.zeroLine_entry = Entry(scoreline_frame, width=7, font='Arial 12 bold')
        offset_label = Label(scoreline_frame, text="Offset", height=1, width=9, font='Arial 12 bold', bg='black',
                             fg='white')
        self.calOffset_entry = Entry(scoreline_frame, width=7, font='Arial 12 bold')
        update_button = Button(scoreline_frame, text="Update\nZeroLine", height=2, width=8, padx=0,
                               font='Arial 12 bold')
        resetZeroLine_button = Button(scoreline_frame, text="Reset\nZeroLine", height=2, width=8, padx=0,
                                      font='Arial 12 bold')
        resetOffset_button = Button(scoreline_frame, text="Clear\nOffset", height=2, width=8, padx=0,
                                    font='Arial 12 bold')

        zeroLine_label.grid(row=0, column=0, padx=2, pady=3)
        self.zeroLine_entry.grid(row=0, column=1, padx=2, pady=3)
        offset_label.grid(row=1, column=0, padx=2, pady=3)
        self.calOffset_entry.grid(row=1, column=1, padx=2, pady=3)
        update_button.grid(row=0, column=2, padx=2, pady=3, rowspan=2)
        resetZeroLine_button.grid(row=0, column=3, padx=2, pady=3, rowspan=2)
        resetOffset_button.grid(row=0, column=4, padx=2, pady=3, rowspan=2)

        # instructions Frame
        instructionBack_button = Button(instructions_frame, command=lambda dir='<': self.updateInstructionsImage(dir))
        instructionBack_button.configure(image=self.instructionsBack)
        instructionsImage_frame = Frame(instructions_frame, height=145, width=335, bg='white')
        instructionsImage_frame.grid_propagate(0)
        self.instructions_label = Label(instructionsImage_frame)
        instructionNext_button = Button(instructions_frame, command=lambda dir='>': self.updateInstructionsImage(dir))
        instructionNext_button.configure(image=self.instructionsNext)
        instructionBack_button.grid(row=0, column=0, padx=5)
        instructionsImage_frame.grid(row=0, column=1, padx=5)
        self.instructions_label.grid(row=0, column=0, padx=2, pady=2)
        instructionNext_button.grid(row=0, column=2, padx=5)

        if len(self.instructionImages) > 0:
            self.instructions_label.configure(image=self.instructionImages[0])

        # Motor Control Frame
        frameDwn_button = Button(motorControl_frame, font='Arial 12 bold')
        frameUp_button = Button(motorControl_frame, font='Arial 12 bold')
        frameHome_button = Button(motorControl_frame, font='Arial 12 bold')
        frameDwn_button.configure(image=self.BullsEye.servoStrong)
        frameUp_button.configure(image=self.BullsEye.servoWeak)
        frameHome_button.configure(image=self.BullsEye.servoHome)

        frameDwn_button.grid(row=0, column=1, padx=(10, 2), pady=(5, 1), sticky='')
        frameUp_button.grid(row=0, column=0, padx=2, pady=(5, 1), sticky='')
        frameHome_button.grid(row=0, column=2, padx=(2, 10), pady=(5, 1), sticky='')
        # calStickVal_frame
        calStickUp_button = Button(calStickVal_frame, text="+", height=1, width=5, font='Arial 10 bold',
                                   command=lambda: self.calStickValChange(0.1))
        calStickUp2_button = Button(calStickVal_frame, text="++", height=1, width=5, font='Arial 10 bold',
                                    command=lambda: self.calStickValChange(1))
        calStickDwn_button = Button(calStickVal_frame, text="--", height=1, width=5, font='Arial 10 bold',
                                    command=lambda: self.calStickValChange(-0.1))
        calStickDwn2_button = Button(calStickVal_frame, text="----", height=1, width=5, font='Arial 10 bold',
                                     command=lambda: self.calStickValChange(-1))
        self.calStickVal_entry = Entry(calStickVal_frame, width=6, font='Arial 18 bold')

        calStickDwn2_button.grid(row=0, column=0, padx=(14, 3), pady=3, sticky='')
        calStickDwn_button.grid(row=1, column=0, padx=(14, 3), pady=3, sticky='')
        self.calStickVal_entry.grid(row=0, column=1, padx=3, pady=3, sticky='', rowspan=2)
        calStickUp2_button.grid(row=0, column=2, padx=3, pady=3, sticky='')
        calStickUp_button.grid(row=1, column=2, padx=3, pady=3, sticky='')

        # loftCal_frame
        lieSys_label = Label(loftCal_frame, text="Lie Sys", height=1, width=9, font='Arial 13 bold', bg='black',
                             fg='white')
        self.lieSys_entry = Entry(loftCal_frame, width=7, font='Arial 13 bold')
        loftSys_label = Label(loftCal_frame, text="Loft Sys", height=1, width=9, font='Arial 13 bold', bg='black',
                              fg='white')
        self.loftSys_entry = Entry(loftCal_frame, width=7, font='Arial 13 bold')
        calcFrame_label = Label(loftCal_frame, text="C.Frame", height=1, width=9, font='Arial 13 bold', bg='black',
                                fg='white')
        self.calcFrame_entry = Entry(loftCal_frame, width=7, font='Arial 13 bold')
        frame_label = Label(loftCal_frame, text="Frame", height=1, width=9, font='Arial 13 bold', bg='black',
                            fg='white')
        self.frameCalMenu_entry = Entry(loftCal_frame, width=7, font='Arial 13 bold')

        lieSys_label.grid(row=0, column=0, padx=2, pady=3, sticky='')
        self.lieSys_entry.grid(row=0, column=1, padx=2, pady=3, sticky='')
        loftSys_label.grid(row=1, column=0, padx=2, pady=3, sticky='')
        self.loftSys_entry.grid(row=1, column=1, padx=2, pady=3, sticky='')
        calcFrame_label.grid(row=2, column=0, padx=2, pady=3, sticky='')
        self.calcFrame_entry.grid(row=2, column=1, padx=2, pady=3, sticky='')
        frame_label.grid(row=3, column=0, padx=2, pady=2, sticky='')
        self.frameCalMenu_entry.grid(row=3, column=1, padx=5, pady=5, sticky='')

        readAngles_button = Button(loftCal_frame, text="Read\nAngles", height=2, width=7, font='Arial 16 bold')
        zeroProtractor_button = Button(loftCal_frame, text="SET\nMC REF", height=2, width=7, font='Arial 16 bold')
        updateFrame_button = Button(loftCal_frame, text="Update\nFrame", height=2, width=7, font='Arial 16 bold')

        readAngles_button.grid(row=0, column=2, padx=10, pady=3, rowspan=2)
        zeroProtractor_button.grid(row=0, column=3, padx=10, pady=3, rowspan=2)
        updateFrame_button.grid(row=2, column=2, padx=10, pady=3, rowspan=2)

        # Exit Button
        saveExit_button = Button(bottom_frame, text="Save & Exit", height=3, width=15, font='Arial 16 bold')
        saveExit_button.grid(row=0, column=1, padx=25, pady=10)

        # Boundary Box & Tilt Limit Edit Buttons
        originXDwn_button = Button(boundBox_frame, text="-", height=2, width=4, font='Arial 12 bold',
                                   command=lambda: self.editScoreFilterValues(0, -1))
        originX_label = Label(boundBox_frame, text="Origin X", height=1, width=8, font='Arial 12 bold', bg='black',
                              fg='white')
        self.originX_entry = Entry(boundBox_frame, width=8, font='Arial 12 bold')
        originXUp_button = Button(boundBox_frame, text="+", height=2, width=4, font='Arial 12 bold',
                                  command=lambda: self.editScoreFilterValues(0, 1))

        originYDwn_button = Button(boundBox_frame, text="-", height=2, width=4, font='Arial 12 bold',
                                   command=lambda: self.editScoreFilterValues(1, -1))
        originY_label = Label(boundBox_frame, text="Origin Y", height=1, width=8, font='Arial 12 bold', bg='black',
                              fg='white')
        originYUp_button = Button(boundBox_frame, text="+", height=2, width=4, font='Arial 12 bold',
                                  command=lambda: self.editScoreFilterValues(1, 1))
        self.originY_entry = Entry(boundBox_frame, width=8, font='Arial 12 bold')

        boxWidthDwn_button = Button(boundBox_frame, text="-", height=2, width=4, font='Arial 12 bold',
                                    command=lambda: self.editScoreFilterValues(2, -1))
        boxWidth_label = Label(boundBox_frame, text="Width", height=1, width=8, font='Arial 12 bold', bg='black',
                               fg='white')
        self.boxWidth_entry = Entry(boundBox_frame, width=8, font='Arial 12 bold')
        boxWidthUp_button = Button(boundBox_frame, text="+", height=2, width=4, font='Arial 12 bold',
                                   command=lambda: self.editScoreFilterValues(2, 1))

        boxHeightDwn_button = Button(boundBox_frame, text="-", height=2, width=4, font='Arial 12 bold',
                                     command=lambda: self.editScoreFilterValues(3, -1))
        boxHeight_label = Label(boundBox_frame, text="Height", height=1, width=8, font='Arial 12 bold', bg='black',
                                fg='white')
        self.boxHeight_entry = Entry(boundBox_frame, width=8, font='Arial 12 bold')
        boxHeightUp_button = Button(boundBox_frame, text="+", height=2, width=4, font='Arial 12 bold',
                                    command=lambda: self.editScoreFilterValues(3, 1))

        tiltLimitDwn_button = Button(boundBox_frame, text="-", height=2, width=4, font='Arial 12 bold',
                                     command=lambda: self.editScoreFilterValues(4, -1))
        tiltLimit_label = Label(boundBox_frame, text="Tilt", height=1, width=8, font='Arial 12 bold', bg='black',
                                fg='white')
        self.tiltLimit_entry = Entry(boundBox_frame, width=8, font='Arial 12 bold')
        tiltLimitUp_button = Button(boundBox_frame, text="+", height=2, width=4, font='Arial 12 bold',
                                    command=lambda: self.editScoreFilterValues(4, 1))

        originZeroDwn_button = Button(boundBox_frame, text="-", height=2, width=4, font='Arial 12 bold',
                                      command=lambda: self.editScoreFilterValues(5, -1))
        originZero_label = Label(boundBox_frame, text="ZeroLine", height=1, width=8, font='Arial 12 bold', bg='black',
                                 fg='white')
        self.originZero_entry = Entry(boundBox_frame, width=8, font='Arial 12 bold')
        originZeroUp_button = Button(boundBox_frame, text="+", height=2, width=4, font='Arial 12 bold',
                                     command=lambda: self.editScoreFilterValues(5, 1))

        originXDwn_button.grid(row=2, column=0, padx=5, pady=2, sticky=W, rowspan=2)
        originX_label.grid(row=2, column=1, padx=5, pady=2, sticky=W)
        self.originX_entry.grid(row=3, column=1, padx=5, pady=2, sticky=W)
        originXUp_button.grid(row=2, column=2, padx=5, pady=2, sticky=W, rowspan=2)

        originYDwn_button.grid(row=4, column=0, padx=5, pady=2, sticky=W, rowspan=2)
        originY_label.grid(row=4, column=1, padx=5, pady=2, sticky=W)
        self.originY_entry.grid(row=5, column=1, padx=5, pady=2, sticky=W)
        originYUp_button.grid(row=4, column=2, padx=5, pady=2, sticky=W, rowspan=2)

        boxWidthDwn_button.grid(row=2, column=3, padx=5, pady=2, sticky=W, rowspan=2)
        boxWidth_label.grid(row=2, column=4, padx=5, pady=2, sticky=W)
        self.boxWidth_entry.grid(row=3, column=4, padx=5, pady=2, sticky=W)
        boxWidthUp_button.grid(row=2, column=5, padx=5, pady=2, sticky=W, rowspan=2)

        boxHeightDwn_button.grid(row=4, column=3, padx=5, pady=2, sticky=W, rowspan=2)
        boxHeight_label.grid(row=4, column=4, padx=5, pady=2, sticky=W)
        self.boxHeight_entry.grid(row=5, column=4, padx=5, pady=2, sticky=W)
        boxHeightUp_button.grid(row=4, column=5, padx=5, pady=2, sticky=W, rowspan=2)

        tiltLimitDwn_button.grid(row=2, column=6, padx=5, pady=2, sticky=W, rowspan=2)
        tiltLimit_label.grid(row=2, column=7, padx=5, pady=2, sticky=W)
        self.tiltLimit_entry.grid(row=3, column=7, padx=5, pady=2, sticky=W)
        tiltLimitUp_button.grid(row=2, column=8, padx=5, pady=2, sticky=W, rowspan=2)

        originZeroDwn_button.grid(row=4, column=6, padx=5, pady=2, sticky=W, rowspan=2)
        originZero_label.grid(row=4, column=7, padx=5, pady=2, sticky=W)
        self.originZero_entry.grid(row=5, column=7, padx=5, pady=2, sticky=W)
        originZeroUp_button.grid(row=4, column=8, padx=5, pady=2, sticky=W, rowspan=2)

        # Button Commands
        stream_button.config(
            command=lambda c=canvas, of=self.calOffset_entry, zr=self.zeroLine_entry: self.vidStreamStart(c, offset=of,
                                                                                                          zero=zr,
                                                                                                          box=True))
        capture_button.config(
            command=lambda c=canvas, of=self.calOffset_entry, zr=self.zeroLine_entry: self.captureImg(c, offset=of,
                                                                                                      zero=zr))
        brightUp_button.config(command=lambda v='+': self.brightnessAdjust(v))
        brightDwn_button.config(command=lambda v='-': self.brightnessAdjust(v))
        frameDwn_button.config(command=lambda d='-', f=self.frameCalMenu_entry: self.motorRotate(d, f))
        frameUp_button.config(command=lambda d='+', f=self.frameCalMenu_entry: self.motorRotate(d, f))
        frameHome_button.config(command=self.seekHome)
        update_button.config(command=self.updateZeroLine)
        resetZeroLine_button.config(command=self.resetZeroLine)
        resetOffset_button.config(command=self.resetOffset)
        readAngles_button.config(command=lambda li=self.lieSys_entry, lo=self.loftSys_entry,
                                                fr=self.frameCalMenu_entry: self.readProtractorReportCalMenu(li, lo,
                                                                                                             fr))
        zeroProtractor_button.config(
            command=lambda li=self.lieSys_entry, lo=self.loftSys_entry, fr=self.frameCalMenu_entry: self.setMCREF(li,
                                                                                                                  lo,
                                                                                                                  fr))
        updateFrame_button.config(command=self.updateFrameVal)
        saveExit_button.config(command=lambda m=self.master: self.exitMenu(m))

        # Entering Default Values
        self.originX_entry.delete(0, END)
        self.originX_entry.insert(0, self.BullsEye.scoreFilterSettings[0])
        self.originY_entry.delete(0, END)
        self.originY_entry.insert(0, self.BullsEye.scoreFilterSettings[1])
        self.boxWidth_entry.delete(0, END)
        self.boxWidth_entry.insert(0, self.BullsEye.scoreFilterSettings[2])
        self.boxHeight_entry.delete(0, END)
        self.boxHeight_entry.insert(0, self.BullsEye.scoreFilterSettings[3])
        self.tiltLimit_entry.delete(0, END)
        self.tiltLimit_entry.insert(0, self.BullsEye.scoreFilterSettings[4])
        self.originZero_entry.delete(0, END)
        self.originZero_entry.insert(0, self.BullsEye.scoreFilterSettings[5])
        self.calStickVal_entry.delete(0, END)
        self.calStickVal_entry.insert(0, self.BullsEye.calStickVal)
        self.lieOffset = 0
        self.frame.grid(row=0, column=0)

        self.vidStreamStart(canvas, offset = self.calOffset_entry , zero = self.zeroLine_entry, box=True)

    def updateZeroLine(self):
        # round(math.atan(self.BullsEye.avgScoreLineSlope) * (180 / math.pi), 1)
        self.BullsEye.zeroLineSlope = self.BullsEye.avgScoreLineSlope
        self.BullsEye.zeroLineAngle = round(math.atan(self.BullsEye.zeroLineSlope) * (180 / math.pi), 1)
        self.zeroLine_entry.delete(0, END)
        self.zeroLine_entry.insert(END, self.BullsEye.zeroLineAngle)

    def resetZeroLine(self):
        self.BullsEye.zeroLineSlope = 0
        self.BullsEye.zeroLineAngle = 0
        self.zeroLine_entry.delete(0, END)
        self.zeroLine_entry.insert(END, self.BullsEye.zeroLineAngle)

    def resetOffset(self):
        self.BullsEye.lieOffset = 0
        self.calOffset_entry.delete(0, END)
        self.calOffset_entry.insert(0, self.BullsEye.lieOffset)

    def editScoreFilterValues(self, spec, val):
        self.BullsEye.scoreFilterSettings[spec] = self.BullsEye.scoreFilterSettings[spec] + val
        self.updateScoreFilterValues()

    def updateScoreFilterValues(self):
        self.originX_entry.delete(0, END)
        self.originX_entry.insert(0, self.BullsEye.scoreFilterSettings[0])
        self.originY_entry.delete(0, END)
        self.originY_entry.insert(0, self.BullsEye.scoreFilterSettings[1])
        self.boxWidth_entry.delete(0, END)
        self.boxWidth_entry.insert(0, self.BullsEye.scoreFilterSettings[2])
        self.boxHeight_entry.delete(0, END)
        self.boxHeight_entry.insert(0, self.BullsEye.scoreFilterSettings[3])
        self.tiltLimit_entry.delete(0, END)
        self.tiltLimit_entry.insert(0, self.BullsEye.scoreFilterSettings[4])
        self.originZero_entry.delete(0, END)
        self.originZero_entry.insert(0, self.BullsEye.scoreFilterSettings[5])

    def resetScoreFilterValues(self):
        self.originX_entry.delete(0, END)
        self.originX_entry.insert(0, self.BullsEye.scoreFilterSettingsDefault[0])
        self.originY_entry.delete(0, END)
        self.originY_entry.insert(0, self.BullsEye.scoreFilterSettingsDefault[1])
        self.boxWidth_entry.delete(0, END)
        self.boxWidth_entry.insert(0, self.BullsEye.scoreFilterSettingsDefault[2])
        self.boxHeight_entry.delete(0, END)
        self.boxHeight_entry.insert(0, self.BullsEye.scoreFilterSettingsDefault[3])
        self.tiltLimit_entry.delete(0, END)
        self.tiltLimit_entry.insert(0, self.BullsEye.scoreFilterSettingsDefault[4])
        self.originZero_entry.delete(0, END)
        self.originZero_entry.insert(0, self.BullsEye.scoreFilterSettingsDefault[5])
        self.scoreFilterSettings = self.BullsEye.scoreFilterSettingsDefault[:]

    def calStickValChange(self, value):
        self.BullsEye.calStickVal = round(self.BullsEye.calStickVal + value, 1)
        self.calStickVal_entry.delete(0, END)
        self.calStickVal_entry.insert(0, self.BullsEye.calStickVal)

    def updateFrameVal(self):
        if self.BullsEye.servoController == None:
            return
        self.BullsEye.servoController.resetFrameCounter()  # reset servoController encoder count
        self.BullsEye.frameBase = self.BullsEye.calcFrame
        self.readProtractorReportCalMenu(self.lieSys_entry, self.loftSys_entry, self.frameCalMenu_entry)

    def readProtractorReportCalMenu(self, lieEntry, loftEntry, frameEntry):
        self.captureAngle(lieEntry, loftEntry, frameEntry)
        self.BullsEye.calcFrame = round(self.BullsEye.frame - (self.BullsEye.loftSys - self.BullsEye.calStickVal), 1)
        self.calcFrame_entry.delete(0, END)
        self.calcFrame_entry.insert(END, self.BullsEye.calcFrame)

    def updateInstructionsImage(self, dir):
        if len(self.instructionImages) == 0:
            return
        if dir == '>':
            self.instructionImgNo = self.instructionImgNo + 1
        elif dir == '<':
            self.instructionImgNo = self.instructionImgNo - 1
        if self.instructionImgNo < 0:
            self.instructionImgNo = len(self.instructionImages) - 1
        if self.instructionImgNo > (len(self.instructionImages) - 1):
            self.instructionImgNo = 0
        self.instructions_label.configure(image=self.instructionImages[self.instructionImgNo])
