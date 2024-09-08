import os

from flask import Flask, render_template, request, send_file
from main import video_to_grid

app = Flask(__name__)

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/process_video", methods=["POST"])
def process_video():
    if "video" not in request.files:
        return "No video file uploaded", 400

    video_file = request.files["video"]
    if video_file.filename == "":
        return "No selected file", 400

    # Save the uploaded video temporarily
    temp_video_path = os.path.join(PROJECT_ROOT, "temp_video.mp4")
    video_file.save(temp_video_path)

    if video_file.filename is None:
        return "No selected file", 400

    # Generate output path
    output_filename = f"{os.path.splitext(video_file.filename)[0]}_qs11x6a0.562.jpg"
    output_path = os.path.join(PROJECT_ROOT, "outputs", output_filename)

    # Ensure the outputs directory exists
    os.makedirs(os.path.join(PROJECT_ROOT, "outputs"), exist_ok=True)

    # Process the video
    video_to_grid(temp_video_path, output_path)

    # Clean up the temporary video file
    os.remove(temp_video_path)

    # Return the processed image
    return send_file(output_path, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(port=5001)
