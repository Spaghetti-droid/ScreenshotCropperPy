import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from pathlib import Path
import logging
import scCore.Options as opt
import scCore.ScreenshotEventHandler as seh

# TODO 
# - Options as JSON
# - Help screen

# Load saved config

logger = logging.getLogger(__name__)
logging.basicConfig(format=opt.LOG_FORMAT, filename='ScreenshotCropper.log', level=opt.DEFAULT_LOG_LEVEL, filemode='w')
options = opt.loadOptions()
logger.setLevel(options.logLevel)

# Callbacks

def selectFolder() -> str:
    """Open the file selection dialog and allow the user to choose a new destination.
    If a new destination is chosen, it is set to destFolder
    """
    newDest = fd.askdirectory(initialdir=destFolder, title='Destination Folder')
    if newDest:
        destFolder.set(newDest)
        
def updateCurrentOptions() -> bool:
    """Update options with the values contained in the fields. Shows an error message to the user if the inputs are invalid.

    Returns:
        bool: True if the update was successful, False if an invalid value was encountered or an error was triggered
    """
    try:
        options.path = Path(destFolder.get())
        options.xOffset = xOffset.get()
        options.yOffset = yOffset.get()
        options.width = width.get()
        options.height = height.get()
        return True
    except Exception as e:
        logger.exception("Options update failed")
        messagebox.showerror("Invalid parameters", "Please check your inputs and try again")
        return False

def saveOptions() -> None:
    """Save options as a file. Shows a message to the user if saving failed.
    """
    if not updateCurrentOptions():
        return
    if opt.saveOptions(options):
        saveBtn.config(text='Saved!')
        saveBtn.after(500, resetSaveLabel)
    else:
        messagebox.showerror("Error", "Failed to save!")
        
def resetSaveLabel() -> None:
    saveBtn.config(text='Save')
        
def toggle() -> None:
    """ Toggles listening on or off. listener is set to None when listening is off. An new instance is created when listening is turned on.
    """
    global listener
    # Start listening
    if listener:
        # Stop listening
        listener.stopListening()
        listener=None
        # Update button
        startBtn.config(text='Start')
    else:
        if not updateCurrentOptions():
            return
        try:            
            listener = seh.ScreenShotEventHandler(options)
            if not options.path.exists():
                options.path.mkdir(666, True, True)
            listener.startListening()
            # change label and command
            startBtn.config(text='Stop')
        except Exception as e:
            messagebox.showerror("Error", "Couldn't start listening!")
            logger.error("Couldn't start listening!", exc_info=e) 
            # As a precaution if the startBtn.config somehow failed
            if listener:
                listener.stopListening()    
                listener = None
 
# Create window

root = tk.Tk()
root.title("Screenshot Cropper")
root.geometry('550x200')

# Initialise field values

destFolder = tk.StringVar(value=options.path)
xOffset = tk.IntVar(value=options.xOffset)
yOffset = tk.IntVar(value=options.yOffset)
width  = tk.IntVar(value=options.width)
height = tk.IntVar(value=options.height)

# Destination choice

destFrame = tk.Frame(root)
destFrame.pack(fill=tk.X, pady=5, padx=10, expand=True)

ttk.Label(destFrame, text='Destination Folder').pack(side=tk.LEFT, padx=10, pady=5)
ttk.Entry(destFrame, textvariable=destFolder).pack(side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(destFrame, text='Browse', command=selectFolder).pack(side=tk.LEFT, padx=10, pady=5)

ttk.Separator(root, orient='horizontal').pack(fill=tk.X, padx=50, pady=5, expand=True)

# Screenshot area options

areaFrame = tk.Frame(root)
areaFrame.pack(padx=50, pady=5, expand=True)

ttk.Label(areaFrame, text='X Offset').grid(column=0, row=0, padx=5, pady=5)
ttk.Entry(areaFrame, textvariable=xOffset, width=8).grid(column=1, row=0, padx=5, pady=5)
ttk.Label(areaFrame, text='Width ').grid(column=2, row=0, padx=5, pady=5)
ttk.Entry(areaFrame, textvariable=width, width=8).grid(column=3, row=0, padx=5, pady=5)

ttk.Label(areaFrame, text='Y Offset').grid(column=0, row=1, padx=5, pady=5)
ttk.Entry(areaFrame, textvariable=yOffset, width=8).grid(column=1, row=1, padx=5, pady=5)
ttk.Label(areaFrame, text='Height').grid(column=2, row=1, padx=5, pady=5)
ttk.Entry(areaFrame, textvariable=height, width=8).grid(column=3, row=1, padx=5, pady=5)

ttk.Separator(root, orient='horizontal').pack(fill=tk.X, padx=50, pady=5, expand=True)

# Buttons

buttonFrame = tk.Frame(root)
buttonFrame.pack(fill=tk.X, pady=5, expand=True)

saveBtn = ttk.Button(buttonFrame, text='Save', command=saveOptions)
saveBtn.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

listener = None
startBtn = ttk.Button(buttonFrame, text='Start', command=toggle)
startBtn.pack(side=tk.LEFT, padx=10, pady=5, expand=True)
ttk.Button(buttonFrame, text='Close', command=lambda:root.quit()).pack(side=tk.LEFT, padx=10, pady=5, expand=True)


root.mainloop()