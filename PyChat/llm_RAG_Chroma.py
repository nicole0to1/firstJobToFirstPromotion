import os
import chromadb
from sentence_transformers import SentenceTransformer # Or from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter # Good for chunking
import openai

# --- RAG Components with ChromaDB ---

# Initialize ChromaDB client
client = chromadb.Client()

# Create or get collection
collection_name = "knowledge_base"
try:
    collection = client.get_collection(name=collection_name)
except:
    collection = client.create_collection(name=collection_name)

# Initialize sentence transformer for embeddings
embedding_model = SentenceTransformer('all-mpnet-base-v2')

# Knowledge base data
knowledge_base = [
    "Fact: The capital of France is Paris. Paris is also known for the Eiffel Tower and the Louvre Museum.",
    "Fact: The capital of Italy is Rome.",
    "Fact: The Great Barrier Reef, located off the coast of Queensland, Australia, is the world's largest coral reef system.",
    "I love gelato.",
    "ice cream is my favorite dessert.",
    "I love to eat ice cream.",
    "I love to eat gelato.",
    "I love to eat ice cream.",
    "I love desserts in Paris.",
    "I love gelato near Trevi Fountain."
]

# Add documents to ChromaDB if collection is empty
if collection.count() == 0:
    # Generate embeddings for all documents
    embeddings = embedding_model.encode(knowledge_base)
    
    # Add documents to collection
    collection.add(
        embeddings=embeddings.tolist(),
        documents=knowledge_base,
        ids=[f"doc_{i}" for i in range(len(knowledge_base))]
    )

def retrieve_information(query: str) -> str:
    """
    Retrieves relevant information from ChromaDB using semantic search.
    """
    # Generate embedding for the query
    query_embedding = embedding_model.encode([query])
    
    # Search for similar documents
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3
    )
    
    # Return relevant documents
    if results['documents'] and results['documents'][0]:
        return "\n".join(results['documents'][0])
    return ""

# --- LLM Interaction (Enhanced with RAG) ---

# Read API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit(1)

openai.api_key = api_key

def ask_llm_with_rag(user_prompt: str) -> str:
    """
    Sends a prompt to the LLM, augmented with retrieved context.
    """
    # Step 1: Retrieve relevant context based on the user's prompt
    retrieved_context = retrieve_information(user_prompt)

    # Step 2: Construct the augmented prompt for the LLM
    if retrieved_context:
        # If context is found, instruct the LLM to use it
        augmented_prompt = (
            f"Based on the following information, please answer the user's question. "
            f"If the provided information is insufficient, state that you cannot fully answer "
            f"based on the given context, but still try to provide a general answer if possible.\n\n"
            f"--- Context Start ---\n"
            f"{retrieved_context}\n"
            f"--- Context End ---\n\n"
            f"User's Question: {user_prompt}"
        )
        # Adjust LLM instructions to emphasize using the provided context
        llm_instructions = (
            "You are a general advisor. Prioritize using the provided 'Context' "
            "to answer the user's question accurately. If the context does not contain "
            "enough information, you may use your general knowledge, but clearly state "
            "if your answer goes beyond the provided context."
        )
    else:
        # If no context is found, just send the original prompt
        augmented_prompt = user_prompt
        llm_instructions = "You are a general advisor. Answer the user's question to the best of your knowledge."

    try:
        # Send the augmented prompt to the LLM
        response = openai.responses.create(
            model="gpt-4o",
            instructions=llm_instructions,
            input=augmented_prompt
        )
        return response.output_text.strip()
    except Exception as e:
        return f"Error communicating with LLM: {e}"

def main():
    print("Welcome to the LLM Shell with Vector Embedding enhanced RAG! Type 'exit' or 'quit' to leave.")
    print("Try asking about: general questions, or questions about gelato or ice cream.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        # Use the RAG-enhanced function
        reply = ask_llm_with_rag(user_input)
        print(f"LLM: {reply}")

if __name__ == "__main__":
    main()