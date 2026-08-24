import http.server
import json
import os
from http.server import HTTPServer
from src.retrieval import get_or_generate_embeddings
from src.agent import RAGAgent

# 1. Initialize RAG components globally
print("[SERVER] Ingesting knowledge base and loading embeddings...")
embedded_chunks = get_or_generate_embeddings("knowledge-base", "kb_embeddings.json")
agent = RAGAgent(embedded_chunks)
print("[SERVER] RAG Agent initialized successfully.")

class RAGChatHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/chat':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                query = data.get('query', '')
                history = data.get('history', [])
                
                print(f"[SERVER] Query received: '{query}'")
                
                # Execute turn in RAG agent
                result = agent.run_turn(query, history)
                
                # Send JSON response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                print(f"[SERVER] Error processing chat request: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "File not found")
            
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # Map root path and index.html to our src/index.html file
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            index_path = os.path.join("src", "index.html")
            with open(index_path, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode('utf-8'))
        else:
            # Fallback to default handler for other files (if any)
            super().do_GET()

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RAGChatHandler)
    print(f"[SERVER] Web interface running at http://localhost:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
