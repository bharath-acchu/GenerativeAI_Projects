import os
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Gemini LLM + embeddings
llm = GoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=os.getenv("GEMINI_API_KEY"))

# Memory to preserve conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Vector DB path
VECTOR_DB_DIR = "vectorstore"

# Set of common small talk phrases
SMALL_TALK = {
    "hi", "hello", "hey", "how are you", "who are you","okie","okay","ok","k","hmm","hmmmmmm"
    "what can you do", "what’s up", "good morning", "good evening",
    "thanks", "thank you"
}

def is_small_talk(text):
    return text.lower().strip() in SMALL_TALK


def get_chatbot_response(question):

    if is_small_talk(question):
        # 🔁 Small talk: route through Gemini with a prompt
        system_prompt = (
            "You are GeminiPDFChatBot. When users casually greet you or ask who you are, "
            "respond politely and inform them that you are a PDF Question Answering bot. "
            "Encourage them to upload a PDF and ask questions based on its content."
        )
        prompt = f"{system_prompt}\nUser: {question}"
        response = llm.invoke(prompt)
        print(response)
        return response
    
    #  If vector store not ready, fallback to general chatbot
    if not os.path.exists(VECTOR_DB_DIR) or not os.listdir(VECTOR_DB_DIR):
        print("vector store not ready calling chatbot directly")
        response = llm.invoke(question)
        return response.content

    # Load vector store
    print("Loading vector db")
    vectordb = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    retriever = vectordb.as_retriever()

    # Setup Conversational Chain with memory
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False
    )

    result = qa_chain.invoke({"question": question})
    print(result['answer'])
    return result['answer']
