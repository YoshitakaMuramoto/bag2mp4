import subprocess

def create_custom_video_layout(input_files, output_file, rows, cols, fps=30, width=3840, height=2880):
    """
    Create a custom video layout using FFmpeg.

    Parameters:
    - input_files (list of str): List of input video file paths.
    - output_file (str): Path to the output video file.
    - rows (int): Number of rows in the layout.
    - cols (int): Number of columns in the layout.
    - fps (int): Frames per second for the output video.
    - width (int): Width of the output video.
    - height (int): Height of the output video.
    """
    if len(input_files) != rows * cols:
        raise ValueError(f"Expected {rows * cols} input files for a {rows}x{cols} layout, but got {len(input_files)}.")
    
    # Generate FFmpeg input arguments
    input_args = []
    for file in input_files:
        input_args.extend(["-i", file])
    
    # Calculate individual cell dimensions
    cell_width = width // cols
    cell_height = height // rows

    # Generate filter_complex for the custom layout
    scale_filters = []
    overlay_filters = []

    # Scaling each video
    for i in range(len(input_files)):
        scale_filters.append(f"[{i}:v]scale={cell_width}:{cell_height}[vid{i+1}]")
    
    # Overlaying videos in a grid
    overlay_sequence = []
    index = 1
    for row in range(rows):
        for col in range(cols):
            x = col * cell_width
            y = row * cell_height
            if row == 0 and col == 0:
                # First video
                overlay_sequence.append(f"[vid{index}]pad={width}:{height}:0:0[base]")
            else:
                # Overlay other videos
                overlay_sequence.append(f"[base][vid{index}]overlay=shortest=1:x={x}:y={y}[base]")
            index += 1

    # Combine all filters
    filter_complex = (
        "; ".join(scale_filters) + "; "
        + "; ".join(overlay_sequence)
    )

    # Construct FFmpeg command
    command = [
        "ffmpeg",
        *input_args,
        "-filter_complex", filter_complex,
        "-map", "[base]",
        "-r", str(fps),  # Set the output FPS
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        output_file
    ]
    
    # Run FFmpeg command
    subprocess.run(command, check=True)


# Example usage
if __name__ == "__main__":
    # List of 12 input videos
    # input_videos = [f"video{i+1}.mp4" for i in range(12)]
    model_files_a = "20250321_asv_v214"
    model_files_b = "20250321_asv_v216"

    input_videos = [
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_a}/movies/_honda_visualization_monocular_camera_rear_left_detection_result_image.mp4",  # Replace with your video file paths
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_a}/movies/_honda_visualization_monocular_camera_front_center_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_a}/movies/_honda_visualization_monocular_camera_rear_right_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_a}/movies/_honda_visualization_monocular_camera_front_left_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_a}/movies/_honda_visualization_monocular_camera_rear_center_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_a}/movies/_honda_visualization_monocular_camera_front_right_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_b}/movies/_honda_visualization_monocular_camera_rear_left_detection_result_image.mp4",  # Replace with your video file paths
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_b}/movies/_honda_visualization_monocular_camera_front_center_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_b}/movies/_honda_visualization_monocular_camera_rear_right_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_b}/movies/_honda_visualization_monocular_camera_front_left_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_b}/movies/_honda_visualization_monocular_camera_rear_center_detection_result_image.mp4",
        f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_files_b}/movies/_honda_visualization_monocular_camera_front_right_detection_result_image.mp4",
    ]
    
    # Output file
    output_video = "asv_v214_v216.mp4"
    
    # Desired FPS
    output_fps = 15
    
    # Layout specification
    layout_rows = 4  # Number of rows
    layout_cols = 3  # Number of columns
    
    # Create the video
    create_custom_video_layout(input_videos, output_video, layout_rows, layout_cols, fps=output_fps)
