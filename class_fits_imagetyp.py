import wx
import pickle
import os


class FitsImageTypeWindow(wx.Dialog):

    def __init__(self, parent, title):
        super(FitsImageTypeWindow, self).__init__(parent, title=title)

        self.image_types = {
            'flats': '',
            'bias': '',
            'darks': '',
            'lights': ''
        }

        self.InitUI()
        self.Centre()
        # self.LoadValues()
        # self.UpdateUI()

    def InitUI(self):
        self.panel = wx.Panel(self, wx.ID_ANY)
        wx.StaticText(self.panel, label='Flats keyword', pos=(20, 20))
        self.flats_keyword = wx.TextCtrl(self.panel, size=(150, -1), pos=(120, 17))

        wx.StaticText(self.panel, label='Darks keyword', pos=(20, 50))
        self.darks_keyword = wx.TextCtrl(self.panel, size=(150, -1), pos=(120, 47))

        wx.StaticText(self.panel, label='Bias keyword', pos=(20, 80))
        self.bias_keyword = wx.TextCtrl(self.panel, size=(150, -1), pos=(120, 77))

        wx.StaticText(self.panel, label='Lights keyword', pos=(20, 110))
        self.lights_keyword = wx.TextCtrl(self.panel, size=(150, -1), pos=(120, 107))

        self.btnSave = wx.Button(self.panel, label='Save Values', pos=(20, 160))
        self.btnCancel = wx.Button(self.panel, label='Cancel', pos=(120, 160))

        self.Bind(wx.EVT_BUTTON, self.closeWindow, self.btnCancel)
        self.Bind(wx.EVT_BUTTON, self.__save_values, self.btnSave)

        self.__load_values()
        self.__update_ui()

    def __load_values(self):
        if os.path.exists('imagetyp.pkl'):
            with open('imagetyp.pkl', 'rb') as pkl_file:
                self.image_types = pickle.load(pkl_file)

        else:
            self.image_types['flats'] = 'Flat Frames'
            self.image_types['bias'] = 'Bias Frames'
            self.image_types['darks'] = 'Dark Frames'
            self.image_types['lights'] = 'Light Frames'

    def __save_values(self, event):
        self.image_types['flats'] = self.flats_keyword.Value
        self.image_types['darks'] = self.darks_keyword.Value
        self.image_types['bias'] = self.bias_keyword.Value
        self.image_types['lights'] = self.lights_keyword.Value

        with open('imagetyp.pkl', "wb") as pkl_file:
            pickle.dump(self.image_types, pkl_file)

        self.closeWindow(event)

    def __update_ui(self):
        self.flats_keyword.SetValue(self.image_types['flats'])
        self.lights_keyword.SetValue(self.image_types['lights'])
        self.bias_keyword.SetValue(self.image_types['bias'])
        self.darks_keyword.SetValue(self.image_types['darks'])

    def closeWindow(self, event):
        self.Close()


# TODO -    Simple relationship for Flats, Darks, Bias, Light frames
#           Saved/Loaded to a Pickle object
# TODO -    Set up a folder in My Documents for saving data to
