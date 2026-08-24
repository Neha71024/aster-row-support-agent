import os
import sys
from dotenv import load_dotenv
from src.retrieval import get_or_generate_embeddings
from src.agent import RAGAgent

load_dotenv()

def chat_loop():
    print("="*60)
    print("Aster & Row Support Agent CLI")
    print("Type 'exit' to quit, or 'clear' to reset conversation history.")
    print("="*60)

    # 1. Initialize embeddings
    kb_dir = "knowledge-base"
    cache_path = "kb_embeddings.json"

    print("\n[System] Loading knowledge base and embeddings...")
    try:
        embedded_chunks = get_or_generate_embeddings(kb_dir, cache_path)
    except Exception as e:
        print(f"[System Error] Failed to initialize knowledge base: {e}")
        sys.exit(1)

    # 2. Instantiate agent
    agent = RAGAgent(embedded_chunks=embedded_chunks)
    history = []

    print("[System] Agent is online and ready! Ask your question below.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[System] Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == 'exit':
            print("[System] Goodbye!")
            break

        if user_input.lower() == 'clear':
            history = []
            print("[System] Conversation history cleared.\n")
            continue

        # Run the agent turn (retrieves context, executes tool, gets response)
        result = agent.run_turn(user_input, history)

        # Print the response
        print(f"\nAgent: {result['answer']}")
        
        # Print sources and handoff if applicable
        if result['sources']:
            print(f"Sources Cited: {', '.join(result['sources'])}")
        
        if result['handoff']:
            print("[Recommendation] ⚠️ Support specialist handoff recommended.")

        print("-"*60 + "\n")

        # Append to history for the next turn
        history.append({"role": "user", "content": user_input})
        history.append({"role": "model", "content": result['answer']})

if __name__ == "__main__":
    chat_loop()
