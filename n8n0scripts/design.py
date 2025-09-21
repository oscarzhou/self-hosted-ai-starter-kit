import sys
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import time

# Get text from n8n
quote = sys.argv[1]

# TeePublic canvas size
WIDTH, HEIGHT = 5000, 5500

# Create transparent background
img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))

# Load font (update path to any TTF you like, e.g. Impact, Arial, Roboto)
try:
    font = ImageFont.truetype("arialbd.ttf", 250)  # Arial Bold
except:
    font = ImageFont.load_default()

draw = ImageDraw.Draw(img)

# Wrap text so it doesn’t overflow
max_width = WIDTH - 400
wrapped = textwrap.wrap(quote, width=20)  # 20 chars per line approx

# Calculate total height
line_height = font.getbbox("A")[3] + 40
text_height = len(wrapped) * line_height
y = (HEIGHT - text_height) // 2

# Draw each line centered
for line in wrapped:
    w, _ = draw.textsize(line, font=font)
    x = (WIDTH - w) // 2
    draw.text((x, y), line, font=font, fill=(0, 0, 0, 255))
    y += line_height

# Save output
outdir = "./designs"
os.makedirs(outdir, exist_ok=True)
outfile = os.path.join(outdir, f"design_{int(time.time())}.png")

img.save(outfile, "PNG", dpi=(150, 150))
print(outfile)   # n8n will capture this path
