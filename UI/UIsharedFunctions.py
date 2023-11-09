import threading
from tkinter import *
from PIL import Image, ImageTk
import math


class sharedFunctions():
    def doNothing(self):
        pass

    def getImage(self, path, **kwargs):
        image = Image.open(path)
        if 'resize' in kwargs:
            image = image.resize(kwargs['resize'])
        width, height = image.size
        image = ImageTk.PhotoImage(image)
        return image

    # Draw Indicator Function
    def drawIndicator(self, canvas, lie, loft):
        canvas.delete('cross')
        canvas.delete('reading')
        x = 205 + (63.5 * loft * -1)
        y = 205 + (-63.5 * lie)
        if x > 364.5: x = 364.5
        if x < 45.5: x = 45.5
        if y < 45.5: y = 45.5
        if y > 364.5: y = 364.5
        text = "Lie: " + str(lie) + "   Loft: " + str(loft)
        canvas.create_line(x - 5, y - 5, x + 5, y + 5, fill='white', tags='cross', width=4)
        canvas.create_line(x - 5, y + 5, x + 5, y - 5, fill='white', tags='cross', width=4)
        canvas.create_text(10, 390, text="Puck", anchor='sw', fill='white', tags='reading')
        canvas.create_text(10, 405, text=text, anchor='sw', fill='white', tags='reading')

    # For Order mode protractor indicator
    def drawIndicator2(self, canvas, lie, loft):
        canvas.delete('cross2')
        canvas.delete('reading2')
        x = 205 + (63.5 * loft * -1)
        y = 205 + (-63.5 * lie)
        if x > 364.5: x = 364.5
        if x < 45.5: x = 45.5
        if y < 45.5: y = 45.5
        if y > 364.5: y = 364.5
        text = "Lie: " + str(lie) + "   Loft: " + str(loft)
        canvas.create_line(x - 5, y - 5, x + 5, y + 5, fill='black', tags='cross2', width=4)
        canvas.create_line(x - 5, y + 5, x + 5, y - 5, fill='black', tags='cross2', width=4)
        canvas.create_text(260, 390, text="Protractor", anchor='sw', fill='black', tags='reading2')
        canvas.create_text(260, 405, text=text, anchor='sw', fill='black', tags='reading2')

    def captureImg(self, canvas, **kwargs):
        if self.BullsEye.myCamera == None:
            self.msg('Camera not connected!')
            return
        camera = self.BullsEye.myCamera
        if self.BullsEye.vidStreamActive is True:
            self.BullsEye.vidStreamActive = False
            self.master.after(1000, self.doNothing)
        raw = camera.captureVport2()
        raw = camera.cropImage(raw)
        # raw2 = raw.copy()
        score_0 = camera.detectScore(raw , self.BullsEye.scoreFilterSettings[0:4])

        score_1 = camera.filterScoreBound(score_0, self.BullsEye.scoreFilterSettings[0:4])

        score_2, self.BullsEye.avgScoreLineSlope = camera.filterScoreSlope(score_1,
                                                                           self.BullsEye.scoreFilterSettings[4])
        self.BullsEye.lieOffset = round(
            math.atan(self.BullsEye.avgScoreLineSlope) * (180 / math.pi) - self.BullsEye.zeroLineAngle, 1)
        camera.scoreLineDraw(raw, score_0, [0, 0, 255])  # Draw scorelines
        camera.boundaryBoxDraw(raw, self.BullsEye.scoreFilterSettings[0:4], [255, 0, 255])
        camera.drawLine(raw, [320, self.BullsEye.scoreFilterSettings[5]], self.BullsEye.zeroLineSlope, [255, 255, 0])  # Draw zero line
        camera.drawLine(raw, [320, self.BullsEye.scoreFilterSettings[5]], self.BullsEye.avgScoreLineSlope, [255, 0, 0])  # Draw Avg Score Line
        # pack in one function

        if 'resize' in kwargs:
            raw = camera.resizeImage(raw, kwargs['resize'])

        tk_score = camera.cv2Tk(raw)
        # tk_raw = camera.cv2Tk(raw2)
        self.BullsEye.tk_score = tk_score
        # self.BullsEye.tk_raw = tk_raw

        if canvas:
            canvas.configure(image=self.BullsEye.tk_score)
            canvas.image = self.BullsEye.tk_score
        if 'offset' in kwargs:
            kwargs['offset'].delete(0, END)
            kwargs['offset'].insert(END, self.BullsEye.lieOffset)
        if 'zero' in kwargs:
            kwargs['zero'].delete(0, END)
            kwargs['zero'].insert(END, self.BullsEye.zeroLineAngle)

        kwargs['zero'] = self.BullsEye.zeroLineAngle

    def clearOffset(self, offsetField):
        self.BullsEye.lieOffset = 0.0
        if offsetField:
            offsetField.delete(0, END)
            offsetField.insert(END, self.BullsEye.lieOffset)

    def vidStreamStart(self, canvas, **kwargs):
        if self.BullsEye.myCamera == None:
            self.msg('Camera not connected!')
            return
        if self.BullsEye.vidStreamActive == True:
            return
        self.BullsEye.vidStreamActive = True
        self.vidStreamThread = threading.Thread(target=lambda cv=canvas: self.vidStream(cv, **kwargs))
        self.vidStreamThread.start()
        self.master.update_idletasks()

    def vidStream(self, canvas, **kwargs):
        camera = self.BullsEye.myCamera
        while self.BullsEye.vidStreamActive is True:
            raw = camera.captureVport2()
            raw = camera.cropImage(raw)
            score_0 = camera.detectScore(raw , self.BullsEye.scoreFilterSettings[0:4])
            score_1 = camera.filterScoreBound(score_0, self.BullsEye.scoreFilterSettings[0:4])

            score_2, self.BullsEye.avgScoreLineSlope = camera.filterScoreSlope(score_1,
                                                                               self.BullsEye.scoreFilterSettings[4])
            self.BullsEye.lieOffset = round(
                math.atan(self.BullsEye.avgScoreLineSlope) * (180 / math.pi) - self.BullsEye.zeroLineAngle, 1)

            if 'box' in kwargs:
                if kwargs['box']:
                    camera.boundaryBoxDraw(raw, self.BullsEye.scoreFilterSettings[0:4], [255, 0, 255])
            camera.scoreLineDraw(raw, score_2, [0, 0, 255])  # Draw scorelines
            camera.drawLine(raw, [320, self.BullsEye.scoreFilterSettings[5]], self.BullsEye.zeroLineSlope,
                            [255, 255, 0])
            camera.drawLine(raw, [320, self.BullsEye.scoreFilterSettings[5]], self.BullsEye.avgScoreLineSlope, [255, 0, 0])  # Draw Avg Score Line

            if 'offset' in kwargs:
                kwargs['offset'].delete(0, END)
                kwargs['offset'].insert(END, self.BullsEye.lieOffset)
            if 'zero' in kwargs:
                kwargs['zero'].delete(0, END)
                kwargs['zero'].insert(END, self.BullsEye.zeroLineAngle)

            image_tk = camera.cv2Tk(raw)
            canvas.configure(image=image_tk)
            canvas.image = image_tk
            self.master.update_idletasks()

    def showScore(self, canvas):
        if self.BullsEye.vidStreamActive == True:
            return
        canvas.configure(image=self.BullsEye.tk_score)
        canvas.image = self.BullsEye.tk_score

    def showRaw(self, canvas):
        if self.BullsEye.vidStreamActive == True:
            return
        canvas.configure(image=self.BullsEye.tk_raw)
        canvas.image = self.BullsEye.tk_raw

    def btStreamStart(self, mainEntryTuple, **kwargs):
        # mainEntryTuple: (Loft, Lie, Heading)
        if self.BullsEye.mbtModule == None:
            self.btConFailMsg()
            return
        # toggle=tkinter_button. If stream active, turn off switch and toggle button
        if 'toggle' in kwargs:
            kwargs['toggle'].config(text='Stream\nEnd')
            kwargs['toggle'].config(command=lambda: self.btStreamEnd(mainEntryTuple, **kwargs))
        if 'angleStreamButton' in kwargs:
            kwargs['angleStreamButton'].configure(state='disabled')
        for entry in mainEntryTuple:
            entry.configure(bg='green')
        self.BullsEye.mbtModule.sensorFusionStart()
        self.BullsEye.btStreamActive = True
        streamThread = threading.Thread(target=lambda e=mainEntryTuple: self.btStream(e, **kwargs))
        streamThread.start()
        self.master.update_idletasks()

    def btStream(self, mainEntryTuple, **kwargs):
        # mainEntryTuple: Loft, Lie, Heading (Tkinter Entry Object)
        # diffEntry: Loft, Lie (Tkinter Entry Object
        loftEntry, lieEntry, headEntry = mainEntryTuple[0], mainEntryTuple[1], mainEntryTuple[2]
        c = 0
        while self.BullsEye.btStreamActive == True:
            frameEncoderCount = self.BullsEye.servoController.getFrame()
            self.BullsEye.frame = round(self.BullsEye.frameBase - float(frameEncoderCount.strip()), 1)
            head, pitch, roll, yaw = self.BullsEye.mbtModule.dataReturn()

            btHeading = round(head, 1)
            self.btLoftRaw = roll * -1
            if self.dex.get() == 0:  # RH
                self.btLieRaw = pitch
            elif self.dex.get() == 1:  # LH
                self.btLieRaw = -pitch

            btLoftComped = round(self.BullsEye.frame - (self.btLoftRaw + self.BullsEye.btLoftCompVal), 1)
            btLieComped = round(self.btLieRaw + self.BullsEye.btLieCompVal + 90, 1)

            diffLoft = round(btLoftComped - self.BullsEye.targetLoft, 1)
            diffLie = round(btLieComped - self.BullsEye.targetLie, 1)

            if 'indicator' in kwargs:
                self.drawIndicator(kwargs['indicator'], diffLie, diffLoft)

            if c > 5:
                loftEntry.delete(0, END)
                lieEntry.delete(0, END)
                headEntry.delete(0, END)
                loftEntry.insert(END, btLoftComped)
                lieEntry.insert(END, btLieComped)
                headEntry.insert(END, btHeading)
                if btHeading > 0.5 and btHeading < 359.5:
                    headEntry.config(bg='red')
                else:
                    headEntry.config(bg='green')

                if 'diffEntry' in kwargs:
                    diffLoftEntry, diffLieEntry = kwargs['diffEntry'][0], kwargs['diffEntry'][1]

                    diffLoftEntry.delete(0, END)
                    diffLieEntry.delete(0, END)
                    diffLoftEntry.insert(END, diffLoft)
                    diffLieEntry.insert(END, diffLie)

                    if abs(diffLoft) < 0.5:
                        diffLoftEntry.config(bg='Green')
                    else:
                        diffLoftEntry.config(bg='White')
                    if abs(diffLie) < 0.5:
                        diffLieEntry.config(bg='Green')
                    else:
                        diffLieEntry.config(bg='White')

                if 'frameEntry' in kwargs:
                    kwargs['frameEntry'].delete(0, END)
                    kwargs['frameEntry'].insert(END, self.BullsEye.frame)

                c = 0
            c = c + 1
            self.master.update_idletasks()

    def btTareToProtractor(self):
        if self.BullsEye.mbtModule == None:
            self.msg('BT Accelerometer not connected!')
            return
        self.BullsEye.mbtModule.tareDevice()
        self.BullsEye.btLoftCompVal = round(self.BullsEye.loftSys - self.btLoftRaw, 2)
        self.BullsEye.btLieCompVal = round(self.BullsEye.lieSys - self.btLieRaw, 2)

    def btTareToZero(self):
        if self.BullsEye.mbtModule == None:
            self.msg('BT Accelerometer not connected!')
            return
        self.master.after(3000, self.doNothing)
        self.master.after(100, self.updateCompVal)
        self.master.after(100, self.BullsEye.mbtModule.tareDevice())

    def updateCompVal(self):
        self.BullsEye.btLoftCompVal = self.btLoftRaw * -1
        self.BullsEye.btLieCompVal = self.btLieRaw * -1

    def btStreamEnd(self, mainEntryTuple, **kwargs):
        self.BullsEye.btStreamActive = False
        for entry in mainEntryTuple:
            entry.configure(bg='white')
        if 'toggle' in kwargs:
            kwargs['toggle'].config(text='Stream\nStart')
            kwargs['toggle'].config(command=lambda: self.btStreamStart(mainEntryTuple, **kwargs))
        if 'angleStreamButton' in kwargs:
            kwargs['angleStreamButton'].configure(state='normal')

    def readProtractor(self):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return

        temp_loft = self.BullsEye.servoController.getLoft()  # Get Loft
        self.BullsEye.loftPro = round(float(temp_loft.strip()), 1)
        self.BullsEye.loftSys = round(self.BullsEye.loftPro + self.BullsEye.frame - 15, 1)

        temp_lie = self.BullsEye.servoController.getLie()  # Get Lie
        self.BullsEye.liePro = round(float(temp_lie.strip()), 1)
        if (self.BullsEye.liePro < 0):
            # LH
            self.BullsEye.lieSys = round(90 + self.BullsEye.liePro - self.BullsEye.lieOffset, 1)
        else:
            # RH
            self.BullsEye.lieSys = round(90 - self.BullsEye.liePro + self.BullsEye.lieOffset, 1)

        frameEncoderCount = self.BullsEye.servoController.getFrame()
        self.BullsEye.frame = round(self.BullsEye.frameBase - float(frameEncoderCount.strip()), 1)

    def readProtractorReport(self, lieEntry, loftEntry, frameEntry, **kwargs):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return
        self.readProtractor()
        lieEntry.delete(0, END)
        lieEntry.insert(END, self.BullsEye.lieSys)
        loftEntry.delete(0, END)
        loftEntry.insert(END, self.BullsEye.loftSys)
        frameEntry.delete(0, END)
        frameEntry.insert(END, self.BullsEye.frame)
        if 'diff' in kwargs:
            diffLie = round(self.BullsEye.lieSys - self.BullsEye.targetLie, 1)
            diffLoft = round(self.BullsEye.loftSys - self.BullsEye.targetLoft, 1)
            kwargs['diff'][0].delete(0, END)
            kwargs['diff'][1].delete(0, END)
            kwargs['diff'][0].insert(END, diffLie)
            kwargs['diff'][1].insert(END, diffLoft)
            if diffLie < 0.5 and diffLie > -0.5:
                kwargs['diff'][0].configure(bg='green')
            else:
                kwargs['diff'][0].configure(bg='white')
            if diffLoft < 0.5 and diffLoft > -0.5:
                kwargs['diff'][1].configure(bg='green')
            else:
                kwargs['diff'][1].configure(bg='white')
        if 'indicator' in kwargs:
            self.drawIndicator2(kwargs['indicator'], diffLie, diffLoft)

    def captureAngle(self, lieEntry, loftEntry, frameEntry, **kwargs):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return
        if 'toggle' in kwargs:
            kwargs['toggle'].configure(command=lambda: self.angleStreamStart(lieEntry, loftEntry, frameEntry, **kwargs))
            kwargs['toggle'].configure(text='Stream\nStart')
        if 'btStreamButton' in kwargs:
            kwargs['btStreamButton'].configure(state='normal')
        if self.BullsEye.angleStreamActive is True:
            self.BullsEye.angleStreamActive = False
            lieEntry.configure(bg='white')
            loftEntry.configure(bg='white')
            frameEntry.configure(bg='white')
            return
        self.readProtractorReport(lieEntry, loftEntry, frameEntry, **kwargs)

    def readFrame(self, frameEntry):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return
        frameEncoderCount = self.BullsEye.servoController.getFrame()
        self.BullsEye.frame = round(self.BullsEye.frameBase - float(frameEncoderCount.strip()), 1)
        frameEntry.delete(0, END)
        frameEntry.insert(END, self.BullsEye.frame)

    def angleStreamStart(self, lieEntry, loftEntry, frameEntry, **kwargs):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return
        if self.BullsEye.angleStreamActive == True:
            return
        if 'btStreamButton' in kwargs:
            kwargs['btStreamButton'].configure(state='disabled')
        if 'toggle' in kwargs:
            kwargs['toggle'].configure(text="Capture")
            kwargs['toggle'].configure(command=lambda: self.captureAngle(lieEntry, loftEntry, frameEntry, **kwargs))
        self.BullsEye.angleStreamActive = True
        streamThread = threading.Thread(target=lambda: self.angleStream(lieEntry, loftEntry, frameEntry, **kwargs))
        streamThread.start()
        self.master.update_idletasks()

    def angleStream(self, lieEntry, loftEntry, frameEntry, **kwargs):
        lieEntry.config(bg='green')
        loftEntry.config(bg='green')
        frameEntry.config(bg='green')
        while self.BullsEye.angleStreamActive == True:
            self.readProtractorReport(lieEntry, loftEntry, frameEntry, **kwargs)
            self.master.update_idletasks()
        lieEntry.config(bg='white')
        loftEntry.config(bg='white')
        frameEntry.config(bg='white')

    def angleStreamEnd(self):
        self.BullsEye.angleStreamActive = False

    def setMCREF(self, lieEntry, loftEntry, frameEntry):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return
        self.BullsEye.servoController.setMCREF()
        if self.BullsEye.angleStreamActive == False:
            self.readProtractorReport(lieEntry, loftEntry, frameEntry)

    def enableMotorControls(self, permissionButton, servoButtonsList, disableButtonsList):
        # pass in buttons as a tuple: (buttn1, buttn2, buttn3)
        if self.BullsEye.angleStreamActive:
            self.msg("Disable Angle Stream First!")
            return
        if self.BullsEye.btStreamActive:
            self.msg("Disable BT Stream First!")
            return
        permissionButton.config(text='Disable',
                                command=lambda a=0: self.disableMotorControls(permissionButton, servoButtonsList,
                                                                              disableButtonsList))
        for widget in servoButtonsList:
            widget.config(state='normal')
        for widget in disableButtonsList:
            widget.config(state='disabled')

    def disableMotorControls(self, permissionButton, servoButtonsList, disableButtonsList):
        permissionButton.config(text='Enable',
                                command=lambda a=0: self.enableMotorControls(permissionButton, servoButtonsList,
                                                                             disableButtonsList))
        for widget in servoButtonsList:
            widget.config(state='disabled')
        for widget in disableButtonsList:
            widget.config(state='normal')

    def seekAngleValue(self, seekValue, frameEntry, **kwargs):
        # seekValue is a float value by default
        # If seekValue is input as an entry instead, add 'isEntry = True'
        if 'isEntry' in kwargs:
            if kwargs['isEntry']:
                temp = seekValue.get()
                seekValue.delete(0, END)
                seekValue = temp
        try:
            seekValue = round(float(seekValue), 1)
        except:
            self.msg('Seek Value Invalid!')
            return
        if seekValue > 65 or seekValue < 9:
            self.msg('Seek Value Out of Range \n Valid Range: 9*~65*')
            return
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return

        diff = self.BullsEye.frame - seekValue
        self.msg("Servo Running")
        # self.seekAngleWrapper(diff, frameEntry)
        self.master.after(200, lambda: self.seekAngleWrapper(diff, frameEntry))

    def seekAngleWrapper(self, diff, frameEntry):
        result = self.BullsEye.servoController.seekAngle(diff)
        self.popup.destroy()
        if result == 1: pass
        if result == -1: self.msg("Limit Reached!")
        if result == -2: self.msg("Serial timeout, please reboot")
        if result == -3: self.frameLockEngagedMsg(diff, frameEntry)
        if result == -4: self.msg("Frame Lock Engaged!")
        self.master.after(200, lambda f=frameEntry: self.readFrame(f))
        # if result == -3: self.msg("Frame Lock Engaged!\nUnlock and retry!")

    def frameLockEngagedMsg(self, diff, frameEntry):
        if hasattr(self, 'popup'):
            self.popup.destroy()
        self.popup = Toplevel(height=200, width=430)
        self.popup.wm_title("Frame Lock Engaged!")
        self.popup.geometry('+300+300')
        self.popup.grid_propagate(0)
        self.popup.wait_visibility()
        self.popup.grab_set_global()
        self.master.after(500, self.popup.focus_force())
        messageLabel = Label(self.popup, text="Frame lock engaged, unlock and retry!", font='Arial 22', wraplength=400,
                             justify=CENTER)
        cancelButton = Button(self.popup, text='Cancel', font='Arial 22', command=self.popup.destroy)
        retryButton = Button(self.popup, text='Retry', font='Arial 22',
                             command=lambda: self.master.after(1000, self.seekAngleWrapper(diff, frameEntry)))
        messageLabel.grid(row=0, column=0, columnspan=2, pady=20, padx=30)
        retryButton.grid(row=1, column=0)
        cancelButton.grid(row=1, column=1)

    def seekHome(self):
        self.msg("Servo Running")
        self.master.after(100, lambda: self.seekHomeWrapper())

    def seekHomeWrapper(self):
        result = self.BullsEye.servoController.seekHome()
        self.popup.destroy()
        if result == 1: return
        if result == -2: self.msg("Timed Out!")
        if result == -3: self.msg("Lock Engaged! Unlock and Retry")

    def motorRotate(self, direction, frameEntry):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return
        self.BullsEye.AngleStreamActive = False
        if direction == '-':
            self.BullsEye.servoController.servoWeak()
        elif direction == '+':
            self.BullsEye.servoController.servoStrong()
        self.readFrame(frameEntry)

    def toggleHoldOff(self, button):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return
        self.BullsEye.servoController.autoHoldOff()
        button.config(text="H.On", command=lambda b=button: self.toggleHoldOn(b))

    def toggleHoldOn(self, button):
        self.BullsEye.servoController.autoHoldOn()
        button.config(text="H.Off", command=lambda b=button: self.toggleHoldOff(b))

    def brightnessAdjust(self, val):
        if self.BullsEye.servoController == None:
            self.msg('Servo Controler Not Connected!')
            return
        if val == '+':
            self.BullsEye.servoController.brightUp()
        elif val == '-':
            self.BullsEye.servoController.brightDwn()

    def exitMenu(self, toplevel):
        self.BullsEye.btStreamActive = False
        self.BullsEye.angleStreamActive = False
        self.BullsEye.vidStreamActive = False
        self.BullsEye.updateScoreSettingFile()
        toplevel.destroy()

    def keyBoardInput(self, entry, char, **kwargs):
        if char == '!':
            entry.delete(0, END)
            return

        if 'limit' in kwargs:
            limit = kwargs['limit']
            if limit:
                if len(entry.get()) < limit:
                    entry.insert(END, char)
                return
        entry.insert(END, char)

    def msg(self, message, **kwargs):
        if hasattr(self, 'popup'):
            self.popup.destroy()
        self.popup = Toplevel(height=100, width=300)
        if 'title' in kwargs: self.popup.wm_title(kwargs['title'])
        self.popup.geometry('+300+300')
        self.popup.pack_propagate(0)
        self.popup.wait_visibility()
        self.popup.grab_set_global()
        self.popup.focus_force()
        myMessage = Label(self.popup, text=message, font='Arial 14')
        okButton = Button(self.popup, text='OK', font='Arial 14', command=self.popup.destroy)
        myMessage.pack(side=TOP)
        okButton.pack(side=BOTTOM)
        if 'title' in kwargs: self.popup.wm_title(kwargs['title'])

    def btConFailMsg(self):
        if hasattr(self, 'popup'):
            self.popup.destroy()
        self.popup = Toplevel(height=300, width=300)
        self.popup.geometry('+300+300')
        self.popup.wait_visibility()
        self.popup.grab_set_global()
        msg = 'BT device not detected!\nConnect to default address:\n' + self.BullsEye.btAddressDefault + ' ?'
        msgLabel = Label(self.popup, text=msg, font='Arial 12 bold')
        conDefault_button = Button(self.popup, text="Connect Default", font='Arial 12 bold',
                                   command=lambda adr=self.BullsEye.btAddressDefault: self.connectBtDevice(adr))
        btMenu_button = Button(self.popup, text='BT Menu', font='Arial 12 bold', command=self.createBTMenu)
        cancel_button = Button(self.popup, text='Cancel', font='Arial 12 bold', command=self.popup.destroy)

        msgLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        conDefault_button.grid(row=1, column=0, pady=10, padx=5)
        btMenu_button.grid(row=1, column=1, pady=10, padx=5)
        cancel_button.grid(row=1, column=2, pady=10, padx=5)

    def createBTMenu(self):
        self.BTmenu = Toplevel()
        self.BTmenu.attributes("-fullscreen", True)
        UI_btConfigMode.btConfigMode(self.BTmenu, self.BullsEye)
        self.popup.destroy()

    def connectBtDevice(self, address):
        if self.BullsEye.mbtModule != None:
            if address == self.BullsEye.mbtModule.address:
                self.msg('Already Connected to address...')
                return
            self.BullsEye.mbtModule.sensorFusionStop()
            self.BullsEye.mbtModule.disconnectDevice()
            self.BullsEye.mbtModule = None
        state = self.BullsEye.connectBT(address)
        if state == 0:
            txt = 'Connection Failed'
            currDevMsg = 'Connected to ' + str(self.BullsEye.mbtModule)
            self.msg(txt + '\n' + currDevMsg)
        elif state == 1:
            txt = 'Connection Successful!'
            currDevMsg = 'Connected to ' + str(self.BullsEye.mbtModule)
            self.msg(txt + '\n' + currDevMsg)


from UI import UI_btConfigMode
from UI import UI_calibrationMode
from UI import UI_guidedMode
from UI import UI_freeMode
