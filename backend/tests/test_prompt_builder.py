from app.services.prompt_builder import PromptBuilder


context = """
Artificial Intelligence enables machines to perform
tasks that normally require human intelligence.

Machine Learning is a subset of Artificial Intelligence.
"""

question = "What is Machine Learning?"


print("=" * 80)
print("GENERAL PROMPT")
print("=" * 80)

prompt = PromptBuilder.build_prompt(
    context,
    question
)

print(prompt)


print("\n")
print("=" * 80)
print("SUMMARY PROMPT")
print("=" * 80)

summary_prompt = PromptBuilder.build_summary_prompt(
    context
)

print(summary_prompt)


print("\n")
print("=" * 80)
print("QUESTION ANSWER PROMPT")
print("=" * 80)

qa_prompt = PromptBuilder.build_qa_prompt(
    context,
    question
)

print(qa_prompt)