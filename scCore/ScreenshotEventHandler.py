from scCore.Options import Options
from scCore.ScreenshotNamer import ScreenShotNamer
from pynput.keyboard import Key, Listener
import pyautogui
import logging

logger = logging.getLogger(__name__)

class ScreenShotEventHandler(object):  
    """ Listens for F12 and takes screenshots
    """      
    def __init__(self, options:Options):
        self.region = options.region 
        self.namer = ScreenShotNamer(options.path) 
        self.listener = Listener(on_release=self.on_release) 
    
    def takeScreenshot(self) -> None:
        """Takes a screenshot and stores it with an unused name
        """
        logger.warning('taking screenshot')
        pyautogui.screenshot(self.namer.nextFreePath(), region=self.region)
        
    def on_release(self, key):
        """When a key is released, check whether it is the trigger for a screenshot
        Args:
            key (_type_): the pressed key
        """
        if key == Key.f12:            
            logger.debug('F12 release detected')
            self.takeScreenshot()      

    def startListening(self) -> None:   
        """ Start listening for button presses. Does not block.
        """ 
        logger.warning('Listening...')
        self.listener.start()
        
    def stopListening(self) -> None:
        """ Stop listening
        """
        logger.warning('Stopped Listening')
        self.listener.stop()