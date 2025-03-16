from pathlib import Path
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)
PREFIX = 'Screenshot '
SUFFIX = '.png'

class ScreenShotNamer(object):  
    """ Handles screenshot events
    """      
    def __init__(self, parentDir:Path):
        self.parent = parentDir   
        self.date = None
        
        
    def nextName(self) -> str:
        """ Generate the next file name. 
        Returns:
            str: The name 
        """
        today = datetime.today().date()
        if self.date != today:
            logger.info('New date detected, resettign counters')
            self.date = today
            self.dateStr = datetime.today().strftime('%Y-%m-%d')
            self.nameIdx = 0
        
        self.nameIdx += 1
        
        return self.fileNamePattern(str(self.nameIdx))
    
    def nextFreePath(self) -> Path:
        """Build a path to a non-existing file
        Raises:
            ValueError: If no path could be generated (shouldn't happen)
        Returns:
            Path: A new path for a screenshot to be saved at
        """
        nextPath = self.parent / self.nextName()
        if not nextPath.exists():
            return nextPath
        
        # Preexisting files were found, so we want to update the index so that it is equal to highest index on disk.
        # That way, we don't have to execute this fallback more than once in normal circumstances
        
        logger.info(f'File already exists. Searching for a free path. Path: {nextPath}')
        pattern = self.fileNamePattern('*')
        conflicts = self.parent.glob(pattern=pattern)
        self.nameIdx = self.getHighestIndex(conflicts)
        nextPath = self.parent / self.nextName()
        if nextPath.exists():
            raise ValueError('Unable to find free path for screenshot!')
        return nextPath
        
    def getHighestIndex(self, paths: list) -> int:
        """ Find the highest index present in the list
        Args:
            paths (list): A list of paths to screenshot files
        Returns:
            int: The highest index encountered or self.nameIdx. Whichever is higher.
        """
        pat = re.compile(self.fileNamePattern(r'(\d+)'))
        maxIdx = self.nameIdx
        for path in paths:
            m = pat.match(path.name)
            if m:
                idx = int(m.group(1))
                if idx > maxIdx:
                    maxIdx = idx
            else:
                logger.debug(f'Failed to match file to expected screenshot format: {path.name}')
        return maxIdx
    
    def fileNamePattern(self, idxStr: str) -> str:
        """ Create a file name, swapping in idxStr where the index should be
        Args:
            idxStr (str): What you want in index position. Intended to be the index or a regexp, depending on context.
        Returns:
            str: A standard screenshot name with idxStr at the index position
        """
        return PREFIX + self.dateStr + '_' + idxStr + SUFFIX
        
        