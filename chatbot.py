



# ONLY CHATBOT CODE




# import os
# import json
# from openai import OpenAI
# from fastapi import FastAPI, Request
# from pydantic import BaseModel

# # ---------------- Load API Key ---------------- #
# api_key = os.getenv("OPENROUTER_API_KEY")
# if not api_key:
#     api_key = input("👉 Please enter your OpenRouter API key: ").strip()
#     os.environ["OPENROUTER_API_KEY"] = api_key

# client = OpenAI(
#     api_key=api_key,
#     base_url="https://openrouter.ai/api/v1",
# )

# # ---------------- Load Services JSON ---------------- #
# with open("C:\\Users\\Arpan\\Desktop\\Website_Chatbot\\Details.json", "r", encoding="utf-8") as f:
#     services = json.load(f)   # ✅ use `services` directly

# # ---------------- System Prompt ---------------- #
# SYSTEM_PROMPT = f"""
# You are a chatbot for Aripro Designs Website.

# You ONLY answer questions based on the following services.
# If the user asks something outside these topics, politely say:
# "Sorry, I can only answer questions about our services.
# "
# Rules for responses:
# 1. Always give short, clear, and professional answers.
# 2. Answer only about the service the user explicitly asks about.
#    for example( 
#    - If they ask about a website → talk only about websites.
#    - If they ask about an app → talk only about apps.
#    - If they ask about the app version of a website → explain only how we can create an app linked to that website.
#    )
# 3. Never mention other services unless the user clearly requests them.
# 4. Do not mix website, app, branding, or marketing information unless the user combines them in the question.
# 5. Keep tone professional, simple, and concise.

# Here are the services:

# {json.dumps(services, indent=2)}
# """

# # ---------------- Helper Functions ---------------- #
# def search_services(query: str) -> str:
#     """Try to find an answer in the local JSON knowledge base."""
#     query_lower = query.lower()
#     for category, subservices in services.items():
#         for name, description in subservices.items():
#             if query_lower in name.lower() or query_lower in description.lower():
#                 return f"**{name}** ({category}): {description}"
#     return None


# def chat_with_bot(user_input: str) -> str:
#     # 1. Try knowledge base first
#     kb_answer = search_services(user_input)
#     if kb_answer:
#         return kb_answer

#     # 2. Otherwise, ask OpenRouter model
#     completion = client.chat.completions.create(
#         model="deepseek/deepseek-r1-0528:free",
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_input},
#         ],
#     )
#     return completion.choices[0].message.content


# # ---------------- Chat Loop ---------------- #
# print("✅ Chatbot is ready! Type 'exit' to quit.\n")
# while True:
#     user_input = input("You: ")
#     if user_input.lower() == "exit":
#         break
#     reply = chat_with_bot(user_input)
#     print("Bot:", reply)







# CHATBOT + API CODE


# import os
# import json
# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from openai import OpenAI

# # ---------------- Load API Key ---------------- #
# api_key = os.getenv("OPENROUTER_API_KEY")
# if not api_key:
#     api_key = input("👉 Please enter your OpenRouter API key: ").strip()
#     os.environ["OPENROUTER_API_KEY"] = api_key

# client = OpenAI(
#     api_key=api_key,
#     base_url="https://openrouter.ai/api/v1",
# )

# # ---------------- Load Services JSON ---------------- #
# with open("C:\\Users\\Arpan\\Desktop\\Website_Chatbot\\Details.json", "r", encoding="utf-8") as f:
#     services = json.load(f)

# # ---------------- System Prompt ---------------- #
# SYSTEM_PROMPT = f"""
# You are a chatbot for Aripro Designs Website.

# You ONLY answer questions based on the following services.
# If the user asks something outside these topics, politely say:
# "Sorry, I can only answer questions about our services."

# Rules for responses:
# 1. Always give short, clear, and professional answers.
# 2. Answer only about the service the user explicitly asks about.
#    - If they ask about a website → talk only about websites.
#    - If they ask about an app → talk only about apps.
#    - If they ask about the app version of a website → explain only how we can create an app linked to that website.
# 3. Never mention other services unless the user clearly requests them.
# 4. Do not mix website, app, branding, or marketing information unless the user combines them in the question.
# 5. Keep tone professional, simple, and concise.

# Here are the services:

# {json.dumps(services, indent=2)}
# """

# # ---------------- Helper Functions ---------------- #
# def search_services(query: str) -> str | None:
#     """Try to find an answer in the local JSON knowledge base."""
#     query_lower = query.lower()
#     for category, subservices in services.items():
#         for name, description in subservices.items():
#             if query_lower in name.lower() or query_lower in description.lower():
#                 return f"**{name}** ({category}): {description}"
#     return None


# def chat_with_bot(user_input: str) -> str:
#     # 1. Try knowledge base first
#     kb_answer = search_services(user_input)
#     if kb_answer:
#         return kb_answer

#     # 2. Otherwise, ask OpenRouter model
#     completion = client.chat.completions.create(
#         model="deepseek/deepseek-r1-0528:free",
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_input},
#         ],
#     )
#     return completion.choices[0].message.content


# # ---------------- FastAPI App ---------------- #
# app = FastAPI()

# # Temporary storage for last Q&A
# last_response = {"question": None, "answer": None}


# class QueryRequest(BaseModel):
#     question: str


# @app.post("/ask")
# async def ask_question(request: QueryRequest):
#     """POST endpoint to ask a question to the chatbot."""
#     global last_response
#     answer = chat_with_bot(request.question)
#     last_response = {"question": request.question, "answer": answer}
#     return {"status": "success", "message": "Your question has been processed."}


# @app.get("/answer")
# async def get_answer():
#     """GET endpoint to fetch the last answer as JSON."""
#     if last_response["answer"] is None:
#         return {"status": "error", "message": "No question has been asked yet."}
#     return {"status": "success", "data": last_response}







# CHATBOT API CODE 2


# chatbot.py
import os
import json
import logging
import traceback
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("aripro")

# ---- Load keys ----
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    # fallback: local file for dev only
    if os.path.exists("API_KEY.txt"):
        OPENROUTER_API_KEY = open("API_KEY.txt", "r", encoding="utf-8").read().strip()

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY missing. Set the env var or put it in API_KEY.txt")

masked = OPENROUTER_API_KEY[:8] + "..." + OPENROUTER_API_KEY[-4:]
log.info(f"OpenRouter key detected: {masked}")

APP_API_KEY = os.getenv("APP_API_KEY")  # optional app-level header auth

# ---- OpenRouter client (with recommended headers) ----
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        # These improve reliability with OpenRouter
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Aripro Chatbot (Local Dev)"
    },
)

# ---- Load services JSON ----
with open("Details.json", "r", encoding="utf-8") as f:
    services = json.load(f)

SYSTEM_PROMPT = f"""
You are a chatbot for Aripro Designs Website.
You ONLY answer questions based on the following services.
If the user asks something outside these topics, politely say:
"Sorry, I can only answer questions about our services."

Rules:
1. Short, clear, professional answers.
2. Answer only about the service asked (website vs app vs eCommerce).
3. Do not mix services unless asked.
Here are the services:
{json.dumps(services, indent=2)}
"""

# ---- FastAPI app ----
app = FastAPI(title="Aripro Chatbot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

last_response = {"question": None, "answer": None}

class QueryRequest(BaseModel):
    question: str

def search_services(query: str) -> str | None:
    q = query.lower()
    for category, subs in services.items():
        for name, desc in subs.items():
            if q in name.lower() or q in desc.lower():
                return f"**{name}** ({category}): {desc}"
    return None

def check_api_key(header_key: str | None):
    if APP_API_KEY:
        if not header_key or header_key != APP_API_KEY:
            raise HTTPException(status_code=401, detail="Invalid or missing x-api-key header")

@app.get("/health")
async def health():
    return {"ok": True, "model": "deepseek/deepseek-r1-0528:free", "openrouter_key_loaded": bool(OPENROUTER_API_KEY)}

@app.post("/ask")
async def ask_question(payload: QueryRequest, x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)

    q = (payload.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty question")

    kb = search_services(q)
    if kb:
        last_response.update({"question": q, "answer": kb})
        return {"status": "success", "source": "local", "answer": kb}

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        bot_reply = completion.choices[0].message.content.strip()
        last_response.update({"question": q, "answer": bot_reply})
        return {"status": "success", "source": "model", "answer": bot_reply}
    except Exception as e:
        # log full traceback to the terminal so you can see the root cause (401/403/404 etc.)
        log.error("OpenRouter call failed:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Model/API error: {e}")

@app.get("/answer")
async def get_answer(x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    if not last_response["answer"]:
        return {"status": "error", "message": "No question asked yet"}
    return {"status": "success", "data": last_response}
