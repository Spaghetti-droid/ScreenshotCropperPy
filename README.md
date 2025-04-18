# ScreenshotCropper

Designate a screen or part of a screen, and take screenshots of that area by pressing F12 that are saved automatically to a folder that you chose previously. 

This tool is intended for situations where you want to take a screenshot without having to spend time selecting the area to capture and the destination folder. For instance, it is quite useful when taking screenshots of games which are not associated to a client with inbuilt screen capture functionality (such as Steam).

This is a complete remake in Python of the Java version of the project which can be found in the https://github.com/Spaghetti-droid/ScreenshotCropper and https://github.com/Spaghetti-droid/ScreenshotCropperGUI repositories.

## Installation
### Using the exe files
Copy the file you want to use to where you want it. I'd advise putting it in a dedicated folder, as it will create some extra files for logs and saving preferences.
### Using sources
Copy the source files where you want them.
#### Dependencies
This program requires the following dependencies:    
- pynput
- pyautogui

Install these using
    
    pip install <dependency name>


Note that pyautogui has a large number of its own dependencies that will be installed along with it.

## Usage

### Graphical user interface

To start up the graphical user interface, simply double-click on the screenshot-cropper-gui .py or .exe file. This should open up a user interface that looks like this

![image info](./Documentation/gui.png)

In this interface, we can see the following elements:

#### Event box

This area displays various events. For example it records when we've started to listen for presses of F12 or when a screenshot is saved.

#### Destination Folder
 
 You can use the file browser or the text box to specify where you want to save the screenshots. If you give a path to a folder that doesn't exist, it will be created when the 'Start' button is clicked.

#### Screenshot area 
   
 In this section you specify which part of your screen(s) you want to capture. All quantities are measured in pixels from the top left of the capturable area.
 - X Offset: Moves the captured area along the x-axis. For instance, an X Offset of 10 would move the area 10 pixels to the right
 - Y Offset: Moves the captured area along the y-axis. For instance, a Y Offset of 10 would move the area 10 pixels down
 - Width: How wide the screenshot should be
 - Height: How high the screenshot should be
  
#### Save button
   
   Saves the provided settings to be reused next time the program is run.

#### Start/Stop button
   
   Start listening for screenshots. Once this is pressed, any press of F12 will trigger a screenshot. Click this button again to stop listening.

#### Close button 
   
   Closes the window, and stops listening. Does exactly the same thing as the cross in the top right.

### Command-line interface

All documentation below uses the python files. The executables should be called in the command line directly, without going through python.

      $ python screenshot-cropper.py -h
        usage: screenshot-cropper.py [-h] [-l LOGLEVEL] [-p PATH] [-x X] [-y Y] [-W WIDTH] [-H HEIGHT] [-s]

        Listen for screenshots, crop them to the desired format, and save them to disk

        options:
          -h, --help            show this help message and exit
          -l LOGLEVEL, --log-level LOGLEVEL
                                Level of detail for logged events. Currently: WARNING
          -p PATH, --path PATH  Path to the folder where the screenshots will be saved. Currently: ./Screenshots.
          -x X, --x-offset X    x offset from top left of the captured area. Currently: 0.
          -y Y, --y-offset Y    y offset from top left of the captured area. Currently: 0.
          -W WIDTH, --width WIDTH
                                Width of the captured area. Currently: 1920.
          -H HEIGHT, --height HEIGHT
                                Height of the captured area. Currently: 1080.
          -s, --save            Save the provided options, so that they become the new defaults.

At its simplest ScreenshotCropper can be used with no arguments:
        
    $ python screenshot-cropper.py
    
    Using Options:{ Folder path: ./Screenshots, X Offset: 0, Y Offset: 0, width: 1920, height: 1080 }
    Listening. Press F12 to take screenshots. Press enter when focused on this window to stop.

If you want to use a different value for a parameter than the default, you can specify it with the corresponding option. Here's an example where we change the path:

    python screenshot-cropper.py -p  f:/Pictures/ScreenShots/Test

If we want to make the options we provide the new defaults, we can provide the -s option:

    python screenshot-cropper.py -sp  f:/Pictures/ScreenShots/Test

After this, all calls which don't specify a value for -p will use our new path by default.

#### Taking screenshots

Once the program is running, any press of F12 will cause a screenshot to be saved to the disk. In order to stop saving screenshots, just press Enter in the console.

## Generating the exe files
The exe files can be generated using pyinstaller. In the project root directory, execute:
    
    pyinstaller -F screenshot-cropper.py
    pyinstaller -F screenshot-cropper-gui.py

## Rationale for remakaking ScreenshotCropper
While the java version of the program functions well enough most of the time, it suffers from issues which are caused by its interference with the clipboard. Notably copying and pasting images while the java screenshot cropper is active isn't possible, which can cause a level of confusion in the person affected. Relatedly, the handling of the clipboard in java does not lend itself well to the purpose of this program, which leads to strange manipulations that are needed to ensure we notice when a screenshot has been taken.

As such, it would be better to not rely on the clipboard at all, and rather listen for a key press (such as F12) and take the screenshot when a press is detected. Unfortunately, java does not seem to have an obvious way of doing that without being focused on the gui of the application. Hence my decision to recode the program in Python.

For the moment the python version of the program seems to work well, with the caveat that the generated exe is 1000 times bigger than the jar generated by the java version (likely due to the dependency on pyautogui).

## Known issues
### Key presses are not relayed to the program
Some games/apps seem to block the transmission of inputs to the program when they are in focus. I'm guessing it might be due to some form of anti-cheat. So far I only know of one game that does this (Honkai Star Rail), but I imagine that there are others I don't know about at time of writing.

For current releases, I see 2 solutions to this issue

1. Use the  [java version](https://github.com/Spaghetti-droid/ScreenshotCropperGUI) of this program
2. Move the focus outside of the game (ie on a 2nd screen) when you want to take a screenshot
