import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from services.vector_service import vector_stores

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def answer_question(doc_id: str, question: str, segments: list = None) -> dict:
    store = vector_stores.get(doc_id)
    context_chunks = []
    if store:
        context_chunks = store.search(question, top_k=3)

    context = "\n\n".join(context_chunks) if context_chunks else "No document context available."

    messages = [
        SystemMessage(content="""You are a helpful assistant that answers questions based on uploaded documents.
Always base your answers on the provided context. If the answer is not in the context, say so clearly."""),
        HumanMessage(content=f"""Context from document:
{context}

Question: {question}

Please answer based on the context above.""")
    ]

    response = llm.invoke(messages)
    answer = response.content

    relevant_timestamp = None
    if segments:
        relevant_timestamp = find_relevant_timestamp(question, segments)

    return {
        "answer": answer,
        "timestamp": relevant_timestamp,
        "sources": context_chunks[:2]
    }

def find_relevant_timestamp(question: str, segments: list) -> float:
    if not segments:
        return None

    segments_text = "\n".join([
        f"[{seg['start']:.1f}s - {seg['end']:.1f}s]: {seg['text']}"
        for seg in segments[:20]
    ])

    messages = [
        HumanMessage(content=f"""Given these transcript segments with timestamps:
{segments_text}

For the question: "{question}"
Reply with ONLY the start timestamp number in seconds, or "none" if not applicable.""")
    ]

    response = llm.invoke(messages)
    result = response.content.strip()
    try:
        return float(result)
    except:
        return None

def summarize_content(text: str) -> str:
    truncated = text[:4000] if len(text) > 4000 else text
    messages = [
        HumanMessage(content=f"Provide a clear structured summary in 3-5 bullet points:\n\n{truncated}")
    ]
    response = llm.invoke(messages)
    return response.content