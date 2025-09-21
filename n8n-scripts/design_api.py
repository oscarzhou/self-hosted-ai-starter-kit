from flask import Flask, request, send_file, jsonify
import io, time, textwrap
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        text = request.json.get("text", "Hello World")
        color = request.json.get("color", "white").lower()

        # TeePublic size requirement
        WIDTH, HEIGHT = 5000, 5500
        img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))  # Transparent background

        # Font (DejaVuSans is bundled with Pillow in python:slim image)
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 250)
        except:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(img)

        # Wrap text into lines
        wrapped = textwrap.wrap(text, width=20)
        line_height = font.getbbox("A")[3] + 40
        total_height = len(wrapped) * line_height
        y = (HEIGHT - total_height) // 2

        # Pick text color
        if color == "black":
            fill = (0, 0, 0, 255)
        else:  # default to white
            fill = (255, 255, 255, 255)

        # Draw each line centered
        for line in wrapped:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            x = (WIDTH - w) // 2
            draw.text((x, y), line, font=font, fill=fill)
            y += line_height

        # Save to buffer
        buf = io.BytesIO()
        img.save(buf, "PNG", dpi=(150, 150))
        buf.seek(0)

        filename = f"design_{int(time.time())}.png"
        return send_file(
            buf,
            mimetype="image/png",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
