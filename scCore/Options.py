from pathlib import Path
import logging
import json

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = "WARNING"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

OPTIONS_FILE_PATH = Path('./options.json')

DEFAULT_X=0
DEFAULT_Y=0
DEFAULT_W=1920
DEFAULT_H=1080
DEFAULT_PATH='./Screenshots'

X_OFFSET_KEY    = 'xOffset'
Y_OFFSET_KEY    = 'yOffset'
WIDTH_KEY       = 'width'
HEIGHT_KEY      = 'height'
PATH_KEY        = 'path'
LOG_LEVEL_KEY   = 'logLevel'

class Options(object):  
    """ Hold program options
    """      
    def __init__(self, path:str, xOffset:int, yOffset:int, width:int, height:int, logLevel:str):
        self.xOffset = int(xOffset)
        self.yOffset = int(yOffset)
        self.width = int(width)
        self.height = int(height)
        self.path = Path(path)
        self.logLevel = logLevel.upper()
        
    def region(self) -> tuple:
        return (self.xOffset, self.yOffset, self.width, self.height)
        
    def toString(self) -> str:
        return 'Folder path: '+ str(self.path) +', X Offset: ' + str(self.xOffset) + ', Y Offset: ' + str(self.yOffset) + ', width: ' + str(self.width) + ', height: ' + str(self.height) 
    
# Functions for managing options

def toOptions(optsAsJson) -> Options:
    """Convert a json object into Options
    Args:
        optsAsJson (json): The json to convert
    Returns:
        Options: The options contained in the json
    """
    return Options(
        optsAsJson[PATH_KEY], 
        optsAsJson[X_OFFSET_KEY], 
        optsAsJson[Y_OFFSET_KEY], 
        optsAsJson[WIDTH_KEY], 
        optsAsJson[HEIGHT_KEY], 
        optsAsJson[LOG_LEVEL_KEY]
        )

def loadOptions() -> Options:
    """ Load options from save file
    Returns:
        Options: Deserialized contents of the file
    """
    if not OPTIONS_FILE_PATH.exists():
        logger.info('No save file found, using defaults')
        return Options(DEFAULT_PATH, DEFAULT_X, DEFAULT_Y, DEFAULT_W, DEFAULT_H, DEFAULT_LOG_LEVEL)
    try:
        with open(OPTIONS_FILE_PATH, "r") as f:
            return json.load(f, object_hook=toOptions)
    except Exception as ex:
        print("Error while loading options:", str(ex))
        logger.exception('Error while loading options')
        return Options(DEFAULT_PATH, DEFAULT_X, DEFAULT_Y, DEFAULT_W, DEFAULT_H, DEFAULT_LOG_LEVEL)

def saveOptions(options: Options) -> bool:
    """Save options to file
    Args:
        options (Options): The options we want to save
    """
    logger.warning('Saving options')
    try:
        with open(OPTIONS_FILE_PATH, "w") as f:
            json.dump({
                X_OFFSET_KEY: options.xOffset,
                Y_OFFSET_KEY: options.yOffset,
                WIDTH_KEY: options.width,
                HEIGHT_KEY: options.height,
                PATH_KEY: str(options.path),
                LOG_LEVEL_KEY : options.logLevel
                }, f, indent=4)
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