from openai import OpenAI

class ChatGPT():
    def __init__(self,
        key: str,
        model: str,
        max_tokens: int,
        temperature: float,
        max_input: int = 500
    ):
        self.key = key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_input = max_input
        
        # Create OpenAI client.
        self.cl = OpenAI(
            api_key = self.key
        )
        
    def prompt(self, role: str, prompt: str) -> str:
        # Make sure prompt doesn't exceed max input.
        if len(prompt) > self.max_input:
            prompt = prompt[:self.max_input]
        
        # Send chat completion API request.
        res = self.cl.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": role
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens = self.max_tokens,
            temperature = self.temperature
        )
        
        # Return first result.
        return res.choices[0].message.content