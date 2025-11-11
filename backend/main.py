from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/flashcards")
async def generate_flashcards(request: Request):
    data = await request.json()
    topic = data.get("topic")

    prompt = f"""
    Create 5 study flashcards about {topic}. 
    Respond in JSON like:
    [{{"question": "...", "answer": "..."}}]
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        cards = completion.choices[0].message.content
        return {"cards": cards}

    except Exception as e:
        return {"error": str(e)}
