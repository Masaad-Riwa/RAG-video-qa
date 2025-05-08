from botbuilder.core import ActivityHandler, TurnContext
from bot.services.api_client import process_video, ask_question

class MainDialog(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip()
        print(f"Received message: {text}")  # Debugging line
        if "youtube.com" in text:
            await turn_context.send_activity("Processing video...")
            process_video(text)  # call FastAPI
            await turn_context.send_activity("Done! Ask your question.")
        else:
            answer = ask_question(text)
            await turn_context.send_activity(f"Answer: {answer}")

