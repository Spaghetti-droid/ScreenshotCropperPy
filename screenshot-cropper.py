import logging
import pickle
import argparse
from pathlib import Path
from scCore.ScreenshotEventHandler import *

# TODO 
# - GUI

OPTIONS_FILE_PATH = Path('./options.pickle')

DEFAULT_X=0
DEFAULT_Y=0
DEFAULT_W=1920
DEFAULT_H=1080
DEFAULT_PATH='./Screenshots'

DEFAULT_LOG_LEVEL = "WARNING"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logger = logging.getLogger(__name__)
logging.basicConfig(format=LOG_FORMAT, filename='ScreenshotCropper.log', level=DEFAULT_LOG_LEVEL, filemode='w')

def initArgParser(options: Options) -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="screenshot-cropper.py", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=f'''\
Listen for screenshots, crop them to the desired format, and save them to disk
''')
    parser.add_argument("-l", "--log-level", dest="logLevel", help=f"Level of detail for logged events. Currently: {options.logLevel}", default=options.logLevel)
    parser.add_argument("-p", "--path", help=f"Path to the folder where the screenshots will be saved. Currently: {options.path}.", default=options.path)
    parser.add_argument("-x", "--x-offset", dest="x", type=int,  help=f"x offset from the top left of the captured area. Currently: {options.xOffset}.", default=options.xOffset)
    parser.add_argument("-y", "--y-offset", dest='y', type=int, help=f"y offset from the top left of the captured area. Currently: {options.yOffset}.", default=options.yOffset)
    parser.add_argument("-W", "--width", type=int, help=f"Width of the captured area. Currently: {options.width}.", default=options.width)
    parser.add_argument("-H", "--height", type=int, help=f"Height of the captured area. Currently: {options.height}.", default=options.height)
    parser.add_argument("-s", "--save", action='store_true', help=f"Save the provided options, so that they become the new defaults.")
    return parser.parse_args()

def main():
    # Get arguments
    
    savedOptions = loadOptions()
    args = initArgParser(savedOptions)
        
    # Init
    
    logger.setLevel(args.logLevel.upper())
    
    logger.warning('Initialising')
    options = Options(args.path, args.x, args.y, args.width, args.height, args.logLevel)
    validateOptions(options)
    if args.save:
        saveOptions(options)
    options.path.mkdir(666, True, True)
    handler = ScreenShotEventHandler(options)
    
    optionsReport = 'Using Options:{ ' + options.toString() +' }'
    print(optionsReport)
    logger.info(optionsReport)
    
    # Listen and block
    
    try:
        handler.startListening()
        input("Listening. Press F12 to take screenshots. Press enter when focused on this window to stop.")
    finally:
        # Probably unecessary
        handler.stopListening()
   
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
        logger.exception('Error while loading options', ex)
        return Options(DEFAULT_PATH, DEFAULT_X, DEFAULT_Y, DEFAULT_W, DEFAULT_H, DEFAULT_LOG_LEVEL)

def saveOptions(options: Options) -> None:
    """Save options to file
    Args:
        options (Options): The options we want to save
    """
    logger.warning('Saving options')
    try:
        with open(OPTIONS_FILE_PATH, "wb") as f:
            pickle.dump(options, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        logger.error('Failed to save options! ', ex)
    
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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if hasattr(e, 'message'):
            print(f"Error: {e.message}")
        else:
            print(f"Error: {e}")
        logger.exception(msg="Program terminated due to an exception", exc_info=e)