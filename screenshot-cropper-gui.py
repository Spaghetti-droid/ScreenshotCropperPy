import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from pathlib import Path
import logging
import scCore.Options as opt
import scCore.ScreenshotEventHandler as seh

# Load saved config

logger = logging.getLogger(__name__)
logging.basicConfig(format=opt.LOG_FORMAT, filename='ScreenshotCropper.log', level=opt.DEFAULT_LOG_LEVEL, filemode='w')
options = opt.loadOptions()
logger.setLevel(options.logLevel)

# Callbacks

def selectFolder() -> str:
    newDest = fd.askdirectory(initialdir=destFolder, title='Destination Folder')
    if newDest:
        destFolder.set(newDest)
        
def updateCurrentOptions() -> bool:
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
    if not updateCurrentOptions():
        return
    if not opt.saveOptions(options):
        messagebox.showerror("Error", "Failed to save!")
        
def toggle() -> None:
    global handler
    # Start listening
    if handler:
        # Stop listening
        handler.stopListening()
        handler=None
        # Update button
        startBtn.config(text='Start')
    else:
        if not updateCurrentOptions():
            return
        try:            
            handler = seh.ScreenShotEventHandler(options)
            handler.startListening()
            # change label and command
            startBtn.config(text='Stop')
        except Exception as e:
            messagebox.showerror("Error", "Couldn't start listening!")
            logger.error("Couldn't start listening!", exc_info=e) 
            # As a precaution if the startBtn.config somehow failed
            if handler:
                handler.stopListening()    
                handler = None
 
# Create window

root = tk.Tk()
root.title("Screenshot Cropper")
root.geometry('550x200')

destFolder = tk.StringVar(value=options.path)
xOffset = tk.IntVar(value=options.xOffset)
yOffset = tk.IntVar(value=options.yOffset)
width  = tk.IntVar(value=options.width)
height = tk.IntVar(value=options.height)

handler = None

destFrame = tk.Frame(root)
destFrame.pack(fill=tk.X, pady=5, padx=10, expand=True)

ttk.Label(destFrame, text='Destination Folder').pack(side=tk.LEFT, padx=10, pady=5)
ttk.Entry(destFrame, textvariable=destFolder).pack(side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(destFrame, text='Browse', command=selectFolder).pack(side=tk.LEFT, padx=10, pady=5)

ttk.Separator(root, orient='horizontal').pack(fill=tk.X, padx=50, pady=5, expand=True)

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

buttonFrame = tk.Frame(root)
buttonFrame.pack(fill=tk.X, pady=5, expand=True)

ttk.Button(buttonFrame, text='Save', command=saveOptions).pack(side=tk.LEFT, padx=10, pady=5, expand=True)
startBtn = ttk.Button(buttonFrame, text='Start', command=toggle)
startBtn.pack(side=tk.LEFT, padx=10, pady=5, expand=True)
ttk.Button(buttonFrame, text='Close', command=lambda:root.quit()).pack(side=tk.LEFT, padx=10, pady=5, expand=True)


root.mainloop()