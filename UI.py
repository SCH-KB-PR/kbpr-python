#TODO: Window sizing is not working properly. The window is not resizing to the correct size. The text is being cut off. The window should resize to fit the text.
#TODO: Make a configure values function and initialize the values there not every time UI element is used
#TODO: Add contraints like when size is "nagyplakát" the roll width should be 914.4mm
# Személyesen én magam nem tudok nagyon UI-t készíteni, ezért az itteni kód nagy része az eredeti kód + AI műve. Ellenőrzést, esetleges javításokat előre köszönöm.
import webbrowser
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from imgprocess import create_image, set_global_values
#This is similar to the original photoshop scripts presets. A parser may be needed so that updated values tranfer to both scripts
from presets import *

#Modified variables for the UI
displayedRollWidth = [round(x) for x in RollWidthsArray]

def smallest_shared_multiple(a: int, b: int) -> int:
    '''
    Finds the smallest shared multiple of two numbers
    
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The smallest shared multiple
    '''
    for i in range(1, a*b+1):
        if i % a == 0 and i % b == 0:
            return i

def pre_calc_grid():
    '''
    Calculates the grid layout for printing
    
    If no file is selected, it assumes sizes for 1 file
    
    Also sets the value for correctedQuantity, documentWidth, documentHeight, wasteMargin, rotate
    
    Returns:
        bool: Returns true if the grid fits the document
    '''
    #TODO: COPILOT WRITTEN CODE
    global actualQuantity, documentWidth, documentHeight, correctedQuantity, wasteMargin, rotate
    actualQuantity = quantityMultiplier * len(selectedFileList)

    paper_size = PaperSizesArray[paper_size_dropdown.current()]
    documentWidth = selectedRollWidth - margin * 2

    if paper_size['width'] <= documentWidth and paper_size['height'] <= documentWidth:
        waste_portrait = waste_check(documentWidth, paper_size, gutter)
        waste_landscape = waste_check(documentWidth, {'width': paper_size['height'], 'height': paper_size['width']}, gutter)
        print(f"Portrait waste: {waste_portrait}")
        print(f"Landscape waste: {waste_landscape}")
        rotate = waste_landscape < waste_portrait
    else:
        if paper_size['width'] <= documentWidth:
            rotate = False
        elif paper_size['height'] <= documentWidth:
            rotate = True
        else:
            print("Nem fér el!")
            return False

    column_width = paper_size['height'] if rotate else paper_size['width']
    row_height = paper_size['width'] if rotate else paper_size['height']
    global column_num, row_num
    column_num = column_num_calc(documentWidth, {'width': column_width, 'height': row_height}, gutter)
    row_num = int((actualQuantity + column_num - 1) // column_num)
    documentHeight = row_num * (row_height + gutter) - gutter
    if not multiFileMode:
        correctedQuantity = column_num * row_num
        quantity_correction_label.config(text=str(int(correctedQuantity)))
    #If given file list is missing or no amount added we are unable to predict
    elif len(selectedFileList) == 0 or quantityMultiplier == 0:
        correctedQuantity = 0
        quantity_correction_label.config(text=str(int(correctedQuantity)))
    else:
        ssm = smallest_shared_multiple(len(selectedFileList), column_num)
        correctedQuantity = ssm
        while quantityMultiplier * len(selectedFileList) > correctedQuantity:
            correctedQuantity += ssm
        correctedQuantity = correctedQuantity / len(selectedFileList)
        text = str(int(correctedQuantity)) + "x=>" + str(int(correctedQuantity)*len(selectedFileList))+"db"
        quantity_correction_label.config(text=text)
    wasteMargin = (documentWidth - (column_num * (column_width + gutter) - gutter)) / 2
    print(10*'\n')
    print(f"Darabszám: {correctedQuantity if quantityCorrectionEnabled else actualQuantity} db")
    print(f"Forgatás: {'Igen' if rotate else 'Nem'}")
    print(f"Rács: {column_num} × {row_num}")
    print(f"Rácsméret: {round(column_width)} × {round(row_height)} mm")
    print(f"Dokumentum: {round(documentWidth)} × {round(documentHeight)} mm")

    return True

def waste_check(document_width, paper_size, gutter):
    '''
    Calculates the waste for a given paper size and document width
    Args:
        documentWidth (float): The width of the document
        paperSize (dict): The size of the paper
        gutter (float): The gutter size
    Returns:
        float: The waste size
    '''
    #TODO: COPILOT WRITTEN CODE
    column_width = paper_size['width']
    column_num = column_num_calc(document_width, paper_size, gutter)
    waste = document_width - (column_num * (column_width + gutter) - gutter)
    return waste

def column_num_calc(document_width, paper_size, gutter):
    '''
    Calculates the number of columns for a given paper size and document width
    Args:
        documentWidth (float): The width of the document
        paperSize (dict): The size of the paper
        gutter (float): The gutter size
    Returns:
        int: The number of columns
    '''
    #TODO: COPILOT WRITTEN CODE
    column_width = paper_size['width']
    return int((document_width-paper_size['width']) // (column_width + gutter) + 1)


def open_link(url):
    '''
    Opens a link in the default browser
    
    Args:
        url (str): The URL to open
    '''
    webbrowser.open(url)

#TODO: Figure out if needed (got it by AI which made the OG UI into python)
def calc_aspect_ratio(file):
    # Placeholder for calculating the aspect ratio
    pass

def parse_hu_float(text: str) -> float:
    '''
    This function makes sure that margin and unique sizes can be read wheather they are written with a comma or a dot
    
    Args:
        text (str): The text to parse
    Returns:
        float: The float value of the text
    '''
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return 0.0

def toggle_multi_file_mode():
    '''
    Toggle between single and multi file mode
    '''
    global multiFileMode, selectedFileList, selectedFile
    multiFileMode = not multiFileMode
    mode_select_text.config(text="Mappa:" if multiFileMode else "Fájl:")
    quantity_text.config(text="Szorzó:" if multiFileMode else "Mennyiség:")
    quantity_unit.config(text="x" if multiFileMode else "db")
    selectedFileList = []
    selectedFile = None
    path_text.config(text="")
    if multiFileMode:
        #Place the special button
        special_button.grid(row=1, column=0, padx=5, pady=5)
        #Make the window bigger to fit the new components
        mainWindow.geometry(f"{mainWindow.winfo_width()}x{mainWindow.winfo_height()+40}")
    else:
        #Get rid of special size button
        special_button.grid_remove()
        #Make the window smaller by the size of the removed components
        mainWindow.geometry(f"{mainWindow.winfo_width()}x{mainWindow.winfo_height()-40}")
        
    pre_calc_grid()


def is_image(path) -> bool:
    '''
    Checks if the file is an image
    Upgraded version of os.path.isfile
    '''
    if not os.path.isfile(path):
        return False
    if not path.lower().endswith(supportedFileFormats):
        return False
    return True

def browse_file():
    '''
    Browse for a file or folder
    Sets up selectedFile or selectedFolder and selectedFileList
    '''
    global selectedFile, selectedFolder, selectedFileList
    path = os.path.abspath(__file__)
    if multiFileMode:
        selectedFolder = filedialog.askdirectory(title="Válassz mappát",initialdir=path)
        selectedFileList = []  # Normally fetch files in the directory
        #Count files in the directory
        if selectedFolder:
            selectedFileList = [os.path.join(selectedFolder, f) for f in os.listdir(selectedFolder) if is_image(os.path.join(selectedFolder, f))]        
        path_text.config(text=selectedFolder+f" ({len(selectedFileList)} fájl)")
    else:
        selectedFile = filedialog.askopenfilename(title="Megnyitás", filetypes=[("Képek", supportedFileFormats)], initialdir=path)
        selectedFileList = [selectedFile] if selectedFile else []
        path_text.config(text=selectedFile)
    pre_calc_grid()
    
    # Resize the window because the text might be too long
    # Calculate the required width based on the length of the text
    text_length = len(path_text.cget("text"))
    char_width = 8  # Approximate width of a character in pixels
    padding = 20  # Additional padding
    new_width = max(text_length * char_width + padding, 325+padding+100)#325 is frame.winfo_width after initializing window for first time I have no idea why and how can get this number back after changing once
    #if new:width > monitor width, set it to monitor width and shorten the text
    if new_width > mainWindow.winfo_screenwidth():
        new_width = mainWindow.winfo_screenwidth()
        path_text.config(text=path_text.cget("text")[:int(new_width/char_width)-5]+"...")
        mainWindow.geometry(f"+{mainWindow.winfo_screenwidth()-new_width}+{mainWindow.winfo_y()}")
    # Resize the window based on the new width
    mainWindow.geometry(f"{new_width}x{mainWindow.winfo_height()}")

def roll_width_changed():
    '''
    This function is called when the roll width dropdown is changed
    '''
    pre_calc_grid()

def change_quantity(p)->bool:
    '''
    This function is responsible for changing and checking the validity the quantity
    
    Args:
        p (str): The input string
    Returns:
        bool: True if the input is an integer, False otherwise
    '''
    for char in p:
        if not char.isdigit():
            return False
    #If it is more than 1 character long, it can't start with 0
    if len(p)==2 and p[0] == '0':
        return False
    global quantityMultiplier
    if p == '':
        quantityMultiplier = 0
    else:
        quantityMultiplier = int(p)
    pre_calc_grid()
    return True

def change_margin(p)->bool:
    '''
    This function is responsible for changing and checking the validity the margin
    
    Args:
        p (str): The input string
    Returns:
        bool: True if the input is a float, False otherwise
    '''
    #If missing empty string messes up the function (IDK why)
    if len(p) == 0:
        return True
    for char in p:
        if not char.isdigit() and char != '.' and char != ',':
            return False
    #If it is more than 1 character long, it can't start with 0
    if len(p)==2 and p[0] == '0':
        return False
    #Can't start with a dot or a comma
    if len(p) == 1 and p[0] == '.' or p[0] == ',':
        return False
    #Can't have more than one dot or comma
    if p.count('.')+p.count(',') > 1:
        return False
    global margin
    margin = parse_hu_float(p)
    return True

def quantity_correction_checkbox_click():
    '''
    Toggle the quantity correction
    '''
    global quantityCorrectionEnabled
    quantityCorrectionEnabled = not quantityCorrectionEnabled

def ok_click():
    '''
    This function will start the script
    '''
    
    #Initialize the variables
    global selectedFile, selectedFolder, selectedFileList, selectedRollWidth, selectedPaperSize, quantityMultiplier, multiFileMode, quantityCorrectionEnabled, gutter, guide, circleMask, ppi
    selectedRollWidth = RollWidthsArray[roll_width_dropdown.current()]
    selectedPaperSize = PaperSizesArray[paper_size_dropdown.current()]
    if quantityCorrectionEnabled:
        quantityMultiplier = int(quantity_correction_label.cget("text"))
    else:
        quantityMultiplier = int(quantity_field.get())
    
    '''
    gutter = parse_hu_float(gutter_field.get())
    guide = guide_checkbox.get()
    circleMask = circle_mask_checkbox.get()
    ppi = ResolutionArray[ppi_dropdown.current()]
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
    print(f"Gutter: {gutter}")
    print(f"Guide: {guide}")
    print(f"Circle Mask: {circleMask}")
    print(f"PPI: {ppi}")
    
    #TODO: Implement submit logic and change the command
    set_global_values(selected_file_list_ui=selectedFileList,
                      selected_file_ui=selectedFile,
                      selected_folder_ui=selectedFolder,
                      selected_roll_width_ui=selectedRollWidth,
                      selected_paper_size_ui=selectedPaperSize,
                      quantity_multiplier_ui=quantityMultiplier,
                      multifile_mode_ui=multiFileMode,
                      margin_ui=margin,
                      quantity_correction_enabled_ui=quantityCorrectionEnabled,
                      gutter_ui=gutter,
                      guide_ui=guide,
                      circle_mask_ui=circleMask,
                      ppi_ui=ppi)
    pre_calc_grid()
    create_image(document_height=documentHeight,row_count=row_num,column_count=column_num,rotation=rotate)
    
if __name__ == "__main__":
    # Initialize the main window
    mainWindow = tk.Tk()
    mainWindow.title("KBPR script")
    mainWindow.resizable(False, False)

    # Main Frame
    frame = tk.Frame(mainWindow)
    frame.pack(padx=10, pady=10)

    # Mode Panel
    mode_panel = tk.LabelFrame(frame, text="Fájl")
    mode_panel.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    # Mode Selection
    mode_select_group = tk.Frame(mode_panel)
    mode_select_group.pack(fill="x", pady=(0, 10))
    tk.Label(mode_select_group, text="Több fájl:", width=propertyWidth//10).pack(side="left")
    mode_checkbox = tk.Checkbutton(mode_select_group, command=lambda: toggle_multi_file_mode())
    mode_checkbox.pack(side="left")

    # Feedback Button
    feedback_button = tk.Button(mode_select_group, text="Hibajelzés", command=lambda: open_link("https://github.com/SCH-KB-PR/kbpr-ps/issues/new/choose"))
    feedback_button.pack(side="right")
    help_button = tk.Button(mode_select_group, text="Súgó", command=lambda: open_link("https://github.com/SCH-KB-PR/kbpr-ps/wiki"))
    help_button.pack(side="right")

    # Path Selection
    path_group = tk.Frame(mode_panel)
    path_group.pack(fill="x", pady=(0, 10))
    mode_select_text = tk.Label(path_group, text="Fájl:", width=propertyWidth//10)
    mode_select_text.pack(side="left")
    path_text = tk.Label(path_group, text="")
    path_text.pack(side="left", fill="x", expand=True)
    path_browse_button = tk.Button(path_group, text="Tallózás...", command=lambda: browse_file())
    path_browse_button.pack(side="right")

    # Paper Panel
    paper_panel = tk.LabelFrame(frame, text="Papír")
    paper_panel.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    roll_width_label = tk.Label(paper_panel, text="Papírtekercs:")
    roll_width_label.grid(row=0, column=0, pady=5, sticky="e")
    roll_width_dropdown = Combobox(paper_panel, values=displayedRollWidth, width=8,validatecommand=(roll_width_changed))
    roll_width_dropdown.grid(row=0, column=1, padx=5, pady=5)
    roll_width_dropdown.current(0)
    roll_width_unit =tk.Label(paper_panel, text="mm")
    roll_width_unit.grid(row=0, column=2, pady=5)
    
    
    margin_label = tk.Label(paper_panel, text="Margó:", width=propertyWidth//10+1)
    margin_label.grid(row=0, column=3, pady=5, sticky="e")
    margin_field = tk.Entry(paper_panel, width=8, validate="key", validatecommand=(mainWindow.register(change_margin), "%P"))
    margin_field.grid(row=0, column=4, pady=5)
    margin_field.insert(0, defaultMarginWidth)
    margin_unit = tk.Label(paper_panel, text="mm")
    margin_unit.grid(row=0, column=5, pady=5)

    paper_size_label = tk.Label(paper_panel, text="Papírméret:", width=propertyWidth//10+1)
    paper_size_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    paper_size_dropdown = Combobox(paper_panel, values=[s["name"] for s in PaperSizesArray], width=longDataWidth//10+2)
    paper_size_dropdown.grid(row=1, column=1, padx=5, pady=5)
    paper_size_dropdown.current(4)

    # Quantity Panel
    quantity_panel = tk.LabelFrame(frame, text="Mennyiség")
    quantity_panel.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    
    #Needs to be defined first in panel
    quantity_correction_labelname = tk.Label(quantity_panel, text="Korrekció:")
    quantity_correction_labelname.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    quantity_correction_checkbox = tk.Checkbutton(quantity_panel, command=quantity_correction_checkbox_click)
    quantity_correction_checkbox.grid(row=0, column=4, padx=5, pady=5)
    quantity_correction_label = tk.Label(quantity_panel, text="20", width=propertyWidth//10+1)
    quantity_correction_label.grid(row=0, column=5, padx=5, pady=5)

    quantity_text = tk.Label(quantity_panel, text="Mennyiség:", width=propertyWidth//10+1)
    quantity_text.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    quantity_field = tk.Entry(quantity_panel, width=8,validate="key", validatecommand=(mainWindow.register(change_quantity), "%P"))
    quantity_field.insert(0, str(quantityMultiplier))
    quantity_field.grid(row=0, column=1, padx=5, pady=5)
    quantity_unit = tk.Label(quantity_panel, text="db")
    quantity_unit.grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    special_button = tk.Button(quantity_panel, text="Speciális...", command=lambda: messagebox.showinfo("Speciális mennyiség", "Ez a funkció még nincs implementálva."))
    special_button.grid(row=1, column=0, padx=5, pady=5)
    #Not visible by default, only when the checkbox is checked
    special_button.grid_remove()
    
    # Layout Panel
    layout_panel = tk.LabelFrame(frame, text="Elrendezés")
    layout_panel.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

    # Submit Group
    submit_group = tk.Frame(frame)
    submit_group.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
    submit_button = tk.Button(submit_group, text="OK", command=ok_click)
    submit_button.pack(side="right")
    cancel_button = tk.Button(submit_group, text="Mégse", command=mainWindow.quit)
    cancel_button.pack(side="right")

    #TODO: ADDED for testing
    pre_calc_grid()
    
    #Get the size of the frame and make the window fit it
    mainWindow.update()
    mainWindow.geometry(f"{frame.winfo_width()+20}x{frame.winfo_height()+15}")
    mainWindow.mainloop()