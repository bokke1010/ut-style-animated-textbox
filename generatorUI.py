print("Starting generatorUI")

from os import system
from os import listdir
from os import path
from sys import platform

import tkinter as tk
from tkinter import ttk
print("tkinter imported correctly")

import dialogueGenerator
print("dialogue generator imported correctly")

#TODO:
# font data maybe?
# Split image path into seperate boxes with a note that the frame number is not required
# Checkbox for auto-open


root = tk.Tk()
root.title("Animated textbox generator")
root.iconbitmap("icon.ico")
# root.geometry("800x400")
print("tkinter window created")

# Creating the headers
appHeader = tk.Label(root, text="Simple animated textbox UI")

# Right side, reserved for settings
optionFrame = tk.Frame(root)
optionHeader = tk.Label(optionFrame, text="Textbox Options:")

# Left side, reserved for box content
contentFrame = tk.Frame(root)
contentHeader = tk.Label(contentFrame, text="Textbox content:")

# Text color
colorLabel = tk.Label(optionFrame, text= "RGB color (0-255)")
colorBox = tk.Frame(optionFrame)

# Define text entry because order sadly matters
textEntry = tk.Text(contentFrame, height=4, width=30, bg = "black", fg = "white", relief = "raised", bd = 5)

def RGBtoHex(r, g, b):
	return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def validateColor(val):
	if val.isdigit() and 0 <= int(val) <= 255:
		textEntry.configure(fg = RGBtoHex(colorRed.get(), colorGreen.get(), colorBlue.get()))
		return True
	return False

colorValidator = root.register(validateColor)

colorRed = tk.StringVar(root, name = "RGB_red", value = 255)
colorRedEntry = tk.Entry(colorBox, textvariable = colorRed, width = 3, bg = "red", bd = 3, relief = "flat", validate = "key", validatecommand = (colorValidator, "%P"))

colorGreen = tk.StringVar(root, name = "RGB_green", value = 255)
colorGreenEntry = tk.Entry(colorBox, textvariable = colorGreen, width = 3, bg = "green", bd = 3, relief = "flat", validate = "key", validatecommand = (colorValidator, "%P"))

colorBlue = tk.StringVar(root, name = "RGB_blue", value = 255)
colorBlueEntry = tk.Entry(colorBox, textvariable = colorBlue, width = 3, bg = "blue", bd = 3, relief = "flat", validate = "key", validatecommand = (colorValidator, "%P"))

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

# Textbox text
def createFunction():
	dialogueGenerator.portraitInterval = int(portraitDelayEntry.get())
	dialogueGenerator.color = (int(colorRed.get()), int(colorGreen.get()), int(colorBlue.get()))
	dialogueGenerator.frametime = int(frametimeEntry.get())

	dialogueGenerator.xoffset = int(textOffsetx.get())
	dialogueGenerator.yoffset = int(textOffsety.get())

	textboxcontent = textEntry.get("1.0", "4.40")
	expression = None

	if useImageVar.get() == 1:
		expression = pathExpression.get()

	dialogueGenerator.create(textboxcontent, pathUniverse.get(), pathCharacter.get(), expression)

	if (autoOpenVar.get() == 1):
		if platform == "win32": # Only windows was tested
			system("start outputDialogue.gif")
		elif platform == "darwin": # Mac OS?
			system("open outputDialogue.gif")
		else: # Linux?
			system("xdg-open outputDialogue.gif")

# Use portrait checkbox
def setPathActiveFunction(*args):
	if useImageVar.get() == 0:
		pathExpressionDropdown.configure(state="disabled")
		pathInline3.configure(state="disabled")
		pathInline4.configure(state="disabled")
		textEntry["width"] = 40
	else:
		pathExpressionDropdown.configure(state="enabled")
		pathInline3.configure(state="normal")
		pathInline4.configure(state="normal")
		textEntry["width"] = 30

useImageVar = tk.IntVar()
useImageCheckbox = tk.Checkbutton(contentFrame, text="Use portrait", variable = useImageVar)
useImageVar.trace('w', setPathActiveFunction)

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

pathUnivereOptions = getpu()
pathUniverse = tk.StringVar()
pathUniverseDropdown = ttk.OptionMenu(pathBox, pathUniverse, pathUnivereOptions[0], *pathUnivereOptions)

pathInline2 = tk.Label(pathBox, text = "/")

pathCharacter = tk.StringVar()
pathCharacterDropdown = ttk.OptionMenu(pathBox, pathCharacter)

pathInline3 = tk.Label(pathBox, text = "/")

pathExpression = tk.StringVar()
pathExpressionDropdown = ttk.OptionMenu(pathBox, pathExpression)

pathInline4 = tk.Label(pathBox, text = ".png")

pathCharacter.trace('w', setpe)
pathUniverse.trace('w', setpc)
pathUniverse.set("ut")

# Auto open checkbox
autoOpenVar = tk.IntVar()
autoOpenCheckbox = tk.Checkbutton(contentFrame, text="auto open gif", variable = autoOpenVar)

# Creation button
createAnimation = tk.Button(contentFrame, text= "Create!", command = createFunction, pady = 5, padx = 15, bg = "black", fg = "gold")

print("elements initialized")

# App layout
appHeader.grid(row = 0, column = 0)

# Options
optionFrame.grid(row=1, column=1)
optionHeader.grid(row = 0)

# Text color
colorLabel.grid(row = 1)
colorBox.grid(row = 2)
colorRedEntry.grid(row = 0, column = 0)
colorGreenEntry.grid(row = 0, column = 1)
colorBlueEntry.grid(row = 0, column = 2)

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

# Text entry field
useImageVar.set(1)
textEntry.grid(row=1, column = 0)

# Sprite present checkbox
useImageCheckbox.grid(row = 2, column = 0)

# Sprite select field
pathRequirementMessage.grid(row = 4, column = 0)
pathBox.grid(row = 5, column = 0)

pathInline1.grid(row = 0, column = 0)
pathUniverseDropdown.grid(row = 0, column = 1)
pathInline2.grid(row = 0, column = 2)
pathCharacterDropdown.grid(row = 0, column = 3)
pathInline3.grid(row = 0, column = 4)
pathExpressionDropdown.grid(row = 0, column = 5)
pathInline4.grid(row = 0, column = 6)

# Auto-open checkbox
autoOpenCheckbox.grid(row = 6, column = 0)

# Create button
createAnimation.grid(row = 7)

print("elements in grid")

print("starting window loop")
root.mainloop()
