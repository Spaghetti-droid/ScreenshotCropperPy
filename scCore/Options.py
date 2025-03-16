from pathlib import Path

class Options(object):  
    """ Hold program options
    """      
    def __init__(self, path, xOffset, yOffset, width, height):
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.width = width
        self.height = height
        self.path = Path(path)
        self.region = (self.xOffset, self.yOffset, self.width, self.height)