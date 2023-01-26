# step2.py
# pass this script to FontForge to build the intermediate UFO sources for each style
# arguments: master source file (sfd format)

# Copyright 2022 Brad Neil
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

import fontforge

DOT_SIZE = 100
GLYPH_WIDTH = 8
GLYPH_HEIGHT = 12
DESCENT_DOTS = 2
LEFT_SIDE_BEARING = 50
SCREEN_DOT_FACTOR = 0.86
PRINT_DOT_RADIUS = 48.0
MAIN_SOURCE = "Quantum-MASTER-main.sfd"
HALFSTEP_SOURCE = "Quantum-MASTER-halfstep.sfd"
UNLINK_LIST = []

def add_names(font, style, suffix=""):
	font.fontname = font.fontname + style + suffix + "-Regular"
	# font.appendSFNTName("English (US)", 16, font.familyname)
	font.familyname = font.familyname + " " + style + (" " + suffix if suffix else "")
	font.fullname = font.familyname
	# font.appendSFNTName("English (US)", 17, style)
	# font.appendSFNTName("English (US)", 21, font.familyname)
	# font.appendSFNTName("English (US)", 22, "Regular")


def make_regular(source):
	font = fontforge.open(source)
	font["dot"].unlinkThisGlyph()
	font["dot"].clear()
	for glyph in UNLINK_LIST:
		font[glyph].unlinkRef() # prevent rendering issues with just-touching components
	font.selection.all()
	font.removeOverlap()
	font.round()
	font.simplify()
	font.round(0.1) # hack: the "dot" glyph is deliberately 1 unit too large so that simplify() produces nicer outlines; this reverses that
	font.fontname = font.fontname + "-Regular"
	font.save("temp\\MatrixSans-Regular.sfd")

def make_screen(source):
	font = fontforge.open(source)
	font.selection.select("dot")
	font.round(0.1)
	font["dot"].transform((SCREEN_DOT_FACTOR, 0.0, 0.0, SCREEN_DOT_FACTOR, (DOT_SIZE - DOT_SIZE * SCREEN_DOT_FACTOR) / 2, (DOT_SIZE - DOT_SIZE * SCREEN_DOT_FACTOR) / 2))
	font["dot"].unlinkThisGlyph()
	font["dot"].clear()
	add_names(font, "Screen")
	font.uwidth = int(SCREEN_DOT_FACTOR * DOT_SIZE)
	font.os2_strikeysize = int(SCREEN_DOT_FACTOR * DOT_SIZE)
	font.os2_strikeypos += int((DOT_SIZE - font.os2_strikeysize) / 2)
	font.save("temp\\MatrixSansScreen-Regular.sfd")

def make_print(source, name_suffix=None):
	font = fontforge.open(source)
	font["dot"].clear()
	circle = fontforge.unitShape(0) # creates a unit circle
	circle.draw(font["dot"].glyphPen()) # draws the circle into the glyph, replacing previous outlines
	font["dot"].transform((PRINT_DOT_RADIUS, 0.0, 0.0, PRINT_DOT_RADIUS, DOT_SIZE / 2, DOT_SIZE / 2))
	font["dot"].round()
	font["dot"].width = 100
	font["dot"].unlinkThisGlyph()
	font["dot"].clear()
	add_names(font, "Print", name_suffix)
	font.uwidth = int(PRINT_DOT_RADIUS * 10/6)
	font.os2_strikeysize = int(PRINT_DOT_RADIUS * 10/6)
	font.os2_strikeypos += int((DOT_SIZE - font.os2_strikeysize) / 2)
	font.save("temp\\MatrixSansPrint-Regular.sfd")

def make_video(source):
	font = fontforge.open(source)

	video_fix = {"four", "M", "N", "R", "b", "d", "g", "p", "q", "z", "AE", "thorn", 
		"Lslash", "uni2074", "radical", "Eng.loclNSM", "uni1E9E", "eng.sc.loclNSM", 
		"m.sc", "n.sc", "r.sc"}

	font.createChar(-1, "halfdot")
	pen = font["halfdot"].glyphPen()
	pen.moveTo(0,0)
	pen.lineTo(0,DOT_SIZE // 2 + 1)
	pen.lineTo(DOT_SIZE // 2 + 1, DOT_SIZE // 2 + 1)
	pen.lineTo(DOT_SIZE // 2 + 1, 0)
	pen.closePath()
	pen = None

	for glyph in font:

		# determine where the dots are in each glyph
		matrix = [[False]*GLYPH_HEIGHT for _ in range(GLYPH_WIDTH)] # full dots
		matrix2 = [[0]*GLYPH_HEIGHT for _ in range(GLYPH_WIDTH)] # occupied quadrants
		skip = False
		for ref, trans in font[glyph].references:
			if ref != "dot":
				skip = True
				break # we are only interested in glyphs that directly reference the "dot" glyph
			x = int(trans[4]) # coordinates of glyph reference
			y = int(trans[5])
			x //= DOT_SIZE
			y = y // DOT_SIZE + DESCENT_DOTS
			matrix[x][y] = True
			matrix2[x][y] = 15
		if skip:
			continue

		# basic interpolation, Mullard SAA5050 style
		for x in range(GLYPH_WIDTH - 1):
			for y in range(GLYPH_HEIGHT - 1):
				if matrix[x][y] and matrix[x + 1][y + 1] and not (matrix[x + 1][y] or matrix[x][y + 1]):
					font[glyph].addReference("halfdot", (1, 0, 0, 1, x * DOT_SIZE + DOT_SIZE // 2 + LEFT_SIDE_BEARING, (y - DESCENT_DOTS + 1) * DOT_SIZE))
					font[glyph].addReference("halfdot", (1, 0, 0, 1, (x + 1) * DOT_SIZE + LEFT_SIDE_BEARING, (y - DESCENT_DOTS) * DOT_SIZE + DOT_SIZE // 2))
					matrix2[x][y + 1] = 8 # bottom right quarter-dot
					matrix2[x + 1][y] = 1 # top left
				if matrix[x][y + 1] and matrix[x + 1][y] and not (matrix[x][y] or matrix[x + 1][y + 1]):
					font[glyph].addReference("halfdot", (1, 0, 0, 1, x * DOT_SIZE + DOT_SIZE // 2 + LEFT_SIDE_BEARING, (y - DESCENT_DOTS) * DOT_SIZE + DOT_SIZE // 2))
					font[glyph].addReference("halfdot", (1, 0, 0, 1, (x + 1) * DOT_SIZE + LEFT_SIDE_BEARING, (y - DESCENT_DOTS + 1) * DOT_SIZE))
					matrix2[x][y] = 2 # top right
					matrix2[x + 1][y + 1] = 4 # bottom left

	# interpolation done, now finish it off the same as Regular style
	font["dot"].unlinkThisGlyph()
	font["halfdot"].unlinkThisGlyph()
	font["dot"].clear()
	font["halfdot"].clear()

	# hack to preserve the counter of the ring diacritic
	font["ring"].unlinkRef()
	font["ring"].removeOverlap()
	font["ring"].addReference("period", (1, 0, 0, 1, 100, 600))
	font["ring"].unlinkRef()
	font["ring"].correctDirection()

	for glyph in UNLINK_LIST:
		font[glyph].unlinkRef() # prevent rendering issues with just-touching components
	font.selection.all()
	font.removeOverlap()
	font.round()
	font.simplify()
	font.round(0.1)

	add_names(font, "Video")
	font.save("temp\\MatrixSansVideo-Regular.sfd")

def make_raster(source):
	font = fontforge.open(source)

	font["dot"].clear()
	pen = font["dot"].glyphPen()
	pen.moveTo((-15, 50))
	pen.curveTo((-15, 72), (3, 90), (25, 90))

	pen.lineTo((75, 90))
	pen.curveTo((97, 90), (115, 72), (115, 50))
	pen.curveTo((115, 28), (97, 10), (75, 10))

	pen.lineTo(25, 10)
	pen.curveTo((3, 10), (-15, 28), (-15, 50))
	pen.closePath()
	font["dot"].width = 100

	font.createChar(-1, "dot2") # overlaps with dot to the right
	pen = font["dot2"].glyphPen()
	pen.moveTo((74, 90))
	pen.lineTo((126, 90))
	pen.lineTo((126, 10))
	pen.lineTo((74, 10))
	pen.closePath()
	font["dot2"].width = 100

	for glyph in font:
		# determine where the dots are in each glyph
		matrix = [[False]*GLYPH_HEIGHT for _ in range(GLYPH_WIDTH)]
		skip = False
		for ref, trans in font[glyph].references:
			if ref != "dot":
				skip = True
				break # we are only interested in glyphs that directly reference the "dot" glyph
			x = int(trans[4]) # coordinates of glyph reference
			y = int(trans[5])
			x //= DOT_SIZE
			y = y // DOT_SIZE + DESCENT_DOTS
			matrix[x][y] = True
		if skip:
			continue

		for j in range(GLYPH_HEIGHT):
			for i in range(GLYPH_WIDTH - 1):
				if matrix[i][j] and matrix[i + 1][j]:
					if glyph == "underscore" or glyph == "emdash":
						font[glyph].addReference("dot2", (1, 0, 0, 1, i * DOT_SIZE, (j - DESCENT_DOTS) * DOT_SIZE))
					else:
						font[glyph].addReference("dot2", (1, 0, 0, 1, i * DOT_SIZE + LEFT_SIDE_BEARING, (j - DESCENT_DOTS) * DOT_SIZE))

	font["dot"].unlinkThisGlyph()
	font["dot"].clear()
	font["dot2"].unlinkThisGlyph()
	font["dot2"].clear()
	font.selection.all()
	font.removeOverlap()
	font.simplify()
	add_names(font, "Raster")
	# font.uwidth = 80
	font.os2_strikeysize = 80
	font.os2_strikeypos += int((DOT_SIZE - font.os2_strikeysize) / 2)
	font.save("temp\\MatrixSansRaster-Regular.sfd")

def main():
	make_regular(MAIN_SOURCE)
	make_print(MAIN_SOURCE)
	make_raster(MAIN_SOURCE)
	make_screen(MAIN_SOURCE)
	make_video(MAIN_SOURCE)
	make_print(HALFSTEP_SOURCE, " #2")

if __name__ == "__main__":
	main()