from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
from os import path
from os import listdir
import json

#DB
# import logging

# l = logging.getLogger("pydub.converter")
# l.setLevel(logging.DEBUG)
# l.addHandler(logging.StreamHandler())
#DB

# ffmpegPath = path.abspath("ffmpeg", "bin")
# ffmpegPath = path.abspath(path.join("ffmpeg", "bin", "ffmpeg.exe"))
# ffprobePath = path.abspath(path.join("ffmpeg", "bin", "ffprobe.exe"))
# AudioSegment.converter = ffmpegPath
# AudioSegment.ffmpeg = ffmpegPath
# AudioSegment.ffprobe = ffprobePath

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
		blip_on_punct: bool = False,
		fileFormat: str = "gif animation"
	):

	#options: gif animation, animated png, png sequence, final frame png

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
		blip = AudioSegment.from_file(path.join("blips", blip_path))
		blipTrack = AudioSegment.silent(frametime * frameCount + len(blip))

	# Create frames
	frames = []
	frameRange = range(len(text)) if fileFormat != "final frame png" else [len(text) - 1]
	for i in frameRange:

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
		charframes = chardelay
		if char in delays:
			charframes = delays[char]
		# Only generate a single frame if the format is single frame png.
		if fileFormat == "final frame png":
			charframes = 1

		if generateAudio and (char.isalnum() or (blip_on_punct and char in ".,:;?!~@#$%^&*()-=_+[]|'\"")):
			blipTrack = blipTrack.overlay(blip, position=len(frames) * frametime)


		# Add the required number of frames
		for j in range(charframes):
			# Draw portrait
			if expression == None:
				frames.append(textFrame)
			else:
				portraitFrame = textFrame.copy()
				portrait = faceAnimation[(len(frames) // portraitInterval) % facecount]
				portraitFrame.paste(portrait.copy(), (77 + portraitxoffset - portrait.width // 2, (bgImage.height - portrait.height) // 2 + portraityoffset), mask = portrait)
				frames.append(portraitFrame)

	# Save animation
	if fileFormat == "gif animation":
		frames[0].save(path.join("output", f"{outputFileName}.gif"), save_all = True, append_images = frames[1:], duration = frametime)
	elif fileFormat == "animated png":
		frames[0].save(path.join("output", f"{outputFileName}.apng"), save_all = True, append_images = frames[1:], duration = frametime)
	elif fileFormat == "png sequence":
		for i, frame in enumerate(frames):
			frame.save(path.join("output", f"{outputFileName}{i:03d}.png"))
	elif fileFormat == "final frame png":
		frames[0].save(path.join("output", f"{outputFileName}.png"))
	if generateAudio and fileFormat != "final frame png":
		audioPath = path.join("output", f"{outputFileName}.mp3")
		# print(audioPath)
		blipTrack.export(audioPath, format="mp3", bitrate="128k")
