print("Starting generatorUI")

from os import system
from os import listdir
from os import path
from sys import platform

import json

import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

from PIL import ImageTk
from PIL import Image
print("tkinter imported correctly")

import dialogueGenerator
print("dialogue generator imported correctly")

#TODO:
# Add offset preview
# Fix line spacing being dependant on character height?
# - See ImageDraw.multiline_text. - possibly fixed? no longer able to reproduce
# Two-frame mode
# Add mp3 file support to UI

root = tk.Tk()
root.title("Animated textbox generator")
root.iconbitmap("icon.ico")
print("tkinter window created")

#ANCHOR general function and data registration
frameSettings = {"padx": 3, "pady": 3, "borderwidth": 3, "relief": "groove"}

def validateInteger(val):
	if val.isdigit():
		return True
	return False

intValidator = root.register(validateInteger)

# Left side, reserved for box content
contentFrame = tk.Frame(root)
contentHeader = tk.Label(contentFrame, text="Textbox content:")

# Middle, reserved for settings
generalOptionsFrame = tk.Frame(root)

# Right side, for portrait and font stuffs

portraitFontOptionsFrame = tk.Frame(root)

#-------------------------------------------------------------------------------
# Variable declaration - for future stuffs

useImageVar = tk.IntVar(value=1)
useSoundVar = tk.IntVar(value=0)

pathUniverse = tk.StringVar()
pathCharacter = tk.StringVar()
pathExpression = tk.StringVar()

#-------------------------------------------------------------------------------
#ANCHOR Save-related functions

def saveSettings():
	settings = {
		"animationDelay": portraitDelayEntry.get(),
		"frameTime": frametimeEntry.get(),
		"outputName": fileNameEntry.get(),
		"textOffsetx": textOffsetx.get(),
		"textOffsety": textOffsety.get(),
		"portraitOffsetx": portraitOffsetx.get(),
		"portraitOffsety": portraitOffsety.get(),
		"portraitScale": portraitScaleField.get(),
		"textColor": dialogueGenerator.color,
		"specialDelays": dialogueGenerator.delays
	}

	with open("generator_settings.json", mode="w") as settingFile:
		json.dump(settings, settingFile)

def loadSettings():
	if path.isfile("generator_settings.json"):
		with open("generator_settings.json", "r") as settingFile:
			settings = json.load(settingFile)

		if "animationDelay" in settings:
			portraitDelayEntry.delete(0, tk.END)
			portraitDelayEntry.insert(0, settings["animationDelay"])
		if "frameTime" in settings:
			frametimeEntry.delete(0, tk.END)
			frametimeEntry.insert(0, settings["frameTime"])
		if "outputName" in settings:
			fileNameEntry.delete(0, tk.END)
			fileNameEntry.insert(0, settings["outputName"])

		textOffsetx.set(settings["textOffsetx"] if "textOffsetx" in settings else None)
		textOffsety.set(settings["textOffsety"] if "textOffsety" in settings else None)
		portraitOffsetx.set(settings["portraitOffsetx"] if "portraitOffsetx" in settings else None)
		portraitOffsety.set(settings["portraitOffsety"] if "portraitOffsety" in settings else None)
		portraitScaleField.set(settings["portraitScale"] if "portraitScale" in settings else None)
		if "textColor" in settings:
			coltup = tuple(settings["textColor"])
			textEntry.config(fg = '#{0:02x}{1:02x}{2:02x}'.format(*coltup))
			dialogueGenerator.color = coltup
		if "specialDelays" in settings:
			dialogueGenerator.delays = settings["specialDelays"]
			charListVar.set(getCharDelayFunction())

#-------------------------------------------------------------------------------
#ANCHOR Dialogue creation function
def createFunction():
	dialogueGenerator.portraitInterval = int(portraitDelayEntry.get())
	dialogueGenerator.frametime = int(frametimeEntry.get())

	filename = fileNameEntry.get()
	dialogueGenerator.outputFileName = filename

	threeLineOffset = (0, 10) if threeLineVar.get() == 1 else (0, 0)

	dialogueGenerator.xoffset = int(textOffsetx.get()) + threeLineOffset[0]
	dialogueGenerator.yoffset = int(textOffsety.get()) + threeLineOffset[1]
	dialogueGenerator.portraitxoffset = int(portraitOffsetx.get())
	dialogueGenerator.portraityoffset = int(portraitOffsety.get())

	scaleFactor = portraitScaleField.get()
	textboxcontent = textEntry.get("1.0", "4.40").rstrip()

	expression = None
	if useImageVar.get() == 1:
		expression = pathExpression.get()

	blip = None
	if useSoundVar.get() == 1:
		blip = blipSelector.get()

	dialogueGenerator.create(textboxcontent,
							 pathUniverse.get(), pathCharacter.get(), expression,
							 fontname=fontSelector.get(),
							 background=bgSelector.get(),
							 scalingFactor=scaleFactor,
							 blip_path=blip)

	if (autoOpenVar.get() == 1):
		if platform == "win32": # Only windows was tested
			system(f"start {filename}.gif")
		elif platform == "darwin": # Mac OS?
			system(f"open {filename}.gif")
		else: # Linux?
			system(f"xdg-open {filename}.gif")

#-------------------------------------------------------------------------------
#ANCHOR Visual entry environment
entryFrame = tk.Frame(contentFrame, bg = "black", relief = "raised", bd = 5)

# Portrait preview comes after path initialization
# Portrait functions can be defined here though
def getPortraitImg():
	if useImageVar.get() == 1:
		universe, name, expression = pathUniverse.get(), pathCharacter.get(), pathExpression.get()
		if path.exists(facepath := path.join("faces", universe, name, expression + "1.png")):
			return ImageTk.PhotoImage(Image.open(facepath))
	print("Portrait image not loaded.")

textEntry = tk.Text(entryFrame, height=4, width=30, bg = "black", fg = "white", relief = "flat", bd = 0, insertbackground = "white")

assetMenu = tk.Frame(contentFrame)

# Use portrait checkbox
def setPathActiveFunction(*args):
	if useImageVar.get() == 0:
		pathExpressionDropdown.configure(state="disabled")
		pathInline3.configure(state="disabled")
		pathInline4.configure(state="disabled")
		textEntry["width"] = 40
		portraitPreviewObj.grid_remove()
		portraitScaleLabel.configure(state="disabled")
		portraitScaleField.configure(state="disabled")
		portraitOffsetLabel.configure(state="disabled")
		for child in portraitOffsetBox.winfo_children():
		    child.configure(state='disable')
	else:
		pathExpressionDropdown.configure(state="enabled")
		pathInline3.configure(state="normal")
		pathInline4.configure(state="normal")
		textEntry["width"] = 32
		portraitPreviewObj.grid()
		portraitScaleLabel.configure(state="normal")
		portraitScaleField.configure(state="normal")
		portraitOffsetLabel.configure(state="normal")
		for child in portraitOffsetBox.winfo_children():
		    child.configure(state='normal')

# Background selector
def getBGOptions():
	return dialogueGenerator.backgrounds

bgSelectorOptions = getBGOptions()
bgSelector = tk.StringVar()
bgSelectorLabel = tk.Label(assetMenu, text = "Background:")
bgSelectorDropdown = ttk.OptionMenu(assetMenu, bgSelector, bgSelectorOptions[0], *bgSelectorOptions)

# Auto open checkbox
autoOpenVar = tk.IntVar()
autoOpenCheckbox = tk.Checkbutton(assetMenu, text="auto open gif", variable = autoOpenVar)

# More portrait stuff
# WHY DOESN'T THIS WORK WITHOUT THE defaultImage?????
defaultImage = getPortraitImg()
portraitPreviewObj = tk.Label(entryFrame, image=defaultImage, relief="flat", bd=0, bg="black")

def updatePreviewImage(*args):
	newPortrait = getPortraitImg()
	portraitPreviewObj.configure(image=newPortrait)
	portraitPreviewObj.image = newPortrait

# From now on, update this stuff - can't be done earlier due to path being required
# for this
pathExpression.trace('w', updatePreviewImage)

# Custom file name
fileNameLabel = tk.Label(contentFrame, text = "File name")
fileNameEntry = tk.Entry(contentFrame)
fileNameEntry.insert(0, "outputDialogue")

# Creation button
createAnimation = tk.Button(contentFrame, text= "Create!", command = createFunction, pady = 5, padx = 15, bg = "black", fg = "gold")

#-------------------------------------------------------------------------------
#ANCHOR save buttons

# Save and load some settings
saveButtonBox = tk.Frame(portraitFontOptionsFrame)
loadSettingsButton = tk.Button(saveButtonBox, text= "load settings", command = loadSettings, pady = 3, padx = 5, bg = "darkblue", fg = "gold")
saveSettingsButton = tk.Button(saveButtonBox, text= "save settings", command = saveSettings, pady = 3, padx = 5, bg = "darkblue", fg = "gold")

#-------------------------------------------------------------------------------
#ANCHOR textbox options

textboxOptionsFrame = tk.Frame(portraitFontOptionsFrame, **frameSettings)

textboxOptionHeader = tk.Label(textboxOptionsFrame, text="Textbox Options:")

# 3 or 4 line text toggle
threeLineVar = tk.IntVar()
threeLineCheckbox = tk.Checkbutton(textboxOptionsFrame, text = "Three line spacing", variable = threeLineVar)

# Text color
def textColor():
	colorRGB, colorHex = tk.colorchooser.askcolor(initialcolor = "#ffffff", parent = generalOptionsFrame, title="Pick your text color")
	if colorRGB == None:
		return
	textEntry.config(fg = colorHex)
	dialogueGenerator.color = (int(colorRGB[0]), int(colorRGB[1]), int(colorRGB[2]), 255)

colorButton = tk.Button(textboxOptionsFrame, text= "Pick text color", command = textColor)

# Offset
textOffsetLabel = tk.Label(textboxOptionsFrame, text="Text offset (x, y):")
textOffsetBox = tk.Frame(textboxOptionsFrame)

textOffsetx = tk.StringVar(value = dialogueGenerator.xoffset)
textOffsetxEntry = tk.Entry(textOffsetBox, textvariable = textOffsetx, width=3, validate = "key", validatecommand = (intValidator, "%P"))

textOffsety = tk.StringVar(value = dialogueGenerator.yoffset)
textOffsetyEntry = tk.Entry(textOffsetBox, textvariable = textOffsety, width=3, validate = "key", validatecommand = (intValidator, "%P"))

#-------------------------------------------------------------------------------
#ANCHOR animation frame
animationFrame = tk.Frame(generalOptionsFrame, **frameSettings)
animationLabel = tk.Label(animationFrame, text="Animation timing settings")

# Frame delay
frametimeLabel = tk.Label(animationFrame, text="Frame delay in milliseconds:")
frametimeEntry = tk.Entry(animationFrame, width=3)
frametimeEntry.insert(tk.END, str(dialogueGenerator.frametime))

# Character delay
framepercharLabel = tk.Label(animationFrame, text="Number of frames for each character:")
framepercharEntry = tk.Entry(animationFrame, width=3)
framepercharEntry.insert(tk.END, str(dialogueGenerator.chardelay))

# Character custom delays
def setCharDelayFunction():
	char = charDelaySelectEntry.get()
	val = charDelayValueEntry.get()
	if val == "" and char in dialogueGenerator.delays:
		del dialogueGenerator.delays[char]
	else:
		dialogueGenerator.delays[char] = int(val)
	charListVar.set(getCharDelayFunction())

def getCharDelayFunction():
	res = ""
	for k, v in dialogueGenerator.delays.items():
		res += "''" + k + "' : " + str(v) + "\n"
	return res

charDelayLabel = tk.Label(animationFrame, text="Number of frames for special characters:")

charDelayBox = tk.Frame(animationFrame)
charDelaySelectEntry = tk.Entry(charDelayBox, width=1)
charDelayJoin = tk.Label(charDelayBox, text=":")
charDelayValueEntry = tk.Entry(charDelayBox, width=3)
setCharDelayButton = tk.Button(charDelayBox, text="Set", command = setCharDelayFunction)

# Display character delays
charListVar = tk.StringVar()
charListVar.set(getCharDelayFunction())
charDelayDefaultMessage = tk.Message(animationFrame, textvariable=charListVar)

# Portrait animation delay
portraitDelayLabel = tk.Label(animationFrame, text="Number of frames for portrait animation:")
portraitDelayEntry = tk.Entry(animationFrame, width=2)
portraitDelayEntry.insert(tk.END, "4")

#-------------------------------------------------------------------------------
#ANCHOR Portrait settings

portraitFrame = tk.Frame(generalOptionsFrame, **frameSettings)
portraitHeader = tk.Label(portraitFrame, text="Portrait options:")

useImageCheckbox = tk.Checkbutton(portraitFrame, text="Use portrait", variable = useImageVar)
useImageVar.trace('w', setPathActiveFunction)

# Path entry
pathRequirementMessage = tk.Message(portraitFrame, text = """Portrait path:
- File must be a png file.
- File names must end with a number
- The amount of frames is decided by the file name number.""", width = 400)
pathBox = tk.Frame(portraitFrame)

def getpu():
	return listdir("faces/")

def getpc():
	return listdir("faces/" + pathUniverse.get() + "/")

def setpc(*args):
	pathCharacterDropdown['menu'].delete(0, tk.END)
	choices = getpc()
	for c in choices:
		pathCharacterDropdown['menu'].add_command(label = c, command = tk._setit(pathCharacter, c))
	pathCharacter.set(choices[0])

def getpe():
	portraits = []
	for file in listdir(path.join( "faces", pathUniverse.get(), pathCharacter.get())):
		if not "." in file:
			continue
		[filename, extension] = file.split(".")
		if extension == "png" and filename[-1].isdigit():
			nameEnd = len(filename) - 1
			while filename[nameEnd].isdigit():
				nameEnd -= 1

			portraitName = filename[:nameEnd+1]
			if portraitName not in portraits:
				portraits.append(portraitName)

	return portraits


def setpe(*args):
	pathExpressionDropdown['menu'].delete(0, tk.END)
	choices = getpe()
	for c in choices:
		pathExpressionDropdown['menu'].add_command(label = c, command = tk._setit(pathExpression, c))
	pathExpression.set(choices[0])

pathInline1 = tk.Label(pathBox, text = "faces/")

pathUniverseOptions = getpu()
pathUniverseDropdown = ttk.OptionMenu(pathBox, pathUniverse, pathUniverseOptions[0], *pathUniverseOptions)

pathInline2 = tk.Label(pathBox, text = "/")

pathCharacterDropdown = ttk.OptionMenu(pathBox, pathCharacter)

pathInline3 = tk.Label(pathBox, text = "/")

pathExpressionDropdown = ttk.OptionMenu(pathBox, pathExpression)

pathInline4 = tk.Label(pathBox, text = ".png")

pathCharacter.trace('w', setpe)
pathUniverse.trace('w', setpc)
pathUniverse.set(pathUniverseOptions[0])

portraitScaleLabel = tk.Label(portraitFrame, text="Portrait scale")
portraitScaleField = tk.Scale(portraitFrame, resolution=1, from_=1, to=8, orient="horizontal")
portraitScaleField.set(2)

portraitOffsetLabel = tk.Label(portraitFrame, text="Portrait offset (x, y):")
portraitOffsetBox = tk.Frame(portraitFrame)

portraitOffsetx = tk.StringVar(value = dialogueGenerator.portraitxoffset)
portraitOffsetxEntry = tk.Entry(portraitOffsetBox, textvariable = portraitOffsetx, width=3, validate = "key", validatecommand = (intValidator, "%P"))

portraitOffsety = tk.StringVar(value = dialogueGenerator.portraityoffset)
portraitOffsetyEntry = tk.Entry(portraitOffsetBox, textvariable = portraitOffsety, width=3, validate = "key", validatecommand = (intValidator, "%P"))

#-------------------------------------------------------------------------------
#ANCHOR Sound settings

soundFrame = tk.Frame(portraitFontOptionsFrame, **frameSettings)
soundHeader = tk.Label(soundFrame, text="Sound options:")

useSoundCheckbox = tk.Checkbutton(soundFrame, text="Use sounds", variable = useSoundVar)

def getBlips():
	return dialogueGenerator.blips

blipSelectorOptions = getBlips()
blipSelector = tk.StringVar()
blipSelectorLabel = tk.Label(soundFrame, text = "Sound blip:")
blipSelectorDropdown = ttk.OptionMenu(soundFrame, blipSelector, blipSelectorOptions[0], *blipSelectorOptions)

#-------------------------------------------------------------------------------
#ANCHOR Font settings


fontFrame = tk.Frame(portraitFontOptionsFrame, **frameSettings)

# Font selector
def getFontOptions():
	return list(dialogueGenerator.fonts.keys())

fontSelectorOptions = getFontOptions()
fontSelector = tk.StringVar()
fontSelectorLabel = tk.Label(fontFrame, text = "Current font:")
fontSelectorDropdown = ttk.OptionMenu(fontFrame, fontSelector, fontSelectorOptions[0], *fontSelectorOptions)

fontDict = {}

def setFontFunction():
	print("Applying font settings!")
	for name, details in fontDict.items():
		for item, data in details.items():
			varType = type(dialogueGenerator.fonts[name][item])
			if varType == str:
				dialogueGenerator.fonts[name][item] = data[1].get()
			elif varType == int:
				dialogueGenerator.fonts[name][item] = int(data[1].get())

def getFontFunction():
	print("Loading font settings")
	for y, (name, details) in enumerate(dialogueGenerator.fonts.items()):

		lineLabel = tk.Label(fontDataFrame, text = name)
		lineLabel.grid(row = y, column = 0)
		rowList = {}

		for x, (item, data) in enumerate(details.items()):
			itemLabel = tk.Label(fontDataFrame, text = item)

			itemVar = tk.StringVar()
			itemVar.set(str(data))
			itemEntry = tk.Entry(fontDataFrame, textvariable = itemVar, width = 4)

			rowList[item] = (itemEntry, itemVar)

			itemLabel.grid(row = y, column = 2 * x + 1)
			itemEntry.grid(row = y, column = 2 * x + 2)
		fontDict[name] = rowList

		# Remove Row Button

def saveFontData():
	setFontFunction()
	print("Saving font settings!")
	with open("fontData.json", mode="w") as jsonFile:
		json.dump(dialogueGenerator.fonts, jsonFile)

# Display font data
fontSettingsLabel = tk.Label(fontFrame, text="Font settings:")
fontDataFrame = tk.Frame(fontFrame)
getFontFunction()

dataFontFrame = tk.Frame(fontFrame)
applyFontButton = tk.Button(dataFontFrame, text = "Apply font settings", command = setFontFunction)
saveFontButton = tk.Button(dataFontFrame, text = "Apply & save to file", command = saveFontData)


print("elements initialized")
#-------------------------------------------------------------------------------

#ANCHOR general settings frame alignment
# Main options
generalOptionsFrame.grid(row=0, column=1)

# Animation frame
animationFrame.grid(row=0, sticky=tk.W)
animationLabel.grid(row=0)

# Frame delay
frametimeLabel.grid(row=1)
frametimeEntry.grid(row=2)

# character delays
framepercharLabel.grid(row=3)
framepercharEntry.grid(row=4)

# Special character delays
charDelayLabel.grid(row=5)
charDelayBox.grid(row=6)

charDelaySelectEntry.grid(row = 0, column = 1)
charDelayJoin.grid(row = 0, column = 2)
charDelayValueEntry.grid(row = 0, column = 3)
setCharDelayButton.grid(row = 0, column = 4)

# Show current special characters
charDelayDefaultMessage.grid(row = 7, column = 0)

# Portrait delay
portraitDelayLabel.grid(row = 8)
portraitDelayEntry.grid(row = 9)


# Textbox options frame
portraitFrame.grid(row=1, sticky=tk.W)

# Sprite present checkbox
useImageCheckbox.grid(row = 0)

# Sprite select field
pathRequirementMessage.grid(row = 1, column = 0)
pathBox.grid(row = 2, column = 0)

pathInline1.grid(row = 0, column = 0)
pathUniverseDropdown.grid(row = 0, column = 1)
pathInline2.grid(row = 0, column = 2)
pathCharacterDropdown.grid(row = 0, column = 3)
pathInline3.grid(row = 0, column = 4)
pathExpressionDropdown.grid(row = 0, column = 5)
pathInline4.grid(row = 0, column = 6)

portraitScaleLabel.grid(row=3)
portraitScaleField.grid(row=4)

portraitOffsetLabel.grid(row = 5, column = 0)
portraitOffsetBox.grid(row = 6, column = 0)
portraitOffsetxEntry.grid(row = 0, column = 0)
portraitOffsetyEntry.grid(row = 0, column = 1)


#ANCHOR content box alignment
# Textbox content
contentFrame.grid(row=0, column = 0)
contentHeader.grid(row = 0)

# Data entry frame
entryFrame.grid(row = 1, column=0)

# Portrait preview
portraitPreviewObj.grid(row = 0, column=0)

# Text entry field
textEntry.grid(row=0, column = 1)

# Asset dropdowns
assetMenu.grid(row = 2, column = 0)

# Background selector dropdown
bgSelectorLabel.grid(row = 0, column=0)
bgSelectorDropdown.grid(row = 1, column=0)

# Auto open checkbox
autoOpenCheckbox.grid(row = 4, column = 0)

# File name
fileNameLabel.grid(row = 8, column = 0)
fileNameEntry.grid(row = 9, column = 0)

# Create button
createAnimation.grid(row = 10)

#ANCHOR extra settings frame alignment

portraitFontOptionsFrame.grid(row=0, column=2)

saveButtonBox.grid(row=0, sticky=tk.W)
saveSettingsButton.grid(row=0, column=0)
loadSettingsButton.grid(row=0, column=1)

# Portrait stuffs
textboxOptionsFrame.grid(row=1, sticky=tk.W)

textboxOptionHeader.grid(row=0)

# three line checkbox
threeLineCheckbox.grid(row = 1, column = 0)

# Text color
colorButton.grid(row = 2)

textOffsetLabel.grid(row = 3, column = 0)

textOffsetBox.grid(row = 4, column = 0)
textOffsetxEntry.grid(row = 0, column = 0)
textOffsetyEntry.grid(row = 0, column = 1)

# Sound stuffs
soundFrame.grid(row=2, sticky=tk.W)
soundHeader.grid(row=0)
useSoundCheckbox.grid(row=1)

blipSelectorLabel.grid(row=2)
blipSelectorDropdown.grid(row=3)

# Font stuffs
fontFrame.grid(row=3, sticky=tk.W)

# Font selector dropdown
fontSelectorLabel.grid(row=1, column = 0)
fontSelectorDropdown.grid(row=2, column = 0)

# Show current font data
fontSettingsLabel.grid(row = 3)
fontDataFrame.grid(row = 4, column = 0)

dataFontFrame.grid(row = 5)
applyFontButton.grid(row = 0, column = 0)
saveFontButton.grid(row = 0, column = 1)

print("elements in grid")

print("starting window loop")
root.mainloop()
