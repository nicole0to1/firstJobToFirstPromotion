import os
import openai

# --- RAG Components ---

# 1. Simple In-Memory Knowledge Base
# In a real-world RAG system, this would be a much larger, external database
# (e.g., vector database, document store) containing your specific data.
knowledge_base = [
    "Fact: The capital of France is Paris. Paris is also known for the Eiffel Tower and the Louvre Museum.",
    "Fact: Mount Everest is the highest mountain in the world, located in the Himalayas, bordering Nepal and China.",
    "Fact: The Amazon River is the largest river by discharge volume in the world, flowing through South America.",
    "Fact: Photosynthesis is the process used by plants, algae, and cyanobacteria to convert light energy into chemical energy, stored in glucose.",
    "Fact: Water's chemical formula is H2O, consisting of two hydrogen atoms and one oxygen atom.",
    "Fact: The Earth revolves around the Sun, taking approximately 365.25 days to complete one orbit.",
    "Fact: The speed of light in a vacuum is approximately 299,792,458 meters per second.",
    "Fact: The human heart has four chambers: two atria and two ventricles.",
    "Fact: The Great Barrier Reef, located off the coast of Queensland, Australia, is the world's largest coral reef system."
]

def retrieve_information(query: str) -> str:
    """
    Simulates retrieving relevant information from a knowledge base.
    For this simple example, it uses keyword matching.
    In a real RAG system, this would involve more sophisticated methods
    like semantic search using embeddings.
    """
    relevant_docs = []
    # Convert query to lowercase for case-insensitive matching
    query_lower = query.lower()

    # Split the query into keywords (simple approach)
    query_keywords = query_lower.split()

    for doc in knowledge_base:
        # Check if any keyword from the query is present in the document
        # A more robust system would use embedding similarity
        if any(keyword in doc.lower() for keyword in query_keywords):
            relevant_docs.append(doc)

    # Return unique relevant documents, joined by newlines
    # Using set to avoid duplicates if multiple keywords match the same doc
    return "\n".join(sorted(list(set(relevant_docs)))) if relevant_docs else ""

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
    print("Welcome to the LLM Shell with RAG! Type 'exit' or 'quit' to leave.")
    print("Try asking about: Paris, Mount Everest, Photosynthesis, H2O, or the Amazon River.")
    print("Also try questions for which no context is provided, like 'What is the capital of Japan?'")
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