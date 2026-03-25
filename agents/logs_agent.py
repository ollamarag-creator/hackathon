import json
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def logs_agent(state):
    with open("data/mock_logs.json") as f:
        logs = json.load(f)

    prompt = f"""
You are a Logs Analysis Agent.

Analyze logs and extract:
- error patterns
- anomalies
- timeline of failure

Logs:
{logs}

Return structured analysis.
"""

    result = llm.invoke(prompt)

    return {"logs_analysis": result.content}
