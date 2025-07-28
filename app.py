from tools import tools
from state import State
from nodes import generate_invoice_worker, attendance_worker, email_worker, route_task

from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
import gradio as gr


def tools_or_next(state: State) -> str:
    """If the last message has tool calls, route to the tools node. Otherwise, end."""
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    return "END"

# --- 3. Build The Graph ---

graph_builder = StateGraph(State)

# 3a. Add all nodes
graph_builder.add_node("route_task", route_task)
graph_builder.add_node("attendance_worker", attendance_worker)
graph_builder.add_node("generate_invoice_worker", generate_invoice_worker)
graph_builder.add_node("email_worker", email_worker)  # <-- ADDED
graph_builder.add_node("tools", ToolNode(tools=tools))

# 3b. Set the entry point
graph_builder.set_entry_point("route_task")

# 3c. Define the edges

# Router to workers
graph_builder.add_conditional_edges(
    "route_task",
    lambda s: s.get("next", "END"),
    {
        "attendance_worker": "attendance_worker",
        "generate_invoice_worker": "generate_invoice_worker",
        "email_worker": "email_worker",  # <-- ADDED
        "END": END,
    },
)

# Individual workers to tools or end
graph_builder.add_conditional_edges(
    "attendance_worker", tools_or_next, {"tools": "tools", "END": END}
)
graph_builder.add_conditional_edges(
    "generate_invoice_worker", tools_or_next, {"tools": "tools", "END": END}
)
graph_builder.add_conditional_edges(
    "email_worker", tools_or_next, {"tools": "tools", "END": END} # <-- ADDED
)

# Tools node back to the correct worker
graph_builder.add_conditional_edges(
    "tools",
    lambda s: s.get("next", "END"),
    {
        "attendance_worker": "attendance_worker",
        "generate_invoice_worker": "generate_invoice_worker",
        "email_worker": "email_worker", # <-- ADDED
        "END": END,
    },
)

# --- 4. Compile the graph ---
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

async def chat(user_input: str, history):
    result = await graph.ainvoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
    return result["messages"][-1].content

if __name__ == "__main__":
    gr.ChatInterface(chat, type="messages").launch()