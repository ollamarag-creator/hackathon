import json
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def resolver_agent(state):
    with open("data/mock_faq_knowledge_base.json") as f:
        kb = json.load(f)

    root_cause = state.get("root_cause", "")

    prompt = f"""
You are a Resolver Agent.

Root cause:
{root_cause}

Use knowledge base:
{kb}

Return:
- resolution steps
- rollback command
- prevention steps
"""

    result = llm.invoke(prompt)

    return {"resolution": result.content}
