class club():
    def __init__(self, modelID, clubID, lie, loft):
        self.modelID = modelID
        self.clubID = clubID
        self.lie = lie
        self.loft = loft

class model():
    modelList = {}

    def __init__(self, modelID):
        self.modelID = modelID
        self.clubs = []
        model.modelList[self.modelID] = self

    def addClub(self, clubID, lie, loft):
        c = club(self.modelID, clubID, lie, loft)
        self.clubs.append(c)

    @classmethod
    def populateFromCSV(cls, filePath):
        with open(filePath) as  fileObject:
            for line in fileObject:
                if line.strip('\n ') != '':
                    blank, modelID, clubID, lie, loft = line.split(',')
                    loft = loft.strip('\n')
                    if modelID in cls.modelList:
                        cls.modelList[modelID].addClub(clubID, lie, loft)
                    else:
                        newModel = cls(modelID)
                        newModel.addClub(clubID, lie, loft)
        return cls.modelList

if __name__ == '__main__':
    model.populateFromCSV('/home/pi/BullsEyeApplication/Settings/clubData.csv')

    for c in model.modelList['ATV Wedge'].clubs:
        print(c.clubID, c.lie, c.loft)



