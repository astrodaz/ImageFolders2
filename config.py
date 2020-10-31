import pickle

config = {
    'SOURCE_FOLDER': '',
    'BASE_FOLDER': '',
    'FOLDER_LIST': [],
    'CREATE_OBJECT': 0,
    'MOVE_NOT_COPY': 0,
    'WRITE_SKIP': 0,
    'CREATE_SUB_TYPES': 0,
    'CREATE_BIAS': 0,
    'CREATE_DARK': 0,
    'CALIBRATE': 0,
    'USE_GENERATED': 0,
    'BIAS_ALT': '',
    'DARK_ALT': ''
}

###############################################
#   NOW NEED TO CREATE AN IMPORT/UPDATE FUNCTION
#   FOR WHEN THE OPTIONS FILE CHANGES
###############################################


class Config:

    def __init__(self):
        self.__firstRun = True
        self.options = config
        self.__old_sub = ''
        self.__new_sub = ''
        self.load_values()

    def replace_old_new(self):
        # Swap the old value for the new value
        if self.__old_sub != '' and self.__new_sub != '':
            old_id = self.options['FOLDER_LIST'].index(self.__old_sub)
            self.options['FOLDER_LIST'][old_id] = self.__new_sub
            self.__new_sub = ''
            self.__old_sub = ''
            self.save_values()

    def swap_old_new(self):
        # Swap the two values around
        old_id = self.options['FOLDER_LIST'].index(self.__old_sub)
        new_id = self.options['FOLDER_LIST'].index(self.__new_sub)
        t = self.options['FOLDER_LIST'][old_id]
        self.options['FOLDER_LIST'][old_id] = self.__new_sub
        self.options['FOLDER_LIST'][new_id] = t
        self.__new_sub = ''
        self.__old_sub = ''
        self.save_values()

    def save_values(self):
        try:
            pkl_file = open('config.pkl', "wb")
            pickle.dump(self.options, pkl_file)
            pkl_file.close()
        except OSError:
            raise OSError

    def load_values(self):
        try:
            pkl_file = open('config.pkl', 'rb')
            self.options = pickle.load(pkl_file)
        except FileNotFoundError:
            pass
        except OSError:
            raise OSError

    @property
    def first_run(self):
        return self.__firstRun

    @first_run.setter
    def first_run(self, value):
        if type(value) is bool:
            self.__firstRun = value

    @property
    def source_folder(self):
        return self.options['SOURCE_FOLDER']

    @source_folder.setter
    def source_folder(self, value):
        self.options['SOURCE_FOLDER'] = value
        if not self.__firstRun:
            self.save_values()

    @property
    def base_folder(self):
        return self.options['BASE_FOLDER']

    @base_folder.setter
    def base_folder(self, value):
        self.options['BASE_FOLDER'] = value
        if not self.__firstRun:
            self.save_values()

    @property
    def sub_folders(self):
        return self.options['FOLDER_LIST']

    @sub_folders.setter
    def sub_folders(self, folder_list):
        self.options['FOLDER_LIST'] = folder_list
        if not self.__firstRun:
            self.save_values()

    @property
    def old_sub(self):
        return None

    @old_sub.setter
    def old_sub(self, old):
        self.__old_sub = old

    @property
    def new_sub(self):
        return None

    @new_sub.setter
    def new_sub(self, new):
        self.__new_sub = new

    @property
    def top_level_object(self):
        return self.options['CREATE_OBJECT']

    @top_level_object.setter
    def top_level_object(self, value):
        if value == 1 or value == 0:
            self.options['CREATE_OBJECT'] = value
            self.save_values()

    @property
    def move_not_copy(self):
        return self.options['MOVE_NOT_COPY']

    @move_not_copy.setter
    def move_not_copy(self, value):
        if value == 1 or value == 0:
            self.options['MOVE_NOT_COPY'] = value
            self.save_values()

    @property
    def write_skip(self):
        return self.options['WRITE_SKIP']

    @write_skip.setter
    def write_skip(self, value):
        if value == 1 or value == 0:
            self.options['WRITE_SKIP'] = value
            self.save_values()

    @property
    def create_subtypes(self):
        return self.options['CREATE_SUB_TYPES']

    @create_subtypes.setter
    def create_subtypes(self, value):
        if value == 1 or value == 0:
            self.options['CREATE_SUB_TYPES'] = value
            self.save_values()

    @property
    def create_bias(self):
        return self.options['CREATE_BIAS']

    @create_bias.setter
    def create_bias(self, value):
        if value == 1 or value == 0:
            self.options['CREATE_BIAS'] = value
            self.save_values()

    @property
    def create_darks(self):
        return self.options['CREATE_DARK']

    @create_darks.setter
    def create_darks(self, value):
        if value == 1 or value == 0:
            self.options['CREATE_DARK'] = value
            self.save_values()

    @property
    def calibrate(self):
        return self.options['CALIBRATE']

    @calibrate.setter
    def calibrate(self, value):
        if value == 1 or value == 0:
            self.options['CALIBRATE'] = value
            self.save_values()

    @property
    def use_generated(self):
        return self.options['USE_GENERATED']

    @use_generated.setter
    def use_generated(self, value):
        if value == 1 or value == 0:
            self.options['USE_GENERATED'] = value
            self.save_values()

    @property
    def create_object(self):
        return self.options['CREATE_OBJECT']

    @create_object.setter
    def create_object(self, value):
        self.options['CREATE_OBJECT'] = value
        self.save_values()

    @property
    def bias_alt(self):
        return self.options['BIAS_ALT']

    @bias_alt.setter
    def bias_alt(self, value):
        self.options['BIAS_ALT'] = value
        self.save_values()

    @property
    def dark_alt(self):
        return self.options['DARK_ALT']

    @dark_alt.setter
    def dark_alt(self, value):
        self.options['DARK_ALT'] = value
        self.save_values()
