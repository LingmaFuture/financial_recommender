import requests
import json

class OllamaAPI:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        
    def chat(self, model_name, messages, stream=True):
        """
        Send a chat request to Ollama API
        
        Args:
            model_name (str): Name of the model to use
            messages (list): List of message dictionaries with 'role' and 'content'
            stream (bool): Whether to stream the response
            
        Returns:
            str: The model's response text
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": stream
        }

        try:
            response = requests.post(url, json=payload, stream=stream)
            response.raise_for_status()
            
            if stream:
                # Stream the response
                full_response = []
                for line in response.iter_lines():
                    if line:
                        json_response = json.loads(line)
                        if 'message' in json_response:
                            content = json_response['message'].get('content', '')
                            if content:
                                full_response.append(content)
                return ''.join(full_response)
            else:
                # Return full response at once
                json_response = response.json()
                if 'message' in json_response:
                    return json_response['message'].get('content', '')
                return ''
                    
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return None
            
    def list_models(self):
        """List all available local models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json().get('models', [])
        except requests.exceptions.RequestException as e:
            print(f"Error listing models: {e}")
            return []

def main():
    ollama = OllamaAPI()
    
    # List available models
    print("Available models:")
    models = ollama.list_models()
    for model in models:
        print(f"- {model['name']}")
    
    if not models:
        print("No models found. Please install at least one model using 'ollama pull <model>'")
        return
        
    # Select model
    model_name = models[0]['name']  # Use first available model
    print(f"\nUsing model: {model_name}")
    
    # Start chat loop
    messages = []
    print("\nChat started (type 'quit' to exit)")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break
            
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        print("\nAssistant:", end=' ')
        # Send chat request
        ollama.chat(model_name, messages)
        
        # Add assistant's response to history (for context)
        # Note: In a more complete implementation, you'd want to capture
        # the assistant's response and add it to messages

if __name__ == "__main__":
    main()
