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
# Add live image preview
# Add offset preview


root = tk.Tk()
root.title("Animated textbox generator")
root.iconbitmap("icon.ico")
print("tkinter window created")

# Creating the headers
appHeader = tk.Label(root, text="Simple animated textbox UI")

# Left side, reserved for box content
contentFrame = tk.Frame(root)
contentHeader = tk.Label(contentFrame, text="Textbox content:")

# Middle, reserved for settings
optionFrame = tk.Frame(root)
optionHeader = tk.Label(optionFrame, text="Textbox Options:")

# Right side, for font stuffs
fontFrame = tk.Frame(root)
fontHeader = tk.Label(fontFrame, text="Font stuffs:")

#-------------------------------------------------------------------------------
# Variable declaration - for future stuffs

useImageVar = tk.IntVar(value=1)

pathUniverse = tk.StringVar()
pathCharacter = tk.StringVar()
pathExpression = tk.StringVar()

#-------------------------------------------------------------------------------
# Define text entry
def createFunction():
	dialogueGenerator.portraitInterval = int(portraitDelayEntry.get())
	dialogueGenerator.frametime = int(frametimeEntry.get())

	filename = fileNameEntry.get()
	dialogueGenerator.outputFileName = filename

	threeLineOffset = (0, 10) if threeLineVar.get() == 1 else (0, 0)

	dialogueGenerator.xoffset = int(textOffsetx.get()) + threeLineOffset[0]
	dialogueGenerator.yoffset = int(textOffsety.get()) + threeLineOffset[1]

	textboxcontent = textEntry.get("1.0", "4.40")
	expression = None

	if useImageVar.get() == 1:
		expression = pathExpression.get()

	dialogueGenerator.create(textboxcontent, pathUniverse.get(), pathCharacter.get(), expression, fontSelector.get(), bgSelector.get())

	if (autoOpenVar.get() == 1):
		if platform == "win32": # Only windows was tested
			system(f"start {filename}.gif")
		elif platform == "darwin": # Mac OS?
			system(f"open {filename}.gif")
		else: # Linux?
			system(f"xdg-open {filename}.gif")

# Visual entry environment
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

# Font selector
def getFontOptions():
	return list(dialogueGenerator.fonts.keys())

fontSelectorOptions = getFontOptions()
fontSelector = tk.StringVar()
fontSelectorLabel = tk.Label(assetMenu, text = "Font:")
fontSelectorDropdown = ttk.OptionMenu(assetMenu, fontSelector, fontSelectorOptions[0], *fontSelectorOptions)


# Use portrait checkbox
def setPathActiveFunction(*args):
	if useImageVar.get() == 0:
		pathExpressionDropdown.configure(state="disabled")
		pathInline3.configure(state="disabled")
		pathInline4.configure(state="disabled")
		textEntry["width"] = 40
		portraitPreviewObj.grid_remove()
	else:
		pathExpressionDropdown.configure(state="enabled")
		pathInline3.configure(state="normal")
		pathInline4.configure(state="normal")
		textEntry["width"] = 30
		portraitPreviewObj.grid()

# Background selector
def getBGOptions():
	return list(dialogueGenerator.backgrounds)

bgSelectorOptions = getBGOptions()
bgSelector = tk.StringVar()
bgSelectorLabel = tk.Label(assetMenu, text = "Background:")
bgSelectorDropdown = ttk.OptionMenu(assetMenu, bgSelector, bgSelectorOptions[0], *bgSelectorOptions)

checkboxes = tk.Frame(contentFrame)

useImageCheckbox = tk.Checkbutton(checkboxes, text="Use portrait", variable = useImageVar)
useImageVar.trace('w', setPathActiveFunction)

threeLineVar = tk.IntVar()
threeLineCheckbox = tk.Checkbutton(checkboxes, text = "Three line spacing", variable = threeLineVar)

# Auto open checkbox
autoOpenVar = tk.IntVar()
autoOpenCheckbox = tk.Checkbutton(checkboxes, text="auto open gif", variable = autoOpenVar)

# Path entry
pathRequirementMessage = tk.Message(contentFrame, text = """Portrait path:
- File must be a png file.
- File name must end with a number containing what frame it is.
- Only having frame 1 will disable animation.""", width = 400)
pathBox = tk.Frame(contentFrame)

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
pathUniverse.set("ut")

# More portrait stuff
# WHY DOESN'T THIS WORK WITHOUT THE defaultImage?????
defaultImage = getPortraitImg()
portraitPreviewObj = tk.Label(entryFrame, image = defaultImage, relief = "flat", bd = 0)

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
# Text color
def textColor():
	colorRGB, colorHex = tk.colorchooser.askcolor(initialcolor = "#ffffff", parent = optionFrame, title="Pick your text color")
	textEntry.config(fg = colorHex)
	dialogueGenerator.color = (int(colorRGB[0]), int(colorRGB[1]), int(colorRGB[2]))

colorButton = tk.Button(optionFrame, text= "Pick color", command = textColor)

# Offset
def validateInteger(val):
	if val.isdigit():
		return True
	return False

intValidator = root.register(validateInteger)

textOffsetLabel = tk.Label(optionFrame, text="Text offset (x, y):")
textOffsetBox = tk.Frame(optionFrame)

textOffsetx = tk.StringVar(value = dialogueGenerator.xoffset)
textOffsetxEntry = tk.Entry(textOffsetBox, textvariable = textOffsetx, width=3, validate = "key", validatecommand = (intValidator, "%P"))

textOffsety = tk.StringVar(value = dialogueGenerator.yoffset)
textOffsetyEntry = tk.Entry(textOffsetBox, textvariable = textOffsety, width=3, validate = "key", validatecommand = (intValidator, "%P"))

# Frame delay
frametimeLabel = tk.Label(optionFrame, text="Frame delay in milliseconds:")
frametimeEntry = tk.Entry(optionFrame, width=3)
frametimeEntry.insert(tk.END, "40")

# Character delay
framepercharLabel = tk.Label(optionFrame, text="Number of frames for each character:")
framepercharEntry = tk.Entry(optionFrame, width=3)
framepercharEntry.insert(tk.END, "1")

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

charDelayLabel = tk.Label(optionFrame, text="Number of frames for special characters:")

charDelayBox = tk.Frame(optionFrame)
charDelaySelectEntry = tk.Entry(charDelayBox, width=1)
charDelayJoin = tk.Label(charDelayBox, text=":")
charDelayValueEntry = tk.Entry(charDelayBox, width=3)
setCharDelayButton = tk.Button(charDelayBox, text="Set", command = setCharDelayFunction)

# Display character delays
charListVar = tk.StringVar()
charListVar.set(getCharDelayFunction())
charDelayDefaultMessage = tk.Message(optionFrame, textvariable=charListVar)

# Portrait animation delay
portraitDelayLabel = tk.Label(optionFrame, text="Number of frames for portrait animation:")
portraitDelayEntry = tk.Entry(optionFrame, width=2)
portraitDelayEntry.insert(tk.END, "4")

#-------------------------------------------------------------------------------

fontLabel = tk.Label(fontFrame, text = "Font options:")
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
fontDataFrame = tk.Frame(fontFrame)
getFontFunction()

dataFontFrame = tk.Frame(fontFrame)
applyFontButton = tk.Button(dataFontFrame, text = "Apply settings", command = setFontFunction)
saveFontButton = tk.Button(dataFontFrame, text = "Apply & save to file", command = saveFontData)


print("elements initialized")
#-------------------------------------------------------------------------------

# App layout
appHeader.grid(row = 0, column = 0)

# Options
optionFrame.grid(row=1, column=1)
optionHeader.grid(row = 0)

# Text color
colorButton.grid(row = 1)

textOffsetLabel.grid(row = 3, column = 0)
textOffsetBox.grid(row = 4, column = 0)
textOffsetxEntry.grid(row = 0, column = 0)
textOffsetyEntry.grid(row = 0, column = 1)


# Frame delay
frametimeLabel.grid(row = 5)
frametimeEntry.grid(row = 6)

# character delays
framepercharLabel.grid(row = 7)
framepercharEntry.grid(row = 8)

# Special character delays
charDelayLabel.grid(row = 9)
charDelayBox.grid(row = 10)

charDelaySelectEntry.grid(row = 0, column = 1)
charDelayJoin.grid(row = 0, column = 2)
charDelayValueEntry.grid(row = 0, column = 3)
setCharDelayButton.grid(row = 0, column = 4)

# Show current special characters
charDelayDefaultMessage.grid(row = 11, column = 0)

# Portrait delay
portraitDelayLabel.grid(row = 12)
portraitDelayEntry.grid(row = 13)

# Textbox content
contentFrame.grid(row=1, column = 0)
contentHeader.grid(row = 0)

# Data entry frame
entryFrame.grid(row = 1, column=0)

portraitPreviewObj.grid(row = 0, column=0)

# Text entry field
textEntry.grid(row=0, column = 1)

# Asset dropdowns

assetMenu.grid(row = 2, column = 0)

# Font selector dropdown
fontSelectorLabel.grid(row=0, column = 0)
fontSelectorDropdown.grid(row=1, column = 0)

# Background selector dropdown
bgSelectorLabel.grid(row = 0, column=1)
bgSelectorDropdown.grid(row = 1, column=1)

# All checkboxes
checkboxes.grid(row = 4, column = 0)
# Sprite present checkbox
useImageCheckbox.grid(row = 0, column = 0)
# Three line dialogue box checkbox
threeLineCheckbox.grid(row = 0, column = 1)
# Auto-open checkbox
autoOpenCheckbox.grid(row = 0, column = 2)


# Sprite select field
pathRequirementMessage.grid(row = 5, column = 0)
pathBox.grid(row = 6, column = 0)

pathInline1.grid(row = 0, column = 0)
pathUniverseDropdown.grid(row = 0, column = 1)
pathInline2.grid(row = 0, column = 2)
pathCharacterDropdown.grid(row = 0, column = 3)
pathInline3.grid(row = 0, column = 4)
pathExpressionDropdown.grid(row = 0, column = 5)
pathInline4.grid(row = 0, column = 6)


# File name
fileNameLabel.grid(row = 8, column = 0)
fileNameEntry.grid(row = 9, column = 0)

# Create button
createAnimation.grid(row = 10)

# Font stuffs
fontFrame.grid(row = 1, column = 2)
fontHeader.grid(row = 0)

# Show current font data
fontLabel.grid(row = 0, column = 0)
fontDataFrame.grid(row = 1, column = 0)

dataFontFrame.grid(row = 2)
applyFontButton.grid(row = 0, column = 0)
saveFontButton.grid(row = 0, column = 1)

print("elements in grid")

print("starting window loop")
root.mainloop()
