global supportedFileFormats
#TODO: Implement , ".pdf" file support
#TODO: Test every imagetype
supportedFileFormats = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp", ".svg")

global uicHeight, defaultMarginWidth, propertyWidth, dataWidth, unitWidth, miscWidth, longDataWidth, buttonWidth

# Constants
uicHeight = 20
defaultMarginWidth = 5
propertyWidth = 80
dataWidth = 60
unitWidth = 35
miscWidth = 10
longDataWidth = dataWidth + defaultMarginWidth + unitWidth
buttonWidth = 80

global RollWidthsArray, PaperSizes, ResolutionArray, PaperSizesArray

# Mock Values for Dropdowns
RollWidthsArray = [609.6, 914.4]#, 1066.8, 1117.6 #Unused rollsizes

PaperSizes = {
    "A0": { "name": "A0", "width": 841, "height": 1189 },
    "A1": { "name": "A1", "width": 594, "height": 841 },
    "A2": { "name": "A2", "width": 420, "height": 594 },
    "A3": { "name": "A3", "width": 297, "height": 420 },
    "A4": { "name": "A4", "width": 210, "height": 297 },
    "A5": { "name": "A5", "width": 148, "height": 210 },
    "A6": { "name": "A6", "width": 105, "height": 148 },
    "A7": { "name": "A7", "width": 74, "height": 105 },
    "POSTER": { "name": "Nagyplakát", "width": 914, "height": 1600 },
    #TODO: Add missing sizes
    #"STICKER70": { "name": "Körmatrica 70mm", "width": 72, "height": 72 },
    #"STICKER49": { "name": "Körmatrica 49mm", "width": 51, "height": 51 },
    #"BADGE": { "name": "Kitűző", "width": 72, "height": 72 },
    #"OTHER": { "name": "Egyéb...", "width": 100, "height": 100 }
}

PaperSizesArray = list(PaperSizes.values())

ResolutionArray = [300, 600]

global fileAspectLock, selectedFileAspect, selectedFile, selectedFolder, selectedFileList, multiFileMode, selectedRollWidth, selectedPaperSize, quantityMultiplier, quantityCorrectionEnabled, gutter, guide, circleMask, ppi

# Setting variables
fileAspectLock = True                  # aspect ratio lock is enabled by default
selectedFileAspect = 1                 # width / height, 1 by default
selectedFile = None                    # selected file, null by default
selectedFolder = None                  # selected folder, null by default
selectedFileList = [None]              # list of files in the selected folder
multiFileMode = False                  # multi file mode disabled by default
selectedRollWidth = RollWidthsArray[0] # default roll width = 610
selectedPaperSize = PaperSizes["A4"]   # default paper size = A4
quantityMultiplier = 20                # default quantity multiplier
quantityCorrectionEnabled = False      # quantity correction disabled by default
gutter = 2                             # default gutter = 2 mm
guide = True                           # guide is enabled by default
circleMask = False                     # circle mask is disabled by default
ppi = ResolutionArray[0]               # default resolution = 300 dpi

global margin, maxDocumentHeight, minDocumentHeight

# Plotter dependent settings
# Don't touch unless you know what you are doing
margin = 0                             # default margin = 0 mm, the printer will add its 3mm by itself
maxDocumentHeight = 18000              # 18 meters (as if photoshop could handle that lmao)
minDocumentHeight = 101.6              # 101.6 mm = 4 inches