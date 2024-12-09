#TODO: Create a prepare image function that can be called to prepare an image. In the for loop this can change the used image when multiple files are used
import cv2
import numpy as np
from tkinter import filedialog
import os
from presets import *
#from UI import pre_calc_grid
global inch_to_mm
inch_to_mm = 25.4


def dummy_check()->bool:
    '''
    Checks if the user should be able to print
    
    Returns:
        bool: Returns true if printing is possible
    '''
    global selectedFile, selectedFolder, selectedFileList, selectedRollWidth, selectedPaperSize, quantityMultiplier, multiFileMode, quantityCorrectionEnabled, gutter, guide, circleMask, ppi
    if (not multiFileMode and selectedFile == None):
        print("Nem választottál ki fájlt!")
        return False
    
    if (multiFileMode and selectedFolder == None):
        print("Nem választottál ki mappát!")
        return False
    
    if (len(selectedFileList)== 0):
        print("A kiválasztott mappa nem tartalmaz fájlokat!")
        return False
    '''
    if (not pre_calc_grid()):
        print("Nem fér el a kiválasztott méretű papíron!")
        return False
    if (document_height > maxDocumentHeight):
        print("Túl nagy a dokumentum!")
        return False
    

    if (document_height < minDocumentHeight):
        #choice = confirm("A dokumentum mérete kisebb mint a minimum nyomtatási méret (" + minDocumentHeight + " mm), ez némi extra felesleggel jár. Biztosan folytatod?");
        if (not choice):
            return False  
    '''
    #TODO: Check if the PaperSize fits the image
    return True

def mm2px(mm, dpi=72) -> int:
    '''
    Converts millimeters to pixels
    Args:
        mm (float): The length in millimeters
        ppi (int): The pixels per inch (default 72)
        
    Returns:
        int: The length in pixels
    '''
    return round(mm * dpi / inch_to_mm)

def px2mm(px, dpi=72) -> float:
    '''
    Converts pixels to millimeters
    Args:
        px (int): Number of pixels
        ppi (int): The pixels per inch (default 72)
        
    Returns:
        float: The length in mm
    '''
    return px * inch_to_mm / dpi
   
def cv_resize(img, size_key="A4", dpi=300):
    '''
    Resizes an image to the specified size
    
    Also attempts to choose the best interpolation method
    
    inter_cubic: For upscaling
   
    inter_area: For downscaling 
    
    Args:
        img (cv2.Image): The image to resize
        size str: The size to resize to
        
    Returns:
        cv2.Image: The resized image
    '''
    seg = PaperSizes[size_key]["width"]
    x = mm2px(seg, dpi)
    seg = PaperSizes[size_key]["height"]
    y = mm2px(seg, dpi)
    downscale = PaperSizes[size_key]["width"]*PaperSizes[size_key]["height"] < img.shape[0]*img.shape[1]
    if downscale:
        return cv2.resize(img, (x, y), interpolation=cv2.INTER_AREA)
    return cv2.resize(img, (x, y), interpolation=cv2.INTER_CUBIC)

def set_global_values(selected_file_ui, selected_folder_ui, selected_file_list_ui, selected_roll_width_ui, selected_paper_size_ui, quantity_multiplier_ui, multifile_mode_ui, quantity_correction_enabled_ui, gutter_ui, guide_ui, circle_mask_ui, ppi_ui,margin_ui):
    '''
    This function will set the global values to the values set in the UI
    '''
    global selectedFile, selectedFolder, selectedFileList, selectedRollWidth, selectedPaperSize, quantityMultiplier, multiFileMode, margin,quantityCorrectionEnabled, gutter, guide, circleMask, ppi
    selectedFile = selected_file_ui
    selectedFolder = selected_folder_ui
    selectedFileList = selected_file_list_ui
    selectedRollWidth = selected_roll_width_ui
    selectedPaperSize = selected_paper_size_ui
    quantityMultiplier = quantity_multiplier_ui
    multiFileMode = multifile_mode_ui
    margin = margin_ui
    quantityCorrectionEnabled = quantity_correction_enabled_ui
    gutter = gutter_ui
    guide = guide_ui
    circleMask = circle_mask_ui
    ppi = ppi_ui
    ppi = 600#TODO: Remove this line

def create_image(document_height,row_count,column_count,rotation):
    '''
    This function will be responsible for creating the final image
    
    For now, it will create an image with pre set values, but later it will be able to create an image from the values set in the UI
    '''
    global selectedFile, selectedFolder, selectedFileList, selectedRollWidth, selectedPaperSize, quantityMultiplier, multiFileMode,margin, quantityCorrectionEnabled, gutter, guide, circleMask, ppi
    #Stopping unimplemented ways to run
    if multiFileMode or selectedPaperSize['name']=='Körmatrica 70mm' or selectedPaperSize['name']=='Körmatrica 49mm' or selectedPaperSize['name']=="Kitűző" or selectedPaperSize['name']=="Egyébb":
        print('Unimplemented parameters')
        return
    if not dummy_check():
        return
    dpi = ppi
    filepath = selectedFile
    os.chdir(os.path.dirname(filepath))
    filepath = os.path.basename(filepath)
    img = cv2.imread(filepath)
    #TODO: Figure out and read document height from UI
    #Create a blank image with only white pixels for base document
    gutter = 2
    height = selectedPaperSize['width'] if rotation else selectedPaperSize['height']
    new_image = np.full(((row_count*mm2px(height,dpi=dpi))+((row_count-1)*mm2px(gutter,dpi=dpi)), mm2px(selectedRollWidth, dpi=dpi), 3), 255, np.uint8)
    print(mm2px(document_height,dpi=dpi))
    if rotation:
        print(mm2px(selectedPaperSize['width'], dpi=dpi))
    else:
        print(mm2px(selectedPaperSize['height'], dpi=dpi))
    print(mm2px(2,dpi=dpi))
    #Testcode was: newImage = np.full((mm2px(67.4 * inch_to_mm,dpi=dpi), mm2px(24 * inch_to_mm, dpi=dpi), 3), 255, np.uint8)
    img = cv_resize(img, selectedPaperSize['name'], dpi=dpi)
    if rotation:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    '''
    #Print the selected values
    print(f"File: {selectedFile}")
    print(f"Folder: {selectedFolder}")
    print(f"File List: {selectedFileList}")
    print(f"Roll Width: {selectedRollWidth}")
    print(f"Paper Size: {selectedPaperSize}")
    print(f"Quantity Multiplier: {quantityMultiplier}")
    print(f"Multiply File Mode: {multiFileMode}")
    print(f"Quantity Correction Enabled: {quantityCorrectionEnabled}")
    print(f"Margin: {margin}")
    print(f"Gutter: {gutter}")
    print(f"Guide: {guide}")
    print(f"Circle Mask: {circleMask}")
    print(f"PPI: {ppi}")
    '''
    ycoordstart = mm2px(0)
    for _ in range (row_count):
        xcoordstart = mm2px(margin,dpi=dpi)
        for __ in range (column_count):        
            new_image[ycoordstart:ycoordstart+img.shape[0], xcoordstart:xcoordstart+img.shape[1]] = img
            xcoordstart += mm2px(gutter,dpi=dpi)
            xcoordstart += img.shape[1]
        ycoordstart += img.shape[0] + mm2px(gutter,dpi=dpi)
    #Set the name and path of the image
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    #Change the selected folder to the folder where the image is about to be saved
    os.chdir(os.path.dirname(filepath))
    #Save the image
    filepath = os.path.basename(filepath)
    cv2.imwrite(filepath, new_image)
if __name__=="__main__":
    print("Run main in UI.py")
    