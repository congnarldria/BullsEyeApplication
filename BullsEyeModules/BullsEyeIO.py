from mbientlab.metawear import *
from mbientlab.metawear.cbindings import *
from mbientlab.warble import *
from time import sleep
from tkinter import *
from picamera import *
from picamera.array import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import math
import os
import serial


######################################################################################################################
# Notes                                                                                                               #
######################################################################################################################
# There are a total of 4 different image file formats
# When editing the code, must be careful of which format the variable is being stored as
# PiRGBArray: This is the format used by the camera for capturing photos.
#            Denoted as rawCapture
# Numpy Array: This is done by converting PiRGBArray to a Numpy array by using the tag .array.
#             This format is needed for the OpenCV methods to work properly.
#             Denoted as "_cv":  raw_cv, img_cv, crop_cv etc...
# Image File: Intermediary format, used when converting Numpy to Tkinter compatable image format
#            denoted as "_img". Only used in certain function for conversion
# Tkinter Compatable Image: This photo format can be displayed in Tkinter.
#            Variables that hold this image format must be declared globally so that the data does not get TRASHED
#            denoted as "_tk": raw_tk, crop_tk, score_tk etc...
######################################################################################################################

class rpiCam():
    def __init__(self):
        try:
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
            self.camera.framerate = 40
            self.tk_raw = None
            self.tk_score = None
        except :
            print("Error open camera")
    def captureStill(self):  # returns in openCV image format
        rawCapture = PiRGBArray(camera, size=(640, 480))
        self.camera.capture(rawCapture, format='bgr')
        raw_cv = rawCapture.array
        return raw_cv

    # Captures a still image using the video port
    # This makes the image lower res for faster loading time
    # Returns in cv array format
    # use cv2Tk function to make image compatible with tkinter canvas
    def captureVport2(self):
        rawCapture = PiRGBArray(camera, size=(640, 480))
        self.camera.capture(rawCapture, format='bgr', use_video_port=True)
        raw_cv = rawCapture.array
        rawCapture.truncate(0)
        return raw_cv

    def cropImage(self, raw_cv):
        imgCrop_cv = raw_cv[180:480, 70:570]  # [Height , Width]
        return imgCrop_cv

    def resizeImage(self, raw_cv, dim):
        imgResized_cv = cv2.resize(raw_cv, dim)
        return imgResized_cv

    # captureVport() needs an empty PiRGBArray as an input!!
    # Used for streaming video. Uses lower-res capture for faster stream speed
    def captureVport(self, rawArray):
        self.camera.capture(rawArray, format="bgr", use_video_port=True)
        return rawArray

    def cv2Tk(self, raw_cv):
        raw_img = Image.fromarray(raw_cv)
        raw_Tk = ImageTk.PhotoImage(image=raw_img)
        return raw_Tk

    def detectScore(self, raw_cv, scoreFilterSettings=[110, 50, 260, 255]):
        img = raw_cv
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Try morphlogy Closing to avoid shawfow effect
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
        dilate = cv2.dilate(gray, kernel)
        gray = cv2.erode(dilate, kernel)
        # ksize = (3, 3)
        # blur = cv2.blur(closing, ksize)
        # gray = cv2.imwrite("close.jpg", blur)
        # end==========================================
        crop_img = gray[scoreFilterSettings[1]:scoreFilterSettings[1] + scoreFilterSettings[3]
        , scoreFilterSettings[0]:scoreFilterSettings[0] + scoreFilterSettings[2]]
        edge = cv2.Canny(crop_img, 75, 150)
        scorelines = cv2.HoughLinesP(edge, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=50)
        count = 0
        if scorelines is None:
            return []
        for lines in scorelines:
            scorelines[count][0][0] += scoreFilterSettings[0]
            scorelines[count][0][1] += scoreFilterSettings[1]
            scorelines[count][0][2] += scoreFilterSettings[0]
            scorelines[count][0][3] += scoreFilterSettings[1]
            count += 1
        return scorelines

    def filterScoreBound(self, scorelines, box):
        scoreInBound = []
        if scorelines is not None:
            for i in range(0, len(scorelines)):
                x1 = scorelines[i][0][0]
                y1 = scorelines[i][0][1]
                x2 = scorelines[i][0][2]
                y2 = scorelines[i][0][3]
                xc = (x1 + x2) / 2
                yc = (y1 + y2) / 2
                if box[0] < xc < box[0] + box[2] and box[1] < yc < box[1] + box[3]:
                    scoreInBound.append(
                        [[scorelines[i][0][0], scorelines[i][0][1], scorelines[i][0][2], scorelines[i][0][3]]])
        return scoreInBound

    def filterScoreSlope(self, scorelines, cutOffAngle):
        cutOffSlope_0 = math.tan(cutOffAngle * (math.pi / 180))
        cutOffSlope_1 = cutOffSlope_0 * -1
        scoreInSlope = []
        slopeAVG = 0
        min = 99999
        max = -99999
        minId = -1
        maxId = -1
        count = 0
        if scorelines is not None:
            for i in range(0, len(scorelines)):
                x1 = scorelines[i][0][0]
                y1 = scorelines[i][0][1]
                x2 = scorelines[i][0][2]
                y2 = scorelines[i][0][3]
                slope = 0
                if x2 - x1 != 0:
                    slope = (y2 - y1) / (x2 - x1)
                if cutOffSlope_0 > slope > cutOffSlope_1:
                    scoreInSlope.append(
                        [[scorelines[i][0][0], scorelines[i][0][1], scorelines[i][0][2], scorelines[i][0][3]]])
                    if slope > max:
                        max = slope
                        maxId = count
                    if slope < min:
                        min = slope
                        minId = count
                    count += 1
        # Remove Max and min
        if len(scoreInSlope) >= 3:
            if minId == maxId or minId == -1 or maxId == -1:
                pass
            elif minId > maxId:
                del scoreInSlope[minId]
                del scoreInSlope[maxId]
            else:
                del scoreInSlope[maxId]
                del scoreInSlope[minId]
        if scoreInSlope is not None:
            for i in range(0, len(scoreInSlope)):
                x1 = scoreInSlope[i][0][0]
                y1 = scoreInSlope[i][0][1]
                x2 = scoreInSlope[i][0][2]
                y2 = scoreInSlope[i][0][3]
                slope = 0
                if x2 - x1 != 0:
                    slope = (y2 - y1) / (x2 - x1)
                slopeAVG = slopeAVG + slope
        if len(scoreInSlope) != 0:
            slopeAVG = slopeAVG / len(scoreInSlope)
        return scoreInSlope, slopeAVG

    def boundaryBoxDraw(self, raw_cv, box, color):
        cv2.line(raw_cv, (box[0], box[1]), (box[0] + box[2], box[1]), color, 2)
        cv2.line(raw_cv, (box[0], box[1] + box[3]), (box[0] + box[2], box[1] + box[3]), color, 2)
        cv2.line(raw_cv, (box[0], box[1]), (box[0], box[1] + box[3]), color, 2)
        cv2.line(raw_cv, (box[0] + box[2], box[1]), (box[0] + box[2], box[1] + box[3]), color, 2)
        imgBox = Image.fromarray(raw_cv)
        return ImageTk.PhotoImage(image=imgBox)

    def scoreLineDraw(self, raw_cv, scorelines, color):  # Color as an array eg: [255, 255, 255]
        if scorelines is not None:
            for i in range(0, len(scorelines)):
                x1 = scorelines[i][0][0]
                y1 = scorelines[i][0][1]
                x2 = scorelines[i][0][2]
                y2 = scorelines[i][0][3]
                cv2.line(raw_cv, (x1, y1), (x2, y2), (color[0], color[1], color[2]), 2)
                cv2.circle(raw_cv, (x1, y1), 2, (255, 255, 255), 0)
                cv2.circle(raw_cv, (x2, y2), 2, (255, 255, 255), 0)
        imgScore = Image.fromarray(raw_cv)
        return ImageTk.PhotoImage(image=imgScore)

    def drawLine(self, raw_cv, origin, slope, color):
        img_cv = raw_cv
        ox = int(origin[0])
        oy = int(origin[1])
        x2 = int(origin[0] + 500)  # All values = 300
        y2 = int(origin[1] + 500 * slope)
        x3 = int(origin[0] - 500)
        y3 = int(origin[1] - 500 * slope)
        cv2.line(img_cv, (ox, oy), (x2, y2), (color), 2)
        cv2.line(img_cv, (ox, oy), (x3, y3), (color), 2)
        imgLine = Image.fromarray(img_cv)
        return ImageTk.PhotoImage(image=imgLine)

    def DrawAll(self):
        pass

    def getImage(self, filePath):
        image = Image.open(filePath)
        image_Tk = ImageTk.PhotoImage(image)
        return image_Tk


# Settng up debug UI for Module
class Window(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.myCamera = rpiCam()
        self.boundBox = [210, 240, 200, 230]
        self.tiltLimit = 10  # In degrees!
        self.zeroLine = [0, 220, 1, 220]
        self.origin = [320, 330]
        self.init_window()
        self.captureImg()

    def init_window(self):
        self.master.title("Camera Module")
        self.master.grid_propagate(0)
        self.master.configure(height=600, width=650)
        # Frames
        canvas_frame = Frame(self.master, height=480, width=640, bg='white')
        canvas_frame.grid_propagate(0)
        controls_frame = Frame(self.master, height=100, width=640, relief='ridge')
        # Image Canvas
        self.canvas = Label(canvas_frame, bg='white')
        self.canvas.grid(row=0, column=0)
        # Controls
        capture_button = Button(controls_frame, width=6, height=2, text="Capture", font='Arial 18 bold',
                                command=self.captureImg)
        capture_button.grid(row=0, column=0, padx=5, pady=5, sticky=NW)
        # Inserting Frames
        canvas_frame.grid(row=0, column=0, padx=5, pady=5, sticky='')
        controls_frame.grid(row=1, column=0, padx=5, pady=5, sticky='')

    def captureImg(self):
        self.raw = self.myCamera.captureStill()
        score_0 = self.myCamera.detectScore(self.raw)
        score_1 = self.myCamera.filterScoreBound(score_0, self.boundBox)
        score_2, self.avgSlope = self.myCamera.filterScoreSlope(score_1, self.tiltLimit)
        self.offset = math.atan(self.avgSlope) * (180 / math.pi)
        self.tk_avgLine = self.myCamera.drawLine(self.raw, self.origin, self.avgSlope, [255, 220, 45])
        self.tk_zeroLine = self.myCamera.drawLine(self.raw, self.origin, 0, [120, 200, 45])
        self.tk_box = self.myCamera.boundaryBoxDraw(self.raw, self.boundBox, [255, 122, 122])
        self.tk_scoreRaw = self.myCamera.scoreLineDraw(self.raw, score_0, [255, 0, 255])  # Purple = Box Filter Fail
        self.tk_scoreBound = self.myCamera.scoreLineDraw(self.raw, score_1,
                                                         [0, 0, 255])  # Blue = Box Filter Pass, Tilt Filter Fail
        self.tk_scoreTilt = self.myCamera.scoreLineDraw(self.raw, score_2,
                                                        [255, 0, 0])  # Red = Box Filter + Tilt Filter Pass
        self.canvas.configure(image=self.tk_scoreTilt)
        self.canvas.image = self.tk_scoreTilt
        print("Detected: ", len(score_0), "\n")
        print("Bound Filter: ", len(score_1), "\n")
        print("Tilt Filter: ", len(score_2), "\n")
        print("Avg Slope: ", self.avgSlope, "\n")
        print("Offset: ", self.offset)


# Class for mbient bluetooth device
class State:
    def __init__(self, address):
        self.address = address
        self.device = MetaWear(address)
        self.device.connect()
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.heading = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.sensorFusionActive = False

    def data_handler(self, ctx, data):
        rawData = str(parse_value(data))
        split = rawData.split(" ")
        self.heading = split[2].strip(",")
        self.pitch = split[5].strip(",")
        self.roll = split[8].strip(",")
        self.yaw = split[11].strip("}")
        # SensorFusion EulerAngle data return format
        # {heading : 285.805, pitch : -178.317, roll : 2.243, yaw : 285.805}

    def dataReturn(self):
        self.heading = float(self.heading)
        self.pitch = float(self.pitch)
        self.roll = float(self.roll)
        self.yaw = float(self.yaw)
        return (self.heading, self.pitch, self.roll, self.yaw)

    def sensorFusionStart(self):
        if self.sensorFusionActive:
            return
        libmetawear.mbl_mw_settings_set_connection_parameters(self.device.board, 7.5, 7.5, 0, 6000)
        libmetawear.mbl_mw_sensor_fusion_set_mode(self.device.board, SensorFusionMode.IMU_PLUS)  # IMU_PLUS or NDOF
        libmetawear.mbl_mw_sensor_fusion_set_acc_range(self.device.board, SensorFusionAccRange._4G)
        libmetawear.mbl_mw_sensor_fusion_set_gyro_range(self.device.board, SensorFusionGyroRange._2000DPS)
        libmetawear.mbl_mw_sensor_fusion_write_config(self.device.board)
        signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.device.board, SensorFusionData.EULER_ANGLE)
        libmetawear.mbl_mw_datasignal_subscribe(signal, None, self.callback)
        libmetawear.mbl_mw_sensor_fusion_enable_data(self.device.board, SensorFusionData.EULER_ANGLE)
        libmetawear.mbl_mw_sensor_fusion_start(self.device.board)
        self.sensorFusionActive = True

    def sensorFusionStop(self):
        libmetawear.mbl_mw_sensor_fusion_stop(self.device.board)
        signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.device.board, SensorFusionData.EULER_ANGLE)
        libmetawear.mbl_mw_datasignal_unsubscribe(signal)
        self.sensorFusionActive = False

    def disconnectDevice(self):
        libmetawear.mbl_mw_debug_disconnect(self.device.board)

    def tareDevice(self):
        libmetawear.mbl_mw_sensor_fusion_reset_orientation(self.device.board)

    def __repr__(self):
        return self.address


class duinoSerial(serial.Serial):
    def getLoft(self):
        self.write(b'*10000')
        loft = self.readline()
        return loft

    def getLie(self):
        self.write(b'*20000')
        lie = self.readline()
        return lie

    def getFrame(self):
        self.write(b'*30000')
        frame = self.readline()
        return frame

    def setMCREF(self):
        self.write(b'*r0000')
        return

    def resetFrameCounter(self):
        self.write(b'*f0000')
        return

    def autoHoldOff(self):
        self.write(b'*h0000')
        return

    def autoHoldOn(self):
        self.write(b'*j0000')
        return

    def brightUp(self):
        self.write(b'*+0000')
        return

    def brightDwn(self):
        self.write(b'*-0000')
        return

    def servoStrong(self):
        self.write(b'*<0000')
        return

    def servoWeak(self):
        self.write(b'*>0000')
        return

    def seekAngle(self, target):
        target = int(target * 10)
        if target >= 0:
            sign = '+'
        elif target < 0:
            sign = '-'
        targetSTR = str(abs(target))
        if target == 0:
            return 1
        elif len(targetSTR) == 3:
            targetCMD = "*s" + sign + targetSTR
        elif len(targetSTR) == 2:
            targetCMD = "*s" + sign + '0' + targetSTR
        elif len(targetSTR) == 1:
            targetCMD = "*s" + sign + '00' + targetSTR
        self.write(targetCMD.encode('ascii'))
        result = self.readline()  # If readLIne times out, result = b'',
        try:
            result = int(result.strip())  # If readLine = b'', will throw error
        except:
            return -2  # Return timeout message to wrapper
        return result

    def seekHome(self):
        self.write(b'*c0000')
        result = self.readline()
        try:
            result = int(result.strip())
        except:
            return -2
        return result


if __name__ == '__main__':
    pass
