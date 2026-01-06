from dotenv import load_dotenv
import asyncio
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

from sqlalchemy import create_engine
load_dotenv()

SALES_CONFIG = {
    "brand_name": "TechHaven",
    "industry": "High-End Electronics Retail",
    "target_audience": "Busy professionals who need quick expert advice",
    "key_benefits": "Instant recommendations, time-saving, premium support",
    "qualifying_questions": [
        "1. What is your primary use case (Gaming, Business, or Creative)?",
        "2. What is your approximate budget range?",
        "3. When are you looking to make a purchase?"
    ]
}

DB_CONNECTION = "sqlite:///memory.db"
engine=create_engine(DB_CONNECTION,connect_args={"check_same_thread": False})

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.5,
    max_retries=0,
    max_tokens=None,
    timeout=None,
    top_p=0.9,
)

def get_session_history(session_id:str)->BaseChatMessageHistory:
    """
    Retrieve history from SQL database.

    :param sender_id: The WhatsApp ID of the sender
    :type sender_id: str

    :return: The chat message history associated with the sender ID
    :rtype: BaseChatMessageHistory
    """
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=engine,
        table_name="sales_agent_chat_history",
    )

async def generate_response(message:str,sender_id:str)->str:
    """
    core Logic for Sales Agent using Groq LPU for high speed responses.

    :param message: The incoming message text
    :type message: str
    :param sender_id: The WhatsApp ID of the sender
    :type sender_id: str

    :return: The generated response text
    :rtype: str
    """

    try:

        system_text = f"""
        You are a senior sales executive for {{brand_name}}, a leader in {{industry}}.
        
        YOUR CUSTOMER:
        You are speaking to {{target_audience}}. They value {{key_benefits}}.
        
        YOUR GOAL:
        Do not just answer questions. You must QUALIFY the lead.
        Guide the conversation to get answers to these 3 specific questions:
        {{qualifying_questions}}
        
        RULES:
        - Keep answers short (under 50 words) suitable for WhatsApp.
        - Be professional but friendly.
        - If the user asks a question, answer it, then immediately ask one of your qualifying questions.
        """
        # We format the string immediately with our Python Config
        formatted_system_text = system_text.format(
            brand_name=SALES_CONFIG["brand_name"],
            industry=SALES_CONFIG["industry"],
            target_audience=SALES_CONFIG["target_audience"],
            key_benefits=SALES_CONFIG["key_benefits"],
            qualifying_questions="\n".join(SALES_CONFIG["qualifying_questions"])
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", formatted_system_text),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{message}")
        ])

        chain=prompt | llm | StrOutputParser()
        with_history=RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="message",
            history_messages_key="chat_history"
        )

        print(f"🧠 SENDING TO GROQ ({SALES_CONFIG['brand_name']}): {message}")
        config = {"configurable": {"session_id": sender_id}}

        response=await asyncio.to_thread(
            with_history.invoke,
            {"message":message},
            config=config
        )

        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I'm having trouble responding right now."