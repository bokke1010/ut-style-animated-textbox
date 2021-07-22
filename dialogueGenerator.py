from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
from os import path
from os import listdir
import json

fonts = {}

def loadFontData():
	loadeddata = {}
	pathString = path.join("data", "fontData.json")
	if path.isfile(pathString):
		with open(pathString, "r") as fontData:
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

backgrounds = []

def loadBackgroundData():
	for filename in listdir("backgrounds/"):
		# Only valid png files
		if not filename[-4:] == ".png":
			continue

		backgrounds.append(filename)

loadBackgroundData()

blips = []

def loadAudioBlips():
	for filename in listdir("blips/"):
		# Only valid sound files
		if filename.split(".")[-1] not in ["wav", "mp3"]:
			continue
		blips.append(filename)

loadAudioBlips()

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
portraitxoffset, portraityoffset = 0, -3

outputFileName = "outputDialogue"

portraitInterval = 4

def create(text: str,
		universe: str,
		name: str,
		expression: str,
		fontname: str = "default.otf",
		background: str = "dialogue_box.png",
		scalingFactor: int = 2,
		blip_path: str = None,
		fileFormat: str = "gif"
	):

	frameCount = sum(delays[char] if char in delays else chardelay for char in text)

	# Background image
	bgImage = Image.open("backgrounds/" + background).convert("RGBA")

	# Get portraits
	if expression != None:
		faceAnimation = []
		facecount = 1
		while path.exists(facepath := path.join("faces", universe, name, expression + str(facecount) + ".png")):
			faceFrame = Image.open(facepath).convert("RGBA")
			faceAnimation.append(faceFrame.resize((faceFrame.width * scalingFactor, faceFrame.height * scalingFactor), resample=Image.NEAREST))
			facecount += 1
		facecount -= 1

	# Get fonts
	charfont = fonts[fontname]
	font = ImageFont.truetype("fonts/" + fontname, charfont["size"])

	# Setup audio
	generateAudio = blip_path != None
	if generateAudio:
		blip = AudioSegment.from_file("blips/" + blip_path)
		blipTrack = AudioSegment.silent(frametime * frameCount + len(blip))

	# Create frames
	frames = []
	for i in range(len(text)):

		# Get background
		textFrame = bgImage.copy()

		# Draw text
		dx = xoffset + (118 if expression != None else 0)
		dy = yoffset
		draw = ImageDraw.Draw(textFrame)
		draw.multiline_text((dx + charfont["dx"], dy + charfont["dy"]),
							text[:i+1], font=font, fill=color, spacing=2)

		# Determine text delay
		char = text[i]
		chartime = chardelay
		if char in delays:
			chartime = delays[char]

		if generateAudio and char.isalnum():
			blipTrack = blipTrack.overlay(blip, position=len(frames) * frametime)


		# Add the required number of frames
		for j in range(chartime):
			# Draw portrait
			if expression == None:
				frames.append(textFrame)
			else:
				portraitFrame = textFrame.copy()
				portrait = faceAnimation[(len(frames) // portraitInterval) % facecount]
				portraitFrame.paste(portrait.copy(), (77 + portraitxoffset - portrait.width // 2, (bgImage.height - portrait.height) // 2 + portraityoffset), mask = portrait)
				frames.append(portraitFrame)

	# Save animation
	frames[0].save(path.join("output", f"{outputFileName}.{fileFormat}"), save_all = True, append_images = frames[1:], duration = frametime)
	if generateAudio:
		blipTrack.export(path.join("output", f"{outputFileName}.mp3"),
						 format="mp3",
						 bitrate="128k")
