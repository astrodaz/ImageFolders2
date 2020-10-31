import wx
import sys
from class_main_window import MainWindow


def main():

    if len(sys.argv) == 1:
        app = wx.App()
        ex = MainWindow(None, title='Image Folder Generator - V2')
        ex.Show()
        app.MainLoop()
    else:
        if sys.argv[1] != '/r':
            sys.stderr.write('Invalid Command Line Argument - expected /r')
        else:
            sys.stdout.write('Running....')


if __name__ == '__main__':
    main()


# TODO - The keywords for the different IMAGETYP need to be editable, so users can enter their own - e.g. FLATS or Flat Frames
# TODO - Add a simple FITS Header view for the image files - also auto extract these values! - needs to be a configurable number of types
# TODO - Add list of expected filetypes, and indicate if they have FITS headers or keywords in filenames
# TODO - Add folders for filter as an option - needs to be configurable number of filters
# TODO - Different source folders for the image types
# TODO Error handling for the file operations


"""  DONE


#  TODO - whenc opying or moving files, check that they exist
#  TODO - Option to overwrite or skip if files exist
# TODO - Update the config class to save itself at each change and do away with the check when exiting
# TODO - Finish adding the overwrite/skip into the options config file, set the Radio button accordingly on Load
# TODO - In the 'process_file' use the Config object rather than passing all the prameters

"""
