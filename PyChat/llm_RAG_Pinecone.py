import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import numpy as np
import openai

pinecone = Pinecone("pcsk_2Dyx1A_FUHLNJXq53PyUFCub3rwSAhKKgSrq37TC43p4WsPSGkzFH97Zt9XBSE5x61DTbL") #api_key=os.environ.get("PINECONE_API_KEY"))

# Create or connect to a Pinecone index
index_name = 'rag-example'

# Delete existing index if it exists (to handle dimension mismatch)
try:
    pinecone.delete_index(index_name)
    print(f"Deleted existing index: {index_name}")
except:
    pass

# Create new index
pinecone.create_index(
    name=index_name,
    dimension=768,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
print(f"Created new index: {index_name}")

index = pinecone.Index(index_name)

# Initialize embedding model
model = SentenceTransformer('all-mpnet-base-v2')

# Sample documents
documents = [
    {"id": "1", "chunk_text": "The capital of France is Paris.  Paris is also known for the Eiffel Tower and the Louvre Museum."},
    {"id": "2", "chunk_text": "The capital of Italy is Rome."},
    {"id": "3", "chunk_text": "The Great Barrier Reef, located off the coast of Queensland, Australia, is the world's largest coral reef system."},
    {"id": "4", "chunk_text": "I love gelato."},
    {"id": "5", "chunk_text": "ice cream is my favorite dessert."},
    {"id": "6", "chunk_text": "I love to eat ice cream."},
    {"id": "7", "chunk_text": "I love to eat gelato."},
    {"id": "8", "chunk_text": "I love to eat ice cream."},
    {"id": "9", "chunk_text": "I love desserts in Paris."},
    {"id": "10", "chunk_text": "I love gelato near Trevi Fountain."}
]

# Embed and upsert documents to Pinecone
vectors = []
for doc in documents:
    embedding = model.encode(doc['chunk_text']).tolist()
    vectors.append((doc['id'], embedding, {'text': doc['chunk_text']}))
index.upsert(vectors=vectors)

def retrieve_information(query: str) -> str:
    """
    Retrieves relevant information from Pinecone using semantic search.
    """
    # Generate embedding for the query and normalize
    query_embedding = model.encode(query).tolist()
     
    # Retrieve top-k relevant documents
    results = index.query(
        vector=[query_embedding], 
        top_k=3, 
        include_metadata=True
    )

    print(results)
    # Extract retrieved documents
    retrieved_docs = [match['metadata']['text'] for match in results['matches']]
    print(retrieved_docs)
    return retrieved_docs  

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
    print("Welcome to the LLM Shell with Pinecone Vector Embedding enhanced RAG! Type 'exit' or 'quit' to leave.")
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

# Cleanup (optional)
# pinecone.delete_index(index_name)