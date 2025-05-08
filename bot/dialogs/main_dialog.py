from botbuilder.core import ActivityHandler, TurnContext
from bot.services.api_client import process_video, ask_question
import uuid
import logging


class MainDialog(ActivityHandler):
    def __init__(self):
        self.session_id = str(uuid.uuid4())  # Generate a unique session ID for each user interaction

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip()
        print(f"Received message: {text}")  # Debugging line
        
        if "youtube.com" in text:
            await turn_context.send_activity("Processing video...")
            #await turn_context.send_activity(f"Sending to FastAPI for processing video with session_id: {self.session_id} and URL: {text}")
            print(f"session_id={self.session_id}, and URL: {text}")
            process_video(text, self.session_id) 
            await turn_context.send_activity("Done! Ask your question.")
        else:
            answer = ask_question(text, self.session_id)  # Pass session ID to the question handler
            await turn_context.send_activity(f"Answer: {answer}")