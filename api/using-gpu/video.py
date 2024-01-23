from gtts import gTTS
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoClip
import numpy as np
from PIL import Image
import os
import time

class VideoGenerator:
    def __init__(self, transcript, background_image_path, output_audio_file, output_video_file):
        """
        Initialize the VideoGenerator with necessary parameters.

        Args:
            transcript (str): The transcript to be converted to speech and used in the video.
            background_image_path (str): The file path to the background image for the video.
            output_audio_file (str): The file path to save the generated audio file.
            output_video_file (str): The file path to save the generated video file.
        """
        self.transcript = transcript
        self.background_image_path = background_image_path
        self.output_audio_file = output_audio_file
        self.output_video_file = output_video_file

    def create_audio(self):
        """
        Create audio from the provided transcript using gTTS.

        If the transcript is empty, print a message and return.

        Returns:
            None
        """
        try:
            if not self.transcript:
                print("Empty transcript. Nothing to convert.")
                return
            
            os.makedirs(os.path.dirname(self.output_audio_file), exist_ok=True)

            # Create a gTTS (Google Text-to-Speech) object
            tts = gTTS(text=self.transcript, lang='en', slow=False)

            # Save the audio to a file
            tts.save(self.output_audio_file)

            print(f"Audio generated and saved to {self.output_audio_file}")
        except Exception as e:
            print(f"Error creating audio: {str(e)}")

    def generate_video(self):
        """
        Generate a video by combining an audio file with a background image using moviepy's concatenate_videoclips.

        Returns:
            None
        """
        try:
            # Load audio file
            audio = AudioFileClip(self.output_audio_file)

            # Load background image and convert to numpy array
            background = np.array(Image.open(self.background_image_path))

            # Create a video clip with the background image
            video = VideoClip(lambda t: background, duration=audio.duration)

            # Set the audio for the video clip
            video = video.set_audio(audio)

            # Write the video to the specified output file
            video.write_videofile(self.output_video_file, codec='libx264', audio_codec='aac', fps=24)

            print(f"Video generated and saved to {self.output_video_file}")
        except Exception as e:
            print(f"Error generating video: {str(e)}")

    def run(self):
        """
        Execute the process of creating audio and generating video.

        Returns:
            None
        """
        try:
            self.create_audio()
            self.generate_video()
        except Exception as e:
            print(f"Error running the video generation process: {str(e)}")
        
        
# Example usage with try-except blocks
# if __name__ == "__main__":
#     try:
#         transcript = "equipe aplicativos online tecnologias sobre robôs dos passo você importantes"
#         background_image_path = "./api/without-gpu/banner.jpeg"
        
#         id = str(int(time.time() * 1000))
        
#         output_audio_file = "./api/without-gpu/output/" + id + ".mp3"
#         output_video_file = "./api/without-gpu/output/" + id + ".mkv"
        
#         video_generator = VideoGenerator(transcript, background_image_path, output_audio_file, output_video_file)
#         video_generator.run()
        
#         print({
#             "output_audio_file": output_audio_file,
#             "output_video_file": output_video_file,
#         })
#     except Exception as e:
#         print(f"Error in example usage: {str(e)}")
