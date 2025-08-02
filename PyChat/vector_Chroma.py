import os
import chromadb
from sentence_transformers import SentenceTransformer # Or from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter # Good for chunking


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
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Knowledge base data
knowledge_base = [
    "Fact: The capital of France is Paris. Paris is also known for the Eiffel Tower and the Louvre Museum.",
    "Fact: The capital of Italy is Rome.",
    "Fact: The Great Barrier Reef, located off the coast of Queensland, Australia, is the world's largest coral reef system.",
    "I love gelato.",
    "ice cream is my favorite dessert.",
    "I love to eat ice cream.",
    "I love to eat gelato.",
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

def search_knowledge_base(query: str, top_k: int = 3) -> list:
    """
    Searches the knowledge base using ChromaDB semantic search.
    Returns the most relevant documents.
    """
    # Generate embedding for the query
    query_embedding = embedding_model.encode([query])
    
    # Search for similar documents
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )
    
    # Return relevant documents
    if results['documents'] and results['documents'][0]:
        return results['documents'][0]
    return []

def format_search_results(documents: list) -> str:
    """
    Formats search results into a readable response.
    """
    if not documents:
        return "No relevant information found in the knowledge base."
    
    response = "Based on the knowledge base, here's what I found:\n\n"
    for i, doc in enumerate(documents, 1):
        response += f"{i}. {doc}\n"
    
    return response

def main():
    print("Welcome to the ChromaDB Vector Search! Type 'exit' or 'quit' to leave.")
    print("Try asking: 'where should I get best ice cream', 'tell me about Paris', or 'what about gelato'")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        # Search the knowledge base
        relevant_docs = search_knowledge_base(user_input)
        response = format_search_results(relevant_docs)
        print(f"Search Results: {response}")

if __name__ == "__main__":
    main()