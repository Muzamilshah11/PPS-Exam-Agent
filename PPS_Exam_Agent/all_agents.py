# Befor the run must add $env:PYHONPATH=1 in Termainal then the below command
# chainlit run src/my_agent2/app.py -w
import os
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv


load_dotenv()
MODEL = 'gemini/gemini-2.0-flash'
KEY = os.getenv("GEMINI_API_KEY")
if not KEY:
    raise ValueError("GEMINI_API_KEY s not set")

# Define existing subject agents (assumed to exist)
intro_agent = Agent(
    name="Intro Tutor",
    instructions="Hello! Welcome to your personalized study assistant. If you’re preparing for the Provincial Planning Services Officers (BPS-17) exam, the PPSO Exam Tutor is the perfect resource for you! This all-in-one tool offers expert guidance across all exam subjects: English, Essay, General Knowledge, Islamiat, Pakistan Studies, Economics, and Viva Voce. With personalized study plans, practice questions, mock tests, and expert tips, it’s designed to boost your confidence and performance. Start your journey to success now!If you have a specific subject or topic in mind, let me know, and I’ll direct you to the right tutor. If you’re unsure where to begin, here’s a general study tip: try breaking your study sessions into 25-minute focused intervals with short breaks in between to improve retention and avoid burnout. How can I assist you today?" 
)

english_agent = Agent(
    name="English Tutor",
    instructions="Expert in English literature, writing, précis, composition, and essay writing."
)
english_conversation_agent = Agent(
    name="English Conversation Tutor",
    instructions="Specialist in English speaking and conversation practice."
)
economics_agent = Agent(
    name="Economics Tutor",
    instructions="Expert in micro and macroeconomics, money, banking, international trade, and general economy."
)
general_science_agent = Agent(
    name="General Science Tutor",
    instructions="Specialist in everyday science concepts."
)
islamiyat_agent = Agent(
    name="Islamiat Tutor",
    instructions="Expert in Islamic studies and religious knowledge."
)

# Define new Pakistan Studies agent
pakistan_studies_agent = Agent(
    name="Pakistan Studies Tutor",
    instructions="Specialist in Pakistan Studies, covering: - History of Pakistan (1857-1947) - Post-independence challenges - The Constitution of Pakistan 1973 - Economy and culture of Pakistan. Provides insights into Pakistan's political, social, and economic landscape."
)

# Define PPSO Exam Tutor agent
ppso_exam_tutor = Agent(
    name="PPSO Exam Tutor",
    instructions="Expert in preparing candidates for the Provincial Planning Services Officers (BPS-17) competitive examination. Provides comprehensive guidance on: - English (Précis & Composition): Grammar, vocabulary, reading comprehension, précis writing - English Essay: Essay writing on various subjects - General Knowledge: General Economy of Pakistan, Current Affairs, Everyday Science - Islamiat / Pakistan Studies: Religious studies or Pakistan's history, depending on preference - Economics: Micro and macroeconomics, money, banking, international trade - Viva Voce: Oral test preparation. Offers study plans, practice questions, and time management tips. For Current Affairs, recommends resources like newspapers and news websites.",
    model=LitellmModel(model=MODEL, api_key=KEY)
    # tools=[
    #     english_agent.as_tool("english", "English Précis, Composition, and Essay"),
    #     economics_agent.as_tool("economics", "Economics and General Economy of Pakistan"),
    #     general_science_agent.as_tool("gen_science", "Everyday Science"),
    #     islamiyat_agent.as_tool("islamiyat", "Islamiat"),
    #     pakistan_studies_agent.as_tool("pak_studies", "Pakistan Studies"),
    #     english_conversation_agent.as_tool("eng_conv", "Viva Voce preparation")
    # ]
)

# Define Triage Agent with all tools
triage_agent = Agent(
    name="Triage Tutor",
    instructions="Always begin by greeting the student with an appropriate emoji 👋. " \
    "Then, analyze the question carefully and route it to the relevant subject tutor, whether it’s English, Economics, Science, Islamiat, Pakistan Studies, or the PPS‑17 Exam Tutor 🔀. " \
    "If the topic is unclear, provide a concise fallback tip to help the student focus, such as: “Try breaking your topic into smaller sub‑topics to improve focus.” " \
    "💡 When asked, “What do you do?” respond with: “I am a study assistant and I will help you prepare for the Provincial Planning Services Officers (BPS‑17) exam.” " \
    "❓ If asked, “Who built you?” reply with: “Powered by Muzzammil Shah 🕵️, Agentic Developer.",
    model=LitellmModel(model=MODEL, api_key=KEY),
    tools=[
        english_agent.as_tool("english", "Literature & writing"),
        english_conversation_agent.as_tool("eng_conv", "Speaking practice"),
        economics_agent.as_tool("economics", "Economics"),
        general_science_agent.as_tool("gen_science", "General Science"),
        islamiyat_agent.as_tool("islamiyat", "Islamiat"),
        pakistan_studies_agent.as_tool("pak_studies", "Pakistan Studies"),
        ppso_exam_tutor.as_tool("ppso_exam", "PPSO exam preparation")
    ]
)