import tkinter as tk
from tkinter import ttk
import argparse
from tkinter import filedialog as fd
from tkinter import messagebox
from pathlib import Path
import logging
import scCore.ScreenshotEventHandler as seh
import scCore.Broadcaster as bc
import scCore.Options as opt

logger = logging.getLogger(__name__)

# Classes
class GuiSubscriber(bc.Subscriber):
    """A subscriber that updates vars based on the events it receives
    """
    def __init__(self, eventDateVar:tk.StringVar, lastEventVar:tk.StringVar, events:list):
        self.events = events
        self.eventDate = eventDateVar
        self.lastEvent = lastEventVar
    
    def trigger(self, event:bc.Event) -> None:
        """Use event to update text and date information in vars
        """
        self.events.append(event)
        self.eventDate.set(event.time.strftime('%Y-%m-%d %H:%M:%S'))
        self.lastEvent.set(event.text)
     
class OptionUpdater:
    def __init__(self, destFolder:tk.StringVar, xOffset:tk.IntVar, yOffset:tk.IntVar, width:tk.IntVar, height:tk.IntVar, options:opt.Options):
        self._destFolder = destFolder
        self._xOffset = xOffset
        self._yOffset = yOffset
        self._width = width
        self._height = height
        self._options = options
        
    def _updateCurrentOptions(self) -> bool:
        """Update options with the values contained in the fields. Shows an error message to the user if the inputs are invalid.

        Returns:
            bool: True if the update was successful, False if an invalid value was encountered or an error was triggered
        """
        try:
            self._options.path = Path(self._destFolder.get())
            self._options.xOffset = self._xOffset.get()
            self._options.yOffset = self._yOffset.get()
            self._options.width = self._width.get()
            self._options.height = self._height.get()
            logger.info("Options updated to: {" + self._options.toString() + "}")
            return True
        except Exception:
            logger.exception("Options update failed")
            messagebox.showerror("Invalid parameters", "Please check your inputs and try again")
            return False
        
    def updateOptions(self) -> opt.Options:
        if self._updateCurrentOptions():
            return self._options
        return None
        
    
class Executor:
    """Starts and stops listening for screenshots
    """
    def __init__(self, broadcaster:bc.Broadcaster, updater:OptionUpdater, startBtn:ttk.Button=None):
        self._listener = None
        self._broadcaster = broadcaster
        self._startBtn = startBtn
        self._updater = updater
        
    def setButton(self, button:ttk.Button) -> None:
        self._startBtn = button
     
    def toggle(self) -> None:
        """ Toggles listening on or off. listener is set to None when listening is off. An new instance is created when listening is turned on.
        """
        if not self._startBtn:
            raise ValueError("Button not set!")
        
        # Start listening
        if self._listener:
            self._stop()
        else:
            self._start()
                    
    def _stop(self):
        """Stop listener and reset button
        """
        # Stop listening
        self._listener.stopListening()
        self._listener=None
        # Update button
        self._startBtn.config(text='Start')
        
    def _start(self):
        """Update options, start listener, change button label
        """
        options = self._updater.updateOptions()
        if not options:
            return
        try:            
            self._listener = seh.ScreenShotEventHandler(options, self._broadcaster)
            if not createOrCheckFolderPath(options.path):
                return
            self._listener.startListening()
            # change label and command
            self._startBtn.config(text='Stop')
        except Exception as e:
            messagebox.showerror("Error", "Couldn't start listening!")
            logger.error("Couldn't start listening!", exc_info=e) 
            # As a precaution if the startBtn.config somehow failed
            if self._listener:
                self._listener.stopListening()    
                self._listener = None
                    
class Saver:
    """Updates and saves options
    """
    def __init__(self, updater:OptionUpdater, saveBtn:ttk.Button=None):
        self._saveBtn = saveBtn
        self._updater = updater
        
    def setButton(self, button:ttk.Button) -> None:
        self._saveBtn = button

    def saveOptions(self) -> None:
        """Save options as a file. Shows a message to the user if saving failed.
        """
        if not self._saveBtn:
            raise ValueError("Button not set!")
        
        options = self._updater.updateOptions()
        if not options:
            return
        if opt.saveOptions(options):
            self._saveBtn.config(text='Saved!')
            self._saveBtn.after(500, self._resetSaveLabel)
        else:
            messagebox.showerror("Error", "Failed to save!")
            
    def _resetSaveLabel(self) -> None:
        self._saveBtn.config(text='Save')
                    
# Functions
        
def parseArgs(options:opt.Options) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="screenshot-cropper-gui.py", 
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description='''\
Listen for screenshots, crop them to the desired format, and save them to disk
''')
    parser.add_argument("-l", "--log-level", dest="logLevel", help=f"Level of detail for logged events. Default: {options.logLevel}", default=options.logLevel)
    return parser.parse_args()


def selectFolder(destFolder:tk.StringVar) -> str:
    """Open the file selection dialog and allow the user to choose a new destination.
    If a new destination is chosen, it is set to destFolder
    """
    newDest = fd.askdirectory(initialdir=destFolder, title='Destination Folder')
    if newDest:
        destFolder.set(newDest)

def createOrCheckFolderPath(path: Path) -> bool:
    """Create folder at path if it doesn't exist
    If it does exist, check that it is a folder

    Args:
        path (Path): Path to a folder

    Returns:
        bool: True if the path points to a folder, which may have been created by this function 
    """
    if not path.exists():
        # Let umask determine permissions
        path.mkdir(0o777, True, True)
        return True
    elif not path.is_dir():
        messagebox.showerror("Error", "Destination is not a folder!")
        logger.error(f"Destination is not a folder: {path}")
        return False
    
    return True