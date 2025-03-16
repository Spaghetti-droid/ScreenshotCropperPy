from pathlib import Path

class Options(object):  
    """ Hold program options
    """      
    def __init__(self, path, xOffset, yOffset, width, height, logLevel):
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.width = width
        self.height = height
        self.path = Path(path)
        self.logLevel = logLevel
        self.region = (self.xOffset, self.yOffset, self.width, self.height)
        
    def toString(self) -> str:
        return 'Folder path: '+ str(self.path) +', X Offset: ' + str(self.xOffset) + ', Y Offset: ' + str(self.yOffset) + ', width: ' + str(self.width) + ', height: ' + str(self.height) 