from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
print(f"✅ Key loaded: {key[:8]}...hidden")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
response = llm.invoke("Say hello in one word")
print("✅ Gemini works:", response.content)
