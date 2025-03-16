import logging
import sys
import argparse
from pathlib import Path
from scCore.ScreenshotEventHandler import *

# TODO 
# - Functionality for saving/loading options
# - GUI

DEFAULT_X=0
DEFAULT_Y=0
DEFAULT_W=1920
DEFAULT_H=1080
DEFAULT_PATH='./Screenshots'

DEFAULT_LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logger = logging.getLogger(__name__)

def initArgParser() -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="screenshot-cropper.py", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=f'''\
Listen for screenshots, crop them to the desired format, and save them to disk
''')
    parser.add_argument("-l", "--log-level", dest="logLevel", help=f"Level of detail for logged events. Default: {DEFAULT_LOG_LEVEL}", default=DEFAULT_LOG_LEVEL)
    parser.add_argument("-p", "--path", help=f"Path to the folder where the screenshots will be saved. Currently: {DEFAULT_PATH}.", default=DEFAULT_PATH)
    parser.add_argument("-x", "--x-offset", dest="x", type=int,  help=f"x offset (from top left) for the crop box. Currently: {DEFAULT_X}.", default=DEFAULT_X)
    parser.add_argument("-y", "--y-offset", dest='y', type=int, help=f"y offset from top left of the crop box. Currently: {DEFAULT_Y}.", default=DEFAULT_Y)
    parser.add_argument("-W", "--width", type=int, help=f"Width of crop box. Currently: {DEFAULT_W}.", default=DEFAULT_W)
    parser.add_argument("-H", "--height", type=int, help=f"Height of crop box. Currently: {DEFAULT_H}.", default=DEFAULT_H)
    return parser.parse_args()

def main():
    args = initArgParser()
    
    # Configure logs
    
    logging.basicConfig(format=LOG_FORMAT, filename='ScreenshotCropper.log', level=args.logLevel.upper(), filemode='w')
    
    # Init
    
    logger.warning('Initialising')
    options = Options(args.path, args.x, args.y, args.width, args.height)
    validateOptions(options)
    options.path.mkdir(666, True, True)
    handler = ScreenShotEventHandler(options)
    
    # Listen and block
    
    try:
        handler.startListening()
        input("Listening. Press F12 for screenshots. Press enter on this window to exit.")
    finally:
        # Probably unecessary
        handler.stopListening()
    
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