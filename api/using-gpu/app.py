import time
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from transcript import Transcript
from video import VideoGenerator

# Create a FastAPI app instance
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount a directory as static files to serve them through FastAPI
app.mount("/output", StaticFiles(directory="./output"), name="output")

# Define a welcome endpoint
@app.get("/")
def welcome():
    return {
        "message": "running...",
        "version": "1.0.4"
    }

# Define an endpoint to get transcript segments
@app.get("/transcript")
def get_transcript(url: str = Query(..., description="URL of the transcript")):
    try:
        # Try to process the transcript
        process = Transcript()
        segments = process.run(url)
        return {
            "segments": segments,
        }
    except Exception as e:
        # If an exception occurs, raise an HTTPException with a 500 status code and an error message
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Define an endpoint to process a video based on a transcript
@app.get("/process_video")
def process_video(text: str = Query(..., description="Transcript content")):
    try:
        # Try to process the video
        transcript = text
        background_image_path = "./banner.jpeg"
        
        id = str(int(time.time() * 1000))
        
        output_audio_file = "./output/" + id + ".mp3"
        output_video_file = "./output/" + id + ".mkv"
        
        video_generator = VideoGenerator(transcript, background_image_path, output_audio_file, output_video_file)
        video_generator.run()
        
        return {
            "output_audio_file": output_audio_file,
            "output_video_file": output_video_file,
        }
    except Exception as e:
        # If an exception occurs, raise an HTTPException with a 500 status code and an error message
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Run the FastAPI app using Uvicorn when the script is executed
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, debug=True)
