# ffmpeg -i BadApple.mp4 -vf "fps=1,scale=640:480" output_%04d.png
# Run > Edit Configurations > Parameters: BadApple bad-apple-audio.mp3
# Paramaters > BadApple bad-apple-audio.mp3
# Scrip ran ffmpeg -i ../BadApple.mp4 -vf "fps=0.1,scale=640:480" output_%04d.png
# venv\Scripts\activate
# python main.py BadApple bad-apple-audio.mp3

from PIL import Image
import sys
import time
import playsound
import threading
import os

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
FRAME_SIZE = 100

class AudioThread(threading.Thread):
    def __init__(self, audio_file):
        super().__init__()
        self.audio_file = audio_file

    def run(self):
        playsound.playsound(self.audio_file)

class VideoThread(threading.Thread):
    def __init__(self, frames_folder):
        super().__init__()
        self.frames_folder = frames_folder

    def run(self):
        frame_count = len([name for name in os.listdir(self.frames_folder) if name.endswith('.png')])
        for index in range(1, frame_count + 1):
            image_path = os.path.join(self.frames_folder, f'frame_{index:04}.png')
            try:
                image = Image.open(image_path, 'r')
                frame = ascii_generator(image)
                sys.stdout.write("\r" + frame)
                sys.stdout.flush()  # Ensure immediate output
                delay_duration = (-0.001 / frame_count) * index + 0.030
                time.sleep(delay_duration)
            except Exception as e:
                print(f"Error processing frame {index}: {e}")
                continue

def resize_image(image_frame):
    width, height = image_frame.size
    aspect_ratio = (height / float(width * 2.5))
    new_height = int(aspect_ratio * FRAME_SIZE)
    resized_image = image_frame.resize((FRAME_SIZE, new_height))
    return resized_image

def greyscale(image_frame):
    return image_frame.convert("L")

def pixels_to_ascii(image_frame):
    pixels = image_frame.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def ascii_generator(image_frame):
    resized_image = resize_image(image_frame)
    greyscale_image = greyscale(resized_image)
    ascii_characters = pixels_to_ascii(greyscale_image)
    pixel_count = len(ascii_characters)
    ascii_image = "\n".join([ascii_characters[index:(index + FRAME_SIZE)] for index in range(0, pixel_count, FRAME_SIZE)])
    return ascii_image

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <frames_folder> <audio_file>")
        sys.exit(1)

    frames_folder = sys.argv[1]
    audio_file = sys.argv[2]

    print(f"Frames folder: {frames_folder}")
    print(f"Audio file: {audio_file}")

    if not os.path.exists(frames_folder):
        print(f"Error: Frames folder '{frames_folder}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(audio_file):
        print(f"Error: Audio file '{audio_file}' does not exist.")
        sys.exit(1)

    audio_thread = AudioThread(audio_file)
    video_thread = VideoThread(frames_folder)
    audio_thread.start()
    video_thread.start()
    audio_thread.join()
    video_thread.join()
