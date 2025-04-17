from scCore.Options import Options
from scCore.ScreenshotNamer import ScreenShotNamer
from scCore.Broadcaster import Broadcaster, EventType
from pynput.keyboard import Key, Listener
import pyautogui
import logging

logger = logging.getLogger(__name__)

class ScreenShotEventHandler(object):  
    """ Listens for F12 and takes screenshots
    """      
    def __init__(self, options:Options, broadcaster:Broadcaster=Broadcaster()):
        self.region = options.region()
        self.namer = ScreenShotNamer(options.path) 
        self.listener = Listener(on_release=self.on_release) 
        self.broadcaster = broadcaster
    
    def takeScreenshot(self) -> None:
        """Takes a screenshot and stores it with an unused name
        """
        logger.warning('Taking screenshot')
        nextPath = self.namer.nextFreePath()
        pyautogui.screenshot(nextPath, region=self.region)
        self.report(EventType.SCREENSHOT, f'Screenshot saved to {nextPath}')
        
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
        self.report(EventType.START_LISTENING, 'Listening...')
        self.listener.start()
        
    def stopListening(self) -> None:
        """ Stop listening
        """
        self.report(EventType.STOP_LISTENING,'Stopped Listening')
        self.listener.stop()
        
    def report(self, eventType:EventType, text:str) -> None:
        logger.warning(text)
        self.broadcaster.report(eventType, text=text)