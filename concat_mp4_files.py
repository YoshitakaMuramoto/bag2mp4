import os
import subprocess

def combine_videos(input_files, output_file):
    """
    Combine 6 MP4 videos into one grid layout video.
    
    Parameters:
        input_files (list): List of 6 MP4 file paths.
        output_file (str): Path to save the output MP4 file.
    """
    if len(input_files) != 6:
        raise ValueError("Exactly 6 input video files are required.")

    # Create a filter_complex string for 2x3 layout
    filter_complex = (
        "[0:v][1:v][2:v]hstack=3[top];"
        "[3:v][4:v][5:v]hstack=3[bottom];"
        "[top][bottom]vstack=2[out]"
    )
    
    # Create FFmpeg command
    command = [
        "ffmpeg",
        "-y",  # Overwrite output file without asking
    ]
    for input_file in input_files:
        command.extend(["-i", input_file])  # Add input files
    command.extend([
        "-filter_complex", filter_complex,
        "-map", "[out]",  # Specify output video stream
        "-c:v", "libx264",  # Set codec to H.264
        "-preset", "fast",  # Use fast preset for encoding
        "-crf", "23",  # Set quality
        output_file
    ])

    # Execute FFmpeg command
    subprocess.run(command, check=True)
    print(f"Output video saved to: {output_file}")

# Example usage
model_dir = "20250527_asv_v220"
input_videos = [
    f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_dir}/movies/_honda_visualization_monocular_camera_rear_left_detection_result_image.mp4",  # Replace with your video file paths
    f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_dir}/movies/_honda_visualization_monocular_camera_front_center_detection_result_image.mp4",
    f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_dir}/movies/_honda_visualization_monocular_camera_rear_right_detection_result_image.mp4",
    f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_dir}/movies/_honda_visualization_monocular_camera_front_left_detection_result_image.mp4",
    f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_dir}/movies/_honda_visualization_monocular_camera_rear_center_detection_result_image.mp4",
    f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_dir}/movies/_honda_visualization_monocular_camera_front_right_detection_result_image.mp4",
]
output_video = f"/media/nvidia/OrinSSD2000/rosbag/movies/{model_dir}/movies/{model_dir}.mp4"

combine_videos(input_videos, output_video)


