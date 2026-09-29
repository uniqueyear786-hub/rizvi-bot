from fastapi import FastAPI, Request
import os, requests
from groq import Groq
app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
@app.get("/")
def home():
    return {"status": "Rizvi Bot Live"}
@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    try:
        m = data['entry'][0]['changes'][0]['value']['messages'][0]
        txt = m['text']['body']
        frm = m['from']
        ai = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"You are Rizvi Communication Karachi assistant, Roman Urdu me jawab do."},{"role":"user","content":txt}]).choices[0].message.content
        requests.post(f"https://graph.facebook.com/v21.0/{os.getenv('PHONE_NUMBER_ID')}/messages", headers={"Authorization": f"Bearer {os.getenv('WHATSAPP_TOKEN')}"}, json={"messaging_product":"whatsapp","to":frm,"text":{"body":ai}})
    except: pass
    return {"ok":True}
