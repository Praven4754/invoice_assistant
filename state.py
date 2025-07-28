from typing import TypedDict, Literal, Optional
from typing import Annotated, TypedDict, List, Dict, Any, Optional
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
    next: Optional[str]