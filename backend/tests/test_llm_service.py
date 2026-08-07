from app.services.llm_service import LLMService


prompt = """
You are an AI assistant.

Question:

What is Artificial Intelligence?

Answer:
"""

response = LLMService.generate_response(
    prompt
)

print("\n")
print("=" * 70)
print("LLM RESPONSE")
print("=" * 70)
print(response)
print("=" * 70)