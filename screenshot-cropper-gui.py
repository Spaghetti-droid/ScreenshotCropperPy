import tkinter as tk
from tkinter import ttk
import logging
import scCore.Options as opt
import scCore.Broadcaster as bc
import scGUI.guiService as gs

# Init logger

logger = logging.getLogger(__name__)
logging.basicConfig(format=opt.LOG_FORMAT, filename='ScreenshotCropper.log', level=opt.DEFAULT_LOG_LEVEL, filemode='w')
options = opt.loadOptions()

# Get args and adjust log level

logger.setLevel(gs.parseArgs(options).logLevel)

# Create window

root = tk.Tk()
root.title("Screenshot Cropper - Take screenshots with F12")
root.geometry('700x250')

# Initialise field values

destFolder = tk.StringVar(value=options.path)
xOffset = tk.IntVar(value=options.xOffset)
yOffset = tk.IntVar(value=options.yOffset)
width  = tk.IntVar(value=options.width)
height = tk.IntVar(value=options.height)

lastEvent = tk.StringVar()
eventDate = tk.StringVar()
events = []

# Init data handling objects

updater = gs.OptionUpdater(destFolder, xOffset, yOffset, width, height, options)
broadcaster = bc.Broadcaster()
broadcaster.subscribe(gs.GuiSubscriber(eventDate, lastEvent, events))
saver = gs.Saver(updater)
executor = gs.Executor(broadcaster, updater)

# Event Log
BACKGROUND = "#444444"
NEUTRAL =   "#ffffff"
eventFrame = tk.Frame(root, background=BACKGROUND)
#ttk.Entry(eventFrame, textvariable=eventDate, width=18).pack(side=tk.LEFT, padx=10, pady=5)
#ttk.Label(eventFrame, textvariable=eventDate, font=("none", 50, "bold"), bg="#000000", fg="#910000", bd=5, relief="ridge").pack(side=tk.LEFT, padx=10, pady=5)
ttk.Label(eventFrame, textvariable=eventDate, font=("none", 10, "bold"), background=BACKGROUND, foreground=NEUTRAL).pack(side=tk.LEFT, padx=10, pady=5)
ttk.Label(eventFrame, textvariable=lastEvent, font=("none", 10, "bold"), background=BACKGROUND, foreground=NEUTRAL, anchor='center').pack(padx=10, pady=5, fill=tk.X, expand=True)
#ttk.Entry(eventFrame, textvariable=lastEvent).pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
eventFrame.pack(fill=tk.X, pady=5, padx=10, expand=True)

# Destination choice

destFrame = tk.Frame(root)
destFrame.pack(fill=tk.X, pady=5, padx=10, expand=True)

ttk.Label(destFrame, text='Destination Folder').pack(side=tk.LEFT, padx=10, pady=5)
ttk.Entry(destFrame, textvariable=destFolder).pack(side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(destFrame, text='Browse', command=lambda:gs.selectFolder(destFolder)).pack(side=tk.LEFT, padx=10, pady=5)

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

saveBtn = ttk.Button(buttonFrame, text='Save', command=saver.saveOptions)
saver.setButton(saveBtn)
saveBtn.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

startBtn = ttk.Button(buttonFrame, text='Start', command=executor.toggle)
executor.setButton(startBtn)
startBtn.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

ttk.Button(buttonFrame, text='Close', command=lambda:root.quit()).pack(side=tk.LEFT, padx=10, pady=5, expand=True)

broadcaster.report(bc.EventType.WAITING, text='Waiting to start')

root.mainloop()