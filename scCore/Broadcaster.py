from enum import Enum
from typing import List
from abc import ABC, abstractmethod
import datetime as dt

class EventType(Enum):
    START_LISTENING = 1
    STOP_LISTENING = 2
    SCREENSHOT = 3
    FAILURE = 4
    WAITING = 5

class Event:
    """A broadcasted event
    """
    def __init__(self, type:EventType, text:str):
        """
        Args:
            type (EventType):
            text (str): A human-readable description of the event
        """
        self.time = dt.datetime.now()
        self.type = type
        self.text = text
    
class Subscriber(ABC):
    """Abstract class representing a subscriber to the broadcaster.
    Anything wanting to subscribe should inherit from this class.
    """
    @abstractmethod
    def trigger(self, event:Event) -> None:
        """ Inform the subscriber of an event
        Args:
            event (Event):
        """
        pass

class Broadcaster:
    """Broadcasts events to all subscribers
    """
    def __init__(self):
        self.subscribers:List[Subscriber] = []
        
    def subscribe(self, subscriber:Subscriber) -> None:
        """ Add a subscriber which will be informed of events
        Args:
            subscriber (Subscriber):
        """
        self.subscribers.append(subscriber)
        
    def report(self, type:EventType, text:str) -> None:
        """ Create an Event and transmit it to all subscribers
        Args:
            type (EventType):
            text (str): A human-readable description
        """
        event = Event(type, text)
        for subscriber in self.subscribers:
            subscriber.trigger(event)