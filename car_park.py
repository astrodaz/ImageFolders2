import wx
from config import Config
Conf = Config()


class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(800, 600), style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)

        self.InitUI()
        self.DefaultSettings()
        self.Centre()
        self.LoadValues()
        self.UpdateUI()

    def InitUI(self):

        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        # Source of input images
        wx.StaticBox(self.panel, label='Image Source Folder', size=(420, 60), pos=(20, 20))
        self.sourceFolder = wx.TextCtrl(self.panel, size=(300, -1), pos=(40, 40))
        btnSource = wx.Button(self.panel, label='Choose', pos=(350, 40))

        # Folders Box
        wx.StaticBox(self.panel, label='Output Folders', size=(420, 320), pos=(20, 80))

        # Base directory
        wx.StaticText(self.panel, label='Output directory', pos=(40, 100))
        self.baseFolder = wx.TextCtrl(self.panel, size=(300, -1), pos=(40, 120))
        btnBase = wx.Button(self.panel, label='Choose', pos=(350, 120))

        # Sub Folders
        self.btnAdd = wx.Button(self.panel, label='Add Sub Folder', pos=(40, 160))
        self.btnRem = wx.Button(self.panel, label='Remove Sub Folder', pos=(180, 160))
        self.lstFolders = wx.ListBox(self.panel, size=(340, 180), pos=(40, 200))

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_BUTTON, (16, 16))
        self.btnFolderUp = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=bmp, pos=(400, 200))
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_BUTTON, (16, 16))
        self.btnFolderDown = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=bmp, pos=(400, 240))

        # Options Box
        wx.StaticBox(self.panel, label='Image Object', size=(300, 80), pos=(460, 20))
        self.chkCreateObject = wx.CheckBox(self.panel, label='Read FITS files', pos=(480, 40))
        tipObject = wx.ToolTip('This will create folders for the given object e.g. \"base_folder\\M51\" - based on the FITS header. '
                               'if not selected, the Object name must be entered')
        self.chkCreateObject.SetToolTip(tipObject)
        wx.StaticText(self.panel, label='Object:', pos=(600, 40))
        self.objectText = wx.TextCtrl(self.panel, size=(80, 20), pos=(640, 40))
        btnFITS = wx.Button(self.panel, label='FITS Options', pos=(640, 60))

        # File Operation
        wx.StaticBox(self.panel, label='File Operation Options', size=(300, 80), pos=(460, 80))
        self.chkMoveCopy = wx.CheckBox(self.panel, label='Move original files, not copy', pos=(480, 100))
        tipMove = wx.ToolTip('Default behavior is to COPY the original files from the source folder. This will force a MOVE instead')
        self.chkMoveCopy.SetToolTip(tipMove)

        self.chkOverwrite = wx.RadioButton(self.panel, label='Overwrite', pos=(500, 130), style=wx.RB_GROUP)
        self.chkSkip = wx.RadioButton(self.panel, label='Skip', pos=(580, 130))

        self.chkCreateTypeFolders = wx.CheckBox(self.panel, label='Create sub folders for image types', pos=(480, 180))
        tipTypes = wx.ToolTip('Create a set of folders for each image type - e.g. Lights, Flats, Darks, Bias - based on the FITS headers, under the Object folder. '
                              'If not selected, all image files will be placed in the root of the Object folder')
        self.chkCreateTypeFolders.SetToolTip(tipTypes)

        self.btnFitsTypes = wx.Button(self.panel, label='Types', pos=(700, 180), size=(40, 20))
        tipTypes = wx.ToolTip('Edit the keywords used in your FITS Headers for the different image types\ne.g. \"FLAT\" or \"Flat Frames\"')
        self.btnFitsTypes.SetToolTip(tipTypes)

        self.chkCreateMasterBias = wx.CheckBox(self.panel, label='Create a Master Bias', pos=(480, 210))
        tipBias = wx.ToolTip('Uses the individual BIAS frames to create a master Bias')
        self.chkCreateMasterBias.SetToolTip(tipBias)

        self.chkCreateMasterDark = wx.CheckBox(self.panel, label='Create a Master Dark', pos=(480, 240))
        tipDark = wx.ToolTip('Uses the individual Dark Frames to create a master Dark, based on common duration, and calibrated with the master Bias')
        self.chkCreateMasterDark.SetToolTip(tipDark)

        self.chkCalibrate = wx.CheckBox(self.panel, label='Calibrate Lights and Flats', pos=(480, 270))
        tipCalibrate = wx.ToolTip('Enable this to auto calibrate the Lights and Flats')
        self.chkCalibrate.SetToolTip(tipCalibrate)

        self.chkUseMasters = wx.CheckBox(self.panel, label='Use generated Master Dark and Bias frames', pos=(480, 300))
        tipUseMasters = wx.ToolTip('Enable this to use the generated Master Dark and Bias frames. If unselected, specify alternate Master frames to use')
        self.chkUseMasters.SetToolTip(tipUseMasters)

        self.masterDarkAlt = wx.StaticText(self.panel, label=' Choose Master Dark', pos=(480, 330), size=(150, 25), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.masterDarkAlt.SetBackgroundColour(wx.LIGHT_GREY)

        self.masterBiasAlt = wx.StaticText(self.panel, label=' Choose Master Bias', pos=(480, 360), size=(150, 25), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.masterBiasAlt.SetBackgroundColour(wx.LIGHT_GREY)

        wx.StaticBox(self.panel, size=(740, 100), pos=(20, 410))
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        info_text = 'Set the various folders and options here, and then be sure to Save them! When you are ready, click the Execute'
        info_text += '\nbutton or you can run from the command-line by using an /r switch. Of course, you need to set the right options'
        info_text += '\nfor that to work correctly! For example, if you don\'t select the option to autogenerate the object, you will need'
        info_text += '\nto supply it with an /o=<object_name> switch. These are the only two switches needed'

        t1 = wx.StaticText(self.panel, label=info_text, size=(700, -1), pos=(30, 430))
        t1.SetFont(font)

        self.btnExecuteNow = wx.Button(self.panel, label='Execute &Now', pos=(30, 520), size=(200, -1))
        tipExecute = wx.ToolTip('Go! Run! Execute! Begin! Start! What else can I say...?!')
        self.btnExecuteNow.SetToolTip(tipExecute)

        btnCancel = wx.Button(self.panel, label='E&xit', pos=(680, 520), size=(80, -1))
        tipCancel = wx.ToolTip('Do not save changes and Exit!')
        btnCancel.SetToolTip(tipCancel)

        # Event bindings
        self.Bind(wx.EVT_CHECKBOX, self.createObject, self.chkCreateObject)
        self.Bind(wx.EVT_CHECKBOX, self.createSubFolders, self.chkCreateTypeFolders)
        self.Bind(wx.EVT_CHECKBOX, self.createBias, self.chkCreateMasterBias)
        self.Bind(wx.EVT_CHECKBOX, self.createDark, self.chkCreateMasterDark)
        self.Bind(wx.EVT_CHECKBOX, self.calibrateFiles, self.chkCalibrate)
        self.Bind(wx.EVT_CHECKBOX, self.useGenerated, self.chkUseMasters)
        self.Bind(wx.EVT_CHECKBOX, self.moveNotCopy, self.chkMoveCopy)
        self.masterDarkAlt.Bind(wx.EVT_LEFT_DOWN, self.chooseMasterDark, self.masterDarkAlt)
        self.masterBiasAlt.Bind(wx.EVT_LEFT_DOWN, self.chooseMasterBias, self.masterBiasAlt)
        self.Bind(wx.EVT_BUTTON, self.executeNow, self.btnExecuteNow)

        self.Bind(wx.EVT_BUTTON, self.closeProgram, btnCancel)
        self.Bind(wx.EVT_BUTTON, self.folderUp, self.btnFolderUp)
        self.Bind(wx.EVT_BUTTON, self.folderDown, self.btnFolderDown)
        self.Bind(wx.EVT_BUTTON, self.sourceChooser, btnSource)
        self.Bind(wx.EVT_BUTTON, self.baseChooser, btnBase)
        self.Bind(wx.EVT_BUTTON, self.addFolder, self.btnAdd)
        self.Bind(wx.EVT_BUTTON, self.remFolder, self.btnRem)
        self.Bind(wx.EVT_LISTBOX, self.listClicked, self.lstFolders)
        self.Bind(wx.EVT_RADIOBUTTON, self.fileOperation)
        self.lstFolders.Bind(wx.EVT_LEFT_DCLICK, self.editSubFolder, self.lstFolders)
        self.Bind(wx.EVT_TEXT, self.updateSource, self.sourceFolder)
        self.Bind(wx.EVT_TEXT, self.updateBase, self.baseFolder)
        self.Bind(wx.EVT_TEXT, self.updateObject, self.objectText)

    def DefaultSettings(self):
        # Set up the controls first time around
        self.lstFolders.Clear()
        self.btnRem.Enable(False)
        self.btnFolderUp.Enable(False)
        self.btnFolderDown.Enable(False)
        self.btnExecuteNow.Enable(False)
        self.objectText.Enable(False)
        self.masterDarkAlt.Enable(False)
        self.masterBiasAlt.Enable(False)

    def createObject(self, event):
        if self.chkCreateObject.GetValue() == wx.CHK_UNCHECKED:
            Conf.create_object = 0
            self.objectText.Enable(True)
        else:
            Conf.create_object = 1
            self.objectText.Enable(False)
        self.UpdateUI()

    def updateObject(self, event):
        self.UpdateUI()

    def moveNotCopy(self, event):
        Conf.move_not_copy = 1 if self.chkMoveCopy.GetValue() == wx.CHK_CHECKED else 0
        self.UpdateUI()

    def fileOperation(self, event):
        rb = event.GetEventObject()
        Conf.write_skip = 1 if rb.GetLabel() == 'Overwrite' else 0
        self.UpdateUI()

    def createSubFolders(self, event):
        Conf.create_subtypes = 1 if self.chkCreateTypeFolders.GetValue() == wx.CHK_CHECKED else 0
        self.UpdateUI()

    def createBias(self, event):
        Conf.create_bias = 1 if self.chkCreateMasterBias.GetValue() == wx.CHK_CHECKED else 0
        self.UpdateUI()

    def createDark(self, event):
        Conf.create_darks = 1 if self.chkCreateMasterDark.GetValue() == wx.CHK_CHECKED else 0
        self.UpdateUI()

    def calibrateFiles(self, event):
        Conf.calibrate = 1 if self.chkCalibrate.GetValue() == wx.CHK_CHECKED else 0
        if Conf.calibrate == 0:
            self.chkUseMasters.Enable(False)
            self.masterBiasAlt.Enable(False)
            self.masterDarkAlt.Enable(False)
        else:
            self.chkUseMasters.Enable(True)
            self.masterBiasAlt.Enable(True)
            self.masterDarkAlt.Enable(True)
        self.UpdateUI()

    def useGenerated(self, event):
        Conf.use_generated = 1 if self.chkUseMasters.GetValue() == wx.CHK_CHECKED else 0
        self.masterBiasAlt.Enable(True) if self.chkUseMasters.GetValue() == wx.CHK_UNCHECKED else self.masterBiasAlt.Enable(False)
        self.masterDarkAlt.Enable(True) if self.chkUseMasters.GetValue() == wx.CHK_UNCHECKED else self.masterDarkAlt.Enable(False)
        self.UpdateUI()

    def editSubFolder(self, event):
        sel = self.lstFolders.GetSelection()
        old_text = self.lstFolders.GetString(sel)
        new_folder = wx.TextEntryDialog(self.panel, 'Enter the folder name', 'Edit Folder Name', value=old_text)
        if new_folder.ShowModal() == wx.ID_OK:

            # Update the list in the Config Options
            self.lstFolders.SetString(sel, new_folder.GetValue())
            Conf.old_sub = old_text
            print(old_text)
            Conf.new_sub = new_folder.GetValue()
            Conf.replace_old_new()

        self.UpdateUI()

    def updateSource(self, event):
        Conf.source_folder = self.sourceFolder.Value
        self.UpdateUI()

    def updateBase(self, event):
        Conf.base_folder = self.baseFolder.Value
        self.UpdateUI()

    def chooseMasterDark(self, event):
        dialog = wx.FileDialog(self.panel, message='Select the Master Dark file', wildcard='FITS Files (*.fit;*;fits;*.FIT;*.FITS)|*.fit;*.fits;*.FIT;*.FITS',
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            self.masterDarkAlt.SetLabel(dialog.GetPath())
            Conf.dark_alt = dialog.GetPath()
        self.UpdateUI()

    def chooseMasterBias(self, event):
        dialog = wx.FileDialog(self.panel, message='Select the Master Bias file', wildcard='FITS Files (*.fit;*;fits;*.FIT;*.FITS)|*.fit;*.fits;*.FIT;*.FITS',
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            self.masterBiasAlt.SetLabel(dialog.GetPath())
            Conf.bias_alt = dialog.GetPath()
        self.UpdateUI()

    def folderUp(self, event):
        # Move the folder up by using a temp item
        to_move_id = self.lstFolders.GetSelection()
        to_move_string = self.lstFolders.GetString(to_move_id)
        Conf.old_sub = to_move_string
        temp = to_move_id - 1
        temp_string = self.lstFolders.GetString(temp)
        Conf.new_sub = temp_string
        self.lstFolders.SetString(temp, to_move_string)
        self.lstFolders.SetString(to_move_id, temp_string)
        self.lstFolders.SetSelection(temp)
        self.listClicked(event)
        self.lstFolders.Update()

        # Now update the Conf object
        Conf.swap_old_new()

        self.UpdateUI()

    def folderDown(self, event):
        # Move the folder up by using a temp item
        to_move_id = self.lstFolders.GetSelection()
        to_move_string = self.lstFolders.GetString(to_move_id)
        Conf.old_sub = to_move_string
        temp = to_move_id + 1
        temp_string = self.lstFolders.GetString(temp)
        Conf.new_sub = temp_string
        self.lstFolders.SetString(temp, to_move_string)
        self.lstFolders.SetString(to_move_id, temp_string)
        self.lstFolders.SetSelection(temp)
        self.listClicked(event)
        self.lstFolders.Update()

        Conf.swap_old_new()

        self.UpdateUI()

    def addFolder(self, event):
        # Do something
        new_folder = wx.TextEntryDialog(self.panel, 'Enter the folder name', 'Add New Folder')
        if new_folder.ShowModal() == wx.ID_OK:
            self.lstFolders.Append(new_folder.GetValue())
            Conf.sub_folders = self.lstFolders.GetStrings()
        self.UpdateUI()

    def remFolder(self, event):
        confirm = wx.MessageBox('Confirm you want to remove this folder?', 'Confirm Deletion', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        if confirm == wx.OK:
            self.lstFolders.Delete(self.lstFolders.GetSelection())
            Conf.sub_folders = self.lstFolders.GetStrings()
        self.btnRem.Enable(False)
        self.UpdateUI()

    def sourceChooser(self, event):
        dialog = wx.DirDialog(self.panel, message='Select the Image Source directory', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.sourceFolder.SetValue(dialog.GetPath())
        self.UpdateUI()

    def baseChooser(self, event):
        dialog = wx.DirDialog(self.panel, message='Select the Image Source directory', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.baseFolder.SetValue(dialog.GetPath())
        self.UpdateUI()

    def listClicked(self, event):
        sel = self.lstFolders.GetSelection()
        self.btnRem.Enable(True)
        if self.lstFolders.GetCount() > 1:
            if sel == 0:
                self.btnFolderUp.Enable(False)
                self.btnFolderDown.Enable(True)
            elif sel == self.lstFolders.GetCount() - 1:
                self.btnFolderUp.Enable(True)
                self.btnFolderDown.Enable(False)
            else:
                self.btnFolderUp.Enable(True)
                self.btnFolderDown.Enable(True)
        else:
            self.btnFolderUp.Enable(False)
            self.btnFolderDown.Enable(False)
        self.UpdateUI()

    def closeProgram(self, event):
        self.Close()

    def LoadValues(self):
        # Set the flag to indicate initial loading
        Conf.first_run = True

        Conf.load_values()

        # Now check the config object and load up the values!
        self.sourceFolder.SetValue(Conf.source_folder) if Conf.source_folder != '' else ''

        if len(Conf.sub_folders) > 0:
            for f in Conf.sub_folders:
                self.lstFolders.Append(f)

        self.baseFolder.SetValue(Conf.base_folder) if Conf.base_folder != '' else ''

        self.chkCreateObject.SetValue(wx.CHK_CHECKED) if Conf.top_level_object == 1 else wx.CHK_UNCHECKED

        self.objectText.Enable(True) if Conf.top_level_object == 0 else False

        self.chkMoveCopy.SetValue(wx.CHK_CHECKED) if Conf.move_not_copy == 1 else wx.CHK_UNCHECKED

        self.chkOverwrite.SetValue(True) if Conf.write_skip == 1 else self.chkSkip.SetValue(True)

        self.chkCreateTypeFolders.SetValue(wx.CHK_CHECKED) if Conf.create_subtypes == 1 else wx.CHK_UNCHECKED

        self.chkCreateMasterBias.SetValue(wx.CHK_CHECKED) if Conf.create_bias == 1 else wx.CHK_UNCHECKED

        self.chkCreateMasterDark.SetValue(wx.CHK_CHECKED) if Conf.create_darks == 1 else wx.CHK_UNCHECKED

        self.chkCalibrate.SetValue(wx.CHK_CHECKED) if Conf.calibrate == 1 else wx.CHK_UNCHECKED

        if Conf.use_generated == 1:
            self.chkUseMasters.SetValue(wx.CHK_CHECKED)
            self.masterBiasAlt.Enable(False)
            self.masterDarkAlt.Enable(False)
        else:
            self.chkUseMasters.SetValue(wx.CHK_UNCHECKED)
            self.masterBiasAlt.Enable(True)
            self.masterDarkAlt.Enable(True)
            self.masterDarkAlt.SetLabel(Conf.dark_alt) if Conf.dark_alt != '' else ''
            self.masterBiasAlt.SetLabel(Conf.bias_alt) if Conf.bias_alt != '' else ''

        # Finished loading, turn off the flag so any changes are captured
        Conf.first_run = False
        self.UpdateUI()

    def UpdateUI(self):
        ERR_COUNT = 0

        ERR_COUNT += 1 if self.sourceFolder.GetValue() == '' else ERR_COUNT
        ERR_COUNT += 1 if self.baseFolder.GetValue() == '' else ERR_COUNT
        ERR_COUNT += 1 if self.chkCreateObject.GetValue() == wx.CHK_UNCHECKED and self.objectText.GetValue() == '' else ERR_COUNT

        # Check if we can enable the Execute button
        self.btnExecuteNow.Enable(True) if ERR_COUNT == 0 else self.btnExecuteNow.Enable(False)

    def executeNow(self, event):
        from process_files import main_process
        try:
            main_process(Conf, object_folder=self.objectText.GetValue())
        except FileExistsError:
            print('path exists')
