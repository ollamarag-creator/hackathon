import json
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def deploy_agent(state):
    with open("data/mock_deployments.json") as f:
        deployments = json.load(f)

    prompt = f"""
You are a Deploy Intelligence Agent.

Find:
- recent deployments
- suspicious config changes
- correlation with incident

Deployments:
{deployments}

Return findings.
"""

    result = llm.invoke(prompt)

    return {"deploy_analysis": result.content}
