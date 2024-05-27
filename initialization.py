import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from pathlib import Path
import warnings
import csv
from tkinter import ttk
warnings.filterwarnings("ignore", category=DeprecationWarning)

rootfolder = ""
pdf_directory = ""
previous_message = ""
selected_image_filename = ""
left_value_frame = None
right_value_frame = None
scroll_y = None
canvas = None
separator = None
num_converted_files = 0
jpg_counter = 0

#Button paths
extractGif = "\\buttons\\ExtractGif.gif"
resetIMG = "\\buttons\\window.png"
dataIMG = "\\buttons\\data.png"
pdftojpgIMG = "\\buttons\\pdftojpg.png"
iconIMG = "\\buttons\\window1.ico"
selectFileButtonIMG = "\\buttons\\SelectFile.png"
selectFolderButtonIMG = "\\buttons\\SelectFolder.png"
convertButtonIMG = "\\buttons\\ConvertButton.png"
cancelButtonIMG = "\\buttons\\CancelButton.png"
extractDataImageButtonIMG = "\\buttons\\ExtractData.png"
convertMoreButtonIMG = "\\buttons\\ConvertMoreButton.png"
extractConvertedImageButtonIMG = "\\buttons\\Extract.png"
resetButtonIMG = "\\buttons\\ResetButton.png"
csvIMG = "\\buttons\\ExtractDataIcon.png"
csvButtonIMG = "\\buttons\\CSVButton.png"
okButtonIMG = "\\buttons\\OkButton.png"
confirmIconIMG = "\\buttons\\Confirm.ico"
errorIconIMG = "\\buttons\\Error.ico"

#ocr paths

#Path to your yolov5 training
yolov5_path = ""

#Path to where you wanna store the results
tess_results_directory = ""