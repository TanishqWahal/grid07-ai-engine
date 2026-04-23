from langgraph.graph import StateGraph
from phase2_langgraph.tools import mock_searxng_search

# Fake LLM (we'll upgrade later)
def fake_llm(prompt):
    return "AI"

# Node 1: Decide topic
def decide_topic(state):
    topic = fake_llm(state["persona"])
    return {
        "topic": topic,
        "bot_id": state["bot_id"],   
        "persona": state["persona"]
    }

# Node 2: Search
def search_node(state):
    result = mock_searxng_search.invoke(state["topic"])
    return {
        "context": result,
        "topic": state["topic"],
        "bot_id": state["bot_id"],   
        "persona": state["persona"]
    }

# Node 3: Draft Post
def draft_post(state):
    return {
        "output": {
            "bot_id": state["bot_id"],
            "topic": state["topic"],
            "post_content": f"{state['context']} - This proves my point!"
        }
    }

# Build graph
graph = StateGraph(dict)

graph.add_node("decide", decide_topic)
graph.add_node("search", search_node)
graph.add_node("draft", draft_post)

graph.set_entry_point("decide")
graph.add_edge("decide", "search")
graph.add_edge("search", "draft")

app = graph.compile()

# Run
if __name__ == "__main__":
    result = app.invoke({
        "bot_id": "bot_a",
        "persona": "Tech maximalist"
    })

    print(result["output"])
