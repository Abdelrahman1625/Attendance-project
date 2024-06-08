import cv2
import os

def output_frames(video_path, output_folder, frames_per_video=200):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_output_folder = os.path.join(output_folder, video_name)
    if not os.path.exists(video_output_folder):
        os.makedirs(video_output_folder)

    existing_frames = len([f for f in os.listdir(video_output_folder) if f.startswith("frame_")])
    if existing_frames >= frames_per_video:
        print(f"Frames already extracted for {video_name}. Skipping...")
        return

    video_capture = cv2.VideoCapture(video_path)

    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_interval = max(total_frames // frames_per_video, 1)

    frame_count = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(video_output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

        if frame_count >= frames_per_video or frame_count >= total_frames:
            break

    video_capture.release()

if __name__ == "__main__":
    # type your videos folder
    video_folder = "D:/projects/image project/dataset/video"  # Replace with the absolute path to your videos folder
    output_folder = "D:/projects/image project/dataset/frame"
    frames_per_video = 200

    video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi", ".mov"))]

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        print(f"Processing {video_file}...")
        output_frames(video_path, output_folder, frames_per_video)
        print("Processing done!")

    input("All videos processed.")