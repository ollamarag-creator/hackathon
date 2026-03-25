import json
from fastapi import FastAPI
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

# Import agents
from agents.logs_agent import logs_agent
from agents.metrics_agent import metrics_agent
from agents.deploy_agent import deploy_agent
from agents.resolver_agent import resolver_agent

# LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# -------------------------
# Commander Agent
# -------------------------
def commander(state):
    alert = state["alert"]

    logs = state.get("logs_analysis", "")
    metrics = state.get("metrics_analysis", "")
    deploy = state.get("deploy_analysis", "")

    prompt = f"""
You are an Autonomous Incident Commander.

Alert:
{alert}

Logs Analysis:
{logs}

Metrics Analysis:
{metrics}

Deploy Analysis:
{deploy}

Tasks:
1. Correlate all signals
2. Identify root cause
3. Provide confidence (HIGH/MEDIUM/LOW)

Return clear explanation.
"""

    result = llm.invoke(prompt)

    return {"root_cause": result.content}

# -------------------------
# RCA Generator
# -------------------------
def generate_rca(state):
    return {
        "rca_report": f"""
# INCIDENT REPORT

## Alert
{state['alert']}

## Root Cause
{state['root_cause']}

## Resolution
{state.get('resolution', '')}

## System
Multi-Agent AI (LangGraph)
"""
    }

# -------------------------
# LangGraph Flow
# -------------------------
workflow = StateGraph(dict)

workflow.add_node("logs", logs_agent)
workflow.add_node("metrics", metrics_agent)
workflow.add_node("deploy", deploy_agent)
workflow.add_node("commander", commander)
workflow.add_node("resolver", resolver_agent)
workflow.add_node("rca", generate_rca)

# Flow
workflow.set_entry_point("logs")
workflow.add_edge("logs", "metrics")
workflow.add_edge("metrics", "deploy")
workflow.add_edge("deploy", "commander")
workflow.add_edge("commander", "resolver")
workflow.add_edge("resolver", "rca")

graph = workflow.compile()

# -------------------------
# FastAPI (DEPLOYABLE)
# -------------------------
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Autonomous Incident Commander Running"}

@app.post("/incident")
def run_incident():
    with open("data/mock_alerts.json") as f:
        alerts = json.load(f)

    result = graph.invoke({
        "alert": alerts[0]
    })

    return result


# -------------------------
# Local Test
# -------------------------
if __name__ == "__main__":
    with open("data/mock_alerts.json") as f:
        alerts = json.load(f)

    output = graph.invoke({
        "alert": alerts[0]
    })

    print(output["rca_report"])
