apt-get update && apt-get install -y ffmpeg

cd backend
uvicorn main:app --host 0.0.0.0 --port 3978

cd ..
python -m bot.app