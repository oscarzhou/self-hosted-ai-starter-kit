from flask import Flask, request, send_file, jsonify
import io, time, textwrap
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        text = request.json.get("text", "Hello World")

        # TeePublic size
        WIDTH, HEIGHT = 5000, 5500
        img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))

        # Use DejaVuSans (ships with Pillow) instead of Arial
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 250)
        except:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(img)

        # Wrap text
        wrapped = textwrap.wrap(text, width=20)
        line_height = font.getbbox("A")[3] + 40
        total_height = len(wrapped) * line_height
        y = (HEIGHT - total_height) // 2

        for line in wrapped:
            # Use textbbox instead of textsize
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            x = (WIDTH - w) // 2
            draw.text((x, y), line, font=font, fill=(0, 0, 0, 255))
            y += line_height

        buf = io.BytesIO()
        img.save(buf, "PNG", dpi=(150, 150))
        buf.seek(0)

        filename = f"design_{int(time.time())}.png"
        return send_file(buf, mimetype="image/png",
                         as_attachment=True,
