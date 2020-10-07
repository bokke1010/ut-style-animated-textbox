from PIL import Image, ImageDraw, ImageFont
from os import path
from os import listdir
import json


#TODO: Load from available fonts & file
fonts = {}

def loadFontData():
	loadeddata = {}
	if path.isfile("fontData.json"):
		with open("fontData.json", "r") as fontData:
			loadeddata = json.load(fontData)
	for filename in listdir("fonts/"):
		# Only valid font files
		if not filename[-4:] in (".otf", ".ttf"):
			continue

		if filename in loadeddata:
			fonts[filename] = loadeddata[filename]
		else:
			fonts[filename] = {"dx": 0, "dy":0, "size":27}

loadFontData()

frametime = 40
chardelay = 1
delays = {
	".": 3,
	",": 3,
	"*": 0
}

color = (255, 255, 255, 255)
xoffset = 28
yoffset = 15

outputFileName = "outputDialogue"

portraitInterval = 4

def create(text, universe, name, expression, fontname = "default.otf"):

	# Background image
	bgImage = Image.open("dialogue_box.png").convert("RGBA")

	# Get portraits
	if expression != None:
		faceAnimation = []
		facecount = 1
		while path.exists(facepath := path.join("faces", universe, name, expression + str(facecount) + ".png")):
			faceFrame = Image.open(facepath).convert("RGBA")
			faceAnimation.append(faceFrame.resize((faceFrame.width * 2, faceFrame.height * 2), resample=Image.NEAREST))
			facecount += 1
		facecount -= 1

	# Get fonts
	charfont = fonts[fontname]
	font = ImageFont.truetype("fonts/" + fontname, charfont["size"])

	# Create frames
	frames = []
	for i in range(len(text)):
		# Get background
		textFrame = bgImage.copy()

		# Draw text
		dx = xoffset + (118 if expression != None else 0)
		dy = yoffset
		draw = ImageDraw.Draw(textFrame)
		draw.multiline_text((dx + charfont["dx"], dy + charfont["dy"]), text[:i+1], font = font, fill = color)

		# Determine text delay
		char = text[i]
		chartime = chardelay
		if char in delays:
			chartime = delays[char]

		# Add the required number of frames
		for j in range(chartime):

			# Draw portrait
			if expression != None:
				portraitFrame = textFrame.copy()
				portrait = faceAnimation[(len(frames) // portraitInterval) % facecount]
				portraitFrame.paste(portrait.copy(), (77 - portrait.width // 2, (bgImage.height - portrait.height) // 2 - 3), mask = portrait)
				frames.append(portraitFrame)
			else:
				frames.append(textFrame)

	# Save animation
	frames[0].save(outputFileName + ".gif", save_all = True, append_images = frames[1:], duration = frametime)
