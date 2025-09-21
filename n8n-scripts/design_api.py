from flask import Flask, request, send_file
import io
from PIL import Image, ImageDraw, ImageFont
import textwrap
import time

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    text = request.json.get("text", "Hello World")

    # TeePublic requirements
    WIDTH, HEIGHT = 5000, 5500
    img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))

    # Font (replace with your .ttf if you want a custom one)
    try:
        font = ImageFont.truetype("arialbd.ttf", 250)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)

    # Word wrapping
    max_width = WIDTH - 400
    wrapped = textwrap.wrap(text, width=20)
    line_height = font.getbbox("A")[3] + 40
    total_height = len(wrapped) * line_height
    y = (HEIGHT - total_height) // 2

    for line in wrapped:
        w, _ = draw.textsize(line, font=font)
        x = (WIDTH - w) // 2
        draw.text((x, y), line, font=font, fill=(0, 0, 0, 255))
        y += line_height

    # Save to buffer
    buf = io.BytesIO()
    img.save(buf, "PNG", dpi=(150, 150))
    buf.seek(0)

    filename = f"design_{int(time.time())}.png"
    return send_file(buf, mimetype="image/png", as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
