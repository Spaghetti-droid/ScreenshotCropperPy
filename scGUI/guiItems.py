import tkinter as tk
import argparse
import scCore.Broadcaster as bc
import scCore.Options as opt

class GuiSubscriber(bc.Subscriber):
    
    def __init__(self, eventDateVar:tk.StringVar, lastEventVar:tk.StringVar, events:list):
        self.events = events
        self.eventDate = eventDateVar
        self.lastEvent = lastEventVar
    
    def trigger(self, event:bc.Event) -> None:
        self.events.append(event)
        self.eventDate.set(event.time.strftime('%Y-%m-%d %H:%M:%S'))
        self.lastEvent.set(event.text)
        
def parseArgs(options:opt.Options) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="screenshot-cropper-gui.py", 
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description='''\
Listen for screenshots, crop them to the desired format, and save them to disk
''')
    parser.add_argument("-l", "--log-level", dest="logLevel", help=f"Level of detail for logged events. Default: {options.logLevel}", default=options.logLevel)
    return parser.parse_args()