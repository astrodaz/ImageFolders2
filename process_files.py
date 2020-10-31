import os
from astropy.io import fits
import shutil
import datetime


class Log:

    def __init__(self):
        self.logfile = open('log.txt', 'wb')

    def Write(self, txt):
        # Get the date and time and write the text
        print(txt)

    def Init(self):
        # Get the date and time and write the first line
        print('start')

    def Fin(self):
        # Get the date and time and close the log
        print('end')


log_file = Log()


def main_process(Conf, object_folder=None):

    # There are two paths to follow in this process - either to create the object folder from the FITS headers
    # or use the name of the object provided. The moving of the files is the same, but if the files are of
    # different objects, they need to be managed individually as multiple object folders could be needed

    # Create a log object
    log_file.Init()
    log_file.Write('Options set are: ')
    log_file.Write('  Source Folder %s' % Conf.source_folder)
    log_file.Write('  Destination folder: %s ' % Conf.base_folder)
    log_file.Write('  Creating %i sub-folders:' % len(Conf.sub_folders))
    log_file.Write('  Use FITS Object: Yes' if Conf.top_level_object == 1 else '  Use FITS Object: No')
    log_file.Write('  Object Name: %s' % object_folder if object_folder != '' else '  Object Name: <not applicable>')
    log_file.Write('  Move Not Copy: Move ' if Conf.move_not_copy == 1 else '  Move Not Copy: Copy')
    log_file.Write('  File Operation: Overwrite' if Conf.write_skip == 1 else '  File Operation: Skip')
    log_file.Write('  Use SubType folders: Yes ' if Conf.create_subtypes == 1 else '  Use SubType folders: No')
    log_file.Write('  Generate Master Bias: Yes' if Conf.create_bias == 1 else '  Generate Master Bias: No')
    log_file.Write('  Generate Master Dark: Yes ' if  Conf.create_darks == 1 else '  Generate Master Dark: No')
    log_file.Write('  Calibrate Images: Yes' if Conf.calibrate == 1 else '  Calibrate Images: No ')
    log_file.Write('  Use Generated Masters: Yes ' if Conf.use_generated == 1 else '  Use Generated Masters: No')
    log_file.Write('  Supplied Dark Master: %s ' % Conf.dark_alt if Conf.dark_alt != '' else '  Alternate Dark: <not applicable>')
    log_file.Write('  Supplied Bias Master: %s ' % Conf.bias_alt if Conf.bias_alt != '' else '  Alternate Bias: <not applicable>')
    log_file.Write('####################################')

    full_obj_path = ''  # the full path to the object directory

    # Go to the Conf.source_folder directory and check there are files to process

    # Are we creating the object folder from the FITS header or from the supplied name?
    # From the header
    # LOOP
    #   Read the file and determine IMAGETYP
    #   If it's a LIGHT
    #       Check if the folder already exists
    #       if not create the object folder
    #       Are we using file subtypes?
    #       Yes
    #           Create them
    #           lights_destination = Lights
    #       No
    #           lights_destination = object folder
    #       Are we moving or copying the file
    #       Moving
    #           move image file from Conf.source_folder to lights_Conf.base_folderination
    #       Copying
    #           copy image file from Conf.source_folder to lights_Conf.base_folderination

    # From the supplied name
    # Check if the folder already exists
    # if not create the folder
    #   Are we using file subtypes?
    #   Yes
    #       Create them
    #       lights_destination = Lights
    #   No
    #       lights_destination = object folder
    # Are we moving or copying the file?
    #   Moving
    #       move image file from Conf.source_folder to lights_destination
    #   Copying
    #       copy image file from Conf.source_folder to lights_destination

    # Go to the Conf.source_folder folder
    os.chdir(Conf.source_folder)

    # Check there are files to process!
    if len(os.listdir(Conf.source_folder)) > 0:

        # We are reading the FITS files
        if Conf.top_level_object == 1:
            log_file.Write('Reading OBJECT from FITS Headers')
            list_of_objects = getObjectsList(Conf.source_folder, 'Light Frame')

            # For each object, create a folder
            for o in list_of_objects:
                log_file.Write('Processing object \"%s\"' % o)
                createObjectFolder(Conf.base_folder, o)

                # Sub types folders
                if Conf.create_subtypes == 1:
                    createSubTypes(Conf.base_folder, o)

                # Now the move/copy of the files
                # Set up the folders for different types
                # THIS WILL CHANGE WHEN THE CONFIGURABLE TYPES IS IMPLEMENTED
                lights_destination = os.path.join(os.path.join(Conf.base_folder, o), 'Lights')
                darks_destination = os.path.join(os.path.join(Conf.base_folder, o), 'Darks')
                bias_destination = os.path.join(os.path.join(Conf.base_folder, o), 'Bias')
                flats_destination = os.path.join(os.path.join(Conf.base_folder, o), 'Flats')

                # Now call the function to move the files
                filesMultiObjectMoveCopy(Conf.source_folder, lights_destination, o, 'Light Frame', Conf.write_skip)
                filesMultiObjectMoveCopy(Conf.source_folder, darks_destination, o, 'DARK', Conf.write_skip)
                filesMultiObjectMoveCopy(Conf.source_folder, bias_destination, o, 'Bias Frame', Conf.write_skip)
                filesMultiObjectMoveCopy(Conf.source_folder, flats_destination, o, 'FLAT', Conf.write_skip)

            # If we are MOVING, we now need to delete the source files
            if Conf.move_not_copy:
                deleteSourceFiles(Conf.source_folder)

        else:
            # We're using the supplied name
            # Create the object directory
            if not os.path.exists(os.path.join(Conf.base_folder, object_folder)):
                os.chdir(Conf.base_folder)
                os.mkdir(object_folder)
                log_file.Write('Object folder \"%s\" created' % object_folder)
            else:
                log_file.Write('Object folder \"%s\" found' % object_folder)

            # Are we using sub-types?
            if Conf.create_subtypes == 1:

                # Yes, so create the folders and set lights_destination
                os.chdir(Conf.base_folder)
                createSubTypes(Conf.base_folder, object_folder)

                # Set up the folders for different types
                lights_destination = os.path.join(os.path.join(Conf.base_folder, object_folder), 'Lights')
                darks_destination = os.path.join(os.path.join(Conf.base_folder, object_folder), 'Darks')
                bias_destination = os.path.join(os.path.join(Conf.base_folder, object_folder), 'Bias')
                flats_destination = os.path.join(os.path.join(Conf.base_folder, object_folder), 'Flats')

                # Now call the function to move the files
                log_file.Write('Moving Lights...')
                filesTypeMoveCopy(Conf.source_folder, lights_destination, Conf.move_not_copy, 'Light Frame', Conf.write_skip)
                log_file.Write('Moving Darks...')
                filesTypeMoveCopy(Conf.source_folder, darks_destination, Conf.move_not_copy, 'DARK', Conf.write_skip)
                log_file.Write('Moving Bias...')
                filesTypeMoveCopy(Conf.source_folder, bias_destination, Conf.move_not_copy, 'Bias Frame', Conf.write_skip)
                log_file.Write('Moving Flats...')
                filesTypeMoveCopy(Conf.source_folder, flats_destination, Conf.move_not_copy, 'FLAT', Conf.write_skip)

            else:
                # No, so destination will be the same as the object
                file_destination = os.path.join(Conf.base_folder, object_folder)
                log_file.Write('Files will be saved to \"%s\" ' % file_destination)

                # Now we can move or copy the files
                filesMoveCopy(Conf.source_folder, file_destination, Conf.move_not_copy, Conf.write_skip)

            # Now we can create any sub-folders needed

    else:
        log_file.Write('The source directory \"%s\" is empty! Nothing to process!' % Conf.source_folder)

    log_file.Fin()


def getObjectsList(src, file_type):
    """
        Because there could be mutiple objects in the FITS files, we'll need to gether this information first and
        then proceed to process in groups
    """
    # Move to the source directory and build a list of objects
    os.chdir(src)
    object_list = []

    # Valid extensions
    ext = ('.fit', '.fits', '.FIT', '.FITS')

    # Loop through the files
    for filename in os.listdir(src):
        if filename.endswith(ext):
            # Open the file with ASTROPY, and get the object
            with fits.open(filename) as hdul:
                hdr = hdul[0].header
                if hdr['IMAGETYP'] == file_type:
                    if hdr['OBJECT'] not in object_list:
                        object_list.append(hdr['OBJECT'])

    return object_list

"""    
def getObjectFromFile(src, dest, light_frame):

    # Valid extensions
    ext = ('.fit', '.fits', '.FIT', '.FITS')

    # Set up a temp variable for the current object, and files found
    current_obj = ''
    file_count = 0
    object_count = 0

    # Loop through the files
    for filename in os.listdir(src):

        # Move to source directory
        os.chdir(src)
        if filename.endswith(ext):

            # Open the file with ASTROPY, and get the object
            with fits.open(filename) as hdul:
                hdr = hdul[0].header

                # If it's not a light frame,
                if hdr['IMAGETYP'] == light_frame:
                    object_folder = hdr['OBJECT']

                    # Check if this is the same as the previous object
                    # Otherwise move on, no point in logging every occurrence
                    file_count += 1
                    if current_obj != object_folder:
                        object_count += 1
                        log_file.Write('Found OBJECT \"%s\" in \"%s\" ' % (object_folder, filename))
                        current_obj = object_folder

                        # Check if the folder exists, if not create it
                        os.chdir(dest)
                        if not os.path.exists(object_folder):
                            os.mkdir(object_folder)
                            log_file.Write('Object folder \"%s\" created' % object_folder)

                        # Are we using sub-types?
                        # We need to do this here, because there may be more than 1 object!
                        if Conf.create_subtypes == 1:
                            # Yes, so create the folders and set lights_destination
                            os.chdir(Conf.base_folder)
                            createSubTypes(Conf.base_folder, object_folder)

    log_file.Write('%i files found, %i object folders created' % (file_count, object_count))
"""


def createObjectFolder(dest, object_name):
    os.chdir(dest)
    if not os.path.exists(os.path.join(dest, object_name)):
        os.mkdir(object_name)
        log_file.Write('Object folder \"%s\" created' % object_name)
    else:
        log_file.Write('Object folder \"%s\" exists - skipping' % object_name)


def createSubTypes(dest, object_folder):
    # Move to the object folder
    os.chdir(os.path.join(dest, object_folder))
    log_file.Write('Create Image Type Sub-folders')
    # Create the folders
    try:
        if not os.path.exists('Lights'):
            os.mkdir('Lights')
            log_file.Write('  Lights folder created')
        else:
            log_file.Write('  Lights folder already exists')
        if not os.path.exists('Darks'):
            os.mkdir('Darks')
            log_file.Write('  Darks folders created')
        else:
            log_file.Write('  Darks folder already exists')
        if not os.path.exists('Bias'):
            os.mkdir('Bias')
            log_file.Write('  Bias folders created')
        else:
            log_file.Write('  Bias folder already exists')
        if not os.path.exists('Flats'):
            os.mkdir('Flats')
            log_file.Write('  Flats folders created')
        else:
            log_file.Write('  Flats folder already exists')

    except PermissionError:
        raise PermissionError
    except OSError:
        raise OSError


def filesMoveCopy(src, dest, mnc, write):
    # mnc = 1 means files will be MOVED - 0 means COPIED
    # Go to the source
    os.chdir(src)

    # Loop through the files
    ext = ('.fit', '.fits', '.FIT', '.FITS')
    ext_t = tuple(ext)
    for filename in os.listdir(src):

        # Is it a valid extension?
        if filename.endswith(ext):

            # Yep, log it an call the move_copy operation
            log_file.Write('Found file - \"%s\"' % filename)
            try:
                file_move_copy_op(src, dest, filename, mnc, write)
            except OSError:
                raise OSError


def file_move_copy_op(src, dest, filename, mnc, write):
    source_file = os.path.join(src, filename)
    dest_file = os.path.join(dest, filename)

    # Check if we are skipping existing files
    if write == 0 and os.path.exists(dest_file):
        log_file.Write('  Destination file \"%s\" exists - skipping' % dest_file)

    else:
        # We are overwriting files

        # If we are moving, move, else copy!
        if mnc == 1:

            # Because of potential inconsistencies, if the file exists and we are overwriting, we'll actually remove the destination file
            # file before the move operation, then move the source file
            if os.path.exists(dest_file):
                os.remove(dest_file)
                log_file.Write('  Destination file \"%s\" exists - overwriting' % dest_file)

            shutil.move(source_file, dest_file)
            log_file.Write('  File %s moved successfully to \"%s\"' % (filename, dest))

        else:
            # Same as before, if the file exists, we'll remove it then copy
            if os.path.exists(dest_file):
                os.remove(dest_file)
                log_file.Write('  Destination file \"%s\" file exists - copying' % dest_file)

            shutil.copyfile(source_file, dest_file)
            log_file.Write('  File \"%s\" copied successfully' % filename)


def filesTypeMoveCopy(src, dest, mnc, frame_type, write):

    # This proc needs to read the file type from the IMAGETYP header card
    # to determine where it should go

    os.chdir(src)
    # Loop through the files in the Conf.source_folder directory
    ext = ('.fit', '.fits', '.FIT', '.FITS')
    for filename in os.listdir(src):
        if filename.endswith(ext):

            # Open the file with ASTROPY, and get the object
            with fits.open(filename) as hdul:
                hdr = hdul[0].header
                typ = hdr['IMAGETYP']

                if typ.strip() == frame_type:
                    log_file.Write('  File found - %s' % filename)
                    file_move_copy_op(src, dest, filename, mnc, write)


def filesMultiObjectMoveCopy(src, dest, object_folder, file_type, write):

    """
        This will move or copy the files in a multi-object scenario
        Each object will get a copy of the darks/bias/flats

        Strategy here is that this function will copy the files from the source to the
        correct destination - ensuring we take notice of move_or_copy flag

        A seperate function will then remove the files - if they are being moved
    :return:
    """

    # Go to the source
    os.chdir(src)

    # Valid extensions
    ext = ('.fit', '.fits', '.FIT', '.FITS')

    # Loop through the files
    for filename in os.listdir(src):
        if filename.endswith(ext):
            # Open the file with ASTROPY, and get the object
            with fits.open(filename) as hdul:
                hdr = hdul[0].header
                if hdr['IMAGETYP'] == file_type:

                    if file_type == 'Light Frame' and hdr['OBJECT'] != object_folder:
                        pass
                    else:

                        # Build the full file paths
                        file_type_src = os.path.join(src, filename)
                        file_type_dest = os.path.join(dest, filename)

                        # No need to check for moving or copying, as this will be done in a different process
                        # once all the objects have been processed

                        # Are we overwriting or skipping?
                        if os.path.exists(file_type_dest) and write == 1:

                            # Overwrite
                            log_file.Write('  Destination \"%s\" exists - overwriting' % file_type_dest)
                            os.remove(file_type_dest)
                            shutil.copyfile(file_type_src, file_type_dest)

                        elif os.path.exists(file_type_dest) and write == 0:
                            log_file.Write('  Destination \"%s\" exists - skipping' % file_type_dest)

                        else:
                            # File does not exist at destination, so just move it
                            # Remember, there may be other objects needing the file, so we copy it for now
                            shutil.copyfile(file_type_src, file_type_dest)
                            log_file.Write('  File \"%s\" successfully moved' % file_type_dest)


def deleteSourceFiles(src):
    os.chdir(src)

    for f in os.listdir(src):

        if os.path.isfile(f):
            log_file.Write('  Removed file \"%s\"' % f)
            os.remove(f)


