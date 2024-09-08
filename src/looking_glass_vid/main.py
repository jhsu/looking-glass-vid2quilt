import argparse
import os

import cv2
import numpy as np

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def video_to_grid(
    video_path, output_path, grid_cols=11, grid_rows=6, output_size=(4092, 4092)
):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Calculate the number of frames to skip
    frames_to_show = grid_cols * grid_rows
    frame_step = max(1, (total_frames - 1) // (frames_to_show - 1))

    # Create a list to store the frames
    frames = []

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_step == 0 or frame_count == total_frames - 1:
            frames.append(frame)

            if len(frames) >= frames_to_show:
                break

        frame_count += 1

    # Reverse the order of frames
    frames.reverse()

    # Calculate the size of each grid cell
    cell_width = output_size[0] // grid_cols
    cell_height = output_size[1] // grid_rows

    # Create a blank canvas
    grid_image = np.zeros((output_size[1], output_size[0], 3), dtype=np.uint8)

    for grid_index, frame in enumerate(frames):
        # Resize the frame while maintaining aspect ratio
        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = frame_width / frame_height
        cell_aspect_ratio = cell_width / cell_height

        if aspect_ratio > cell_aspect_ratio:
            # Frame is wider, scale to cell height
            new_height = cell_height
            new_width = int(new_height * aspect_ratio)
        else:
            # Frame is taller, scale to cell width
            new_width = cell_width
            new_height = int(new_width / aspect_ratio)

        resized_frame = cv2.resize(frame, (new_width, new_height))

        # Crop the center of the resized frame to fit the cell
        start_x = (new_width - cell_width) // 2
        start_y = (new_height - cell_height) // 2
        cropped_frame = resized_frame[
            start_y : start_y + cell_height, start_x : start_x + cell_width
        ]

        # Calculate the position in the grid
        row = grid_rows - 1 - (grid_index // grid_cols)
        col = grid_index % grid_cols

        # Place the frame in the grid
        y_start = row * cell_height
        x_start = col * cell_width
        grid_image[y_start : y_start + cell_height, x_start : x_start + cell_width] = (
            cropped_frame
        )

    # Release the video capture object
    cap.release()

    # Save the final grid image
    cv2.imwrite(output_path, grid_image)

    print(f"Grid image saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Looking Glass Vid CLI")
    args = parser.parse_args()

    # CLI mode
    video_path = os.path.join(PROJECT_ROOT, "vase.mp4")
    output_path = os.path.join(PROJECT_ROOT, "outputs", "vase_qs11x6a0.562.jpg")
    video_to_grid(video_path, output_path)
    print(f"Processed video: {video_path}")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()
