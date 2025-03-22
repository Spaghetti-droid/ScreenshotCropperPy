from pathlib import Path
import logging
import pickle

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = "WARNING"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

OPTIONS_FILE_PATH = Path('./options.pickle')

DEFAULT_X=0
DEFAULT_Y=0
DEFAULT_W=1920
DEFAULT_H=1080
DEFAULT_PATH='./Screenshots'

class Options(object):  
    """ Hold program options
    """      
    def __init__(self, path:str, xOffset:int, yOffset:int, width:int, height:int, logLevel:str):
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.width = width
        self.height = height
        self.path = Path(path)
        self.logLevel = logLevel.upper()
        self.region = (self.xOffset, self.yOffset, self.width, self.height)
        
    def toString(self) -> str:
        return 'Folder path: '+ str(self.path) +', X Offset: ' + str(self.xOffset) + ', Y Offset: ' + str(self.yOffset) + ', width: ' + str(self.width) + ', height: ' + str(self.height) 
    
# Functions for managing options

def loadOptions() -> Options:
    """ Load options from save file
    Returns:
        Options: Deserialized contents of the file
    """
    if not OPTIONS_FILE_PATH.exists():
        logger.info('No save file found, using defaults')
        return Options(DEFAULT_PATH, DEFAULT_X, DEFAULT_Y, DEFAULT_W, DEFAULT_H, DEFAULT_LOG_LEVEL)
    try:
        with open(OPTIONS_FILE_PATH, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error while loading options:", ex)
        logger.exception('Error while loading options: '+ str(ex))
        return Options(DEFAULT_PATH, DEFAULT_X, DEFAULT_Y, DEFAULT_W, DEFAULT_H, DEFAULT_LOG_LEVEL)

def saveOptions(options: Options) -> bool:
    """Save options to file
    Args:
        options (Options): The options we want to save
    """
    logger.warning('Saving options')
    try:
        with open(OPTIONS_FILE_PATH, "wb") as f:
            pickle.dump(options, f, protocol=pickle.HIGHEST_PROTOCOL)
        return True
    except Exception as ex:
        logger.error('Failed to save options! ', ex)
        return False
    
def validateOptions(options: Options) -> None:
    """Check values in options are correct
    Args:
        options (Options): The options we are running with
    Raises:
        ValueError: If an option has a bad value 
    """
    if options.path.exists() and not options.path.is_dir():
        raise ValueError(f'File on provided path is not a Directory!')   
    validateInt('X Offset', options.xOffset)
    validateInt('Y Offset', options.yOffset)
    validateInt('Width', options.width)
    validateInt('Height', options.height)
    
def validateInt(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f'{name} has invalid value: {value}')