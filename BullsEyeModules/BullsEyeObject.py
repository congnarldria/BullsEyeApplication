from BullsEyeModules import BullsEyeIO as BEIO
from BullsEyeModules import modelData as MD
from tkinter import *
from PIL import Image, ImageTk

class BullsEye():
    def __init__(self):
        # IO Objects
        self.myCamera = None
        self.servoController = None
        self.mbtModule = None

        # Lie/Loft values from Arduino
        self.loftPro = 0
        self.liePro = 0

        # Lie/Loft Values calculated
        self.loftSys = 0
        self.lieSys = 0

        # Frame
        self.frame = 0
        self.frameBase = 30
        self.calcFrame = 0

        # Lie/Loft compensation values from BT Accelerometer
        self.btLoftCompVal = 0
        self.btLieCompVal = 0

        # Target BT Values  << This should be initiated from each specific UI class??
        self.targetLoft = 0
        self.targetLie = 0

        # Scoreline variables
        # [X, Y, W, H, tilt Limit, zeroLineY]
        self.scoreFilterSettings = [110, 50, 260, 225, 3, 240]
        self.scoreFilterSettingsDefault = [110, 50, 260, 225, 3, 240]
        self.avgScorelineSlope = 0  # Place holder
        self.zeroLineSlope = 0  # Used for calibraiton
        self.zeroLineAngle = 0  # Used for LieSys Calculations
        self.zeroLineSlopeDefault = 0  # Default value
        self.lieOffset = 0

        # Loft Calibration Variables
        self.calStickVal = 27
        self.calcFrameVal = 0
        self.seekAngle = 0

        # BT Address Log
        self.defaultIndex = ''
        self.btAddressDefault = ''
        self.btAddressList = []

        #Model Data
        self.modelList = None
        self.currentModel = None
        self.currentClubIndex = None

        # Streaming Variables
        self.vidStreamActive = False
        self.btStreamActive = False
        self.angleStreamActive = False

        # Image Place Holders
        self.tk_raw = None
        self.tk_score = None

        #
        self.clubModelDataFilePath = '/home/pi/BullsEyeApplication/Settings/clubData.csv'
        self.scoreSettingsFilePath = '/home/pi/BullsEyeApplication/Settings/scoreFilterSettings.txt'
        self.btAddressLogFilePath = '/home/pi/BullsEyeApplication/Settings/btAddressLog.txt'

    def initiateIO(self):
        if self.btAddressDefault != '' and self.mbtModule == None:
            try:
                mod = BEIO.State(self.btAddressDefault)
                self.mbtModule = mod
                self.sensorFusionIsOn=1
            except:
                pass
        if self.myCamera == None:
            try:
                cam = BEIO.rpiCam()
                self.myCamera = cam
            except:
                pass
        if self.servoController == None:
            try:
                serCon = BEIO.duinoSerial(port='/dev/ttyACM0', timeout=None)
                self.servoController = serCon
            except:
                pass
            
    def connectBT(self, address):
        try:
            mod = BEIO.State(self.btAddressDefault)
            self.mbtModule = mod
            return 1
        except:
            return 0
        
    def updateBtAddressFromFile(self):
        btAddressLog = open(self.btAddressLogFilePath)
        self.defaultIndex = btAddressLog.readline()
        self.defaultIndex = int(self.defaultIndex) - 1  # Attune to list index
        for i in range(0, 50):
            address = btAddressLog.readline()
            if address != '':
                self.btAddressList.append(address.strip())
                i = i + 1
            else:
                break
        btAddressLog.close()
        if self.btAddressList != []:
            self.btAddressDefault = self.btAddressList[self.defaultIndex]
            
    def updateBtAddressFile(self):
        btAddressLog = open(self.btAddressLogFilePath, 'w')
        btAddressLog.write(str(self.defaultIndex+1))
        btAddressLog.write('\n')
        for i in range(len(self.btAddressList)):
            btAddressLog.write(str(self.btAddressList[i]))
            btAddressLog.write('\n')
        btAddressLog.close()
        if self.btAddressList != []:
            self.btAddressDefault = self.btAddressList[self.defaultIndex]
    
    def updateScoreFilterFromFile(self):
        f = open(self.scoreSettingsFilePath)
        settings = [] #Order: [originX, OriginY, Width, Height, Tilt, ZeroY, FrameAngle]
        for i in range (0, 7):
            line = f.readline()
            title, data = line.split(",")
            data = data.strip(", []\n")
            if i ==6:
                settings.append(float(data))
                break
            settings.append(int(data))
        self.scoreFilterSettings = settings[:]
        self.frameBase = self.scoreFilterSettings[6]
        self.frame = self.frameBase
        f.close()       

    def updateScoreSettingFile(self):
        f = open(self.scoreSettingsFilePath, "w")
        scoreDict = ('OriginX', 'OriginY', 'Width', 'Height', 'Tilt', 'ZeroY')
        for i in range (0, 6):
            tag = scoreDict[i]
            data = str(self.scoreFilterSettings[i])
            line = tag + ', ' + data
            f.write(line)
            f.write('\n')
        data = str(self.frame)
        line = 'Frame' + ', ' + data
        f.write(line)
        f.close()
        
    def updateModelDataFromCSV(self):
        self.modelList = MD.model.populateFromCSV(self.clubModelDataFilePath)
        if self.modelList:
            self.currentModel = list(MD.model.modelList.values())[0]
        if self.currentModel.clubs:
            self.currentClubIndex = 0

    def importImage(self, path):
        image = Image.open(path)
        image = ImageTk.PhotoImage(image)
        return image
    def resizeimportimage(self , path , reizewh):
        image = Image.open(path)
        image = image.resize(reizewh)
        image = ImageTk.PhotoImage(image)
        return image
        return image
    def loadIconImages(self):
        self.servoStrong = self.importImage("/home/pi/BullsEyeApplication/UI/icons/servoStrong.png")
        self.servoWeak = self.importImage("/home/pi/BullsEyeApplication/UI/icons/servoWeak.png")
        self.servoHome = self.importImage("/home/pi/BullsEyeApplication/UI/icons/servoHome.png")
        self.brightUp = self.importImage("/home/pi/BullsEyeApplication/UI/icons/brightUp.png")
        self.brightDwn = self.importImage("/home/pi/BullsEyeApplication/UI/icons/brightDwn.png")
        self.instructionsBack = self.importImage("/home/pi/BullsEyeApplication/UI/icons/instructionsBack.png")
        self.instructionsNext = self.importImage("/home/pi/BullsEyeApplication/UI/icons/instructionsNext.png")
        self.mainMenu = self.importImage("/home/pi/BullsEyeApplication/UI/icons/mainMenu.png")
        self.protractor = self.importImage("/home/pi/BullsEyeApplication/UI/icons/protractor.png")
        self.bullsEyeIndicator = self.importImage("/home/pi/BullsEyeApplication/UI/icons/bullsEyeIndicator.png")
        # self.bullsEyeIndicator = self.resizeimportimage("/home/pi/BullsEyeApplication/UI/icons/bullsEyeIndicator.png", (500,410))