# -*- coding: utf8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from NumberedCollagesCore import *
from threading import Thread
from time import sleep

LAST_FOLDER_FILE = "last.dat"
CHOOSE_FOLDER_MSG = "(nie wybrano...)"
START_COLLAGE_BTN = "Utwórz kolaże"

class TarninowyKolaz:
    def __init__(self, master):
        self.master = master
        master.title("Numerowany Kolaż")
        master.iconbitmap("appicon.ico")
        master.resizable(0,0)

        self.folderPathLabelText = StringVar()
        self.collageButtonText = StringVar()
        self.folderPath = self.loadFolderLocation()
        ttk.Style().configure("TButton", padding=10)
        self.logoFrame = ttk.Frame(master, padding=10)
        self.logoFrame.pack(side="top", anchor="n")
        self.folderSelectFrame = ttk.Frame(master, padding=20)
        self.folderSelectFrame.pack(side="top", anchor="nw")
        self.createCollageFrame = ttk.Frame(master, padding=20)
        self.createCollageFrame.pack(side="top", anchor="n")


        self.logoImage = PhotoImage(file="logo.gif")
        self.logoLabel = ttk.Label(
            self.logoFrame,
            image=self.logoImage,
            padding=10)
        self.logoLabel.pack(side="top", anchor="n")

        self.folderPathLabel = ttk.Label(
            self.folderSelectFrame,
            textvariable=self.folderPathLabelText,
            wraplength=300,
            padding=10)
        self.folderPathLabel.pack(side="left")

        self.selectFolderButton = ttk.Button(
            self.folderSelectFrame,
            text="Wybierz folder",
            command=self.selectFolder,)
        self.selectFolderButton.pack(side="right")

        self.createCollageButton = ttk.Button(
            self.createCollageFrame,
            textvariable=self.collageButtonText,
            command=self.createCollages)
        self.collageButtonText.set(START_COLLAGE_BTN)
        self.createCollageButton.pack(side="top", anchor="nw")

    def selectFolder(self):
        dialogText = "Wybierz folder ze zdjęciami do kolażu"
        folder = ""
        if not self.folderPath:
            folder = filedialog.askdirectory(title=dialogText)
        else:
            folder = filedialog.askdirectory(
                initialdir=self.folderPath,
                title=dialogText)

        if not folder:
            self.folderPathLabelText.set(CHOOSE_FOLDER_MSG)
            self.noFolderMessageBox()
        else:
            self.folderPath = folder
            self.folderPathLabelText.set(self.folderPath)
            self.saveFolderLocation()

    def createCollages(self):
        if not self.folderPath:
            return

        imageSelector = ImageSelector(self.folderPath)
        imageSelector.createPictureList()

        if not imageSelector.collagePicturesExist():
            self.noImagesMessageBox()
            return


        CollageCreator(imageSelector).createCollages()

        return



    def noFolderMessageBox(self):
        messagebox.showinfo("Info", "Nie wybrano żadnego folderu")

    def noImagesMessageBox(self):
        messagebox.showinfo("Info", "Wybrany folder nie zawiera plików ze zdjęciami.\nWymagane pliki: *.jpg, *.png")

    def saveFolderLocation(self):
        try:
            if self.folderPath:
                file = open(LAST_FOLDER_FILE, "w+")
                file.write(self.folderPath)
                file.close()
        except Exception as e:
            errorMessage("Unable to save " + LAST_FOLDER_FILE, e)

    def loadFolderLocation(self):
        try:
            file = open(LAST_FOLDER_FILE, "r")
            folder = file.read()
            file.close()
            self.folderPathLabelText.set(folder)
            return folder
        except Exception as e:
            errorMessage("Unable to read from " + LAST_FOLDER_FILE, e)
            self.folderPath = ""
            self.folderPathLabelText.set(CHOOSE_FOLDER_MSG)




root = Tk()
mainWindow = TarninowyKolaz(root)
root.mainloop()
