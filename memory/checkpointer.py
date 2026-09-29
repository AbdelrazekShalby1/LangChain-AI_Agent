from langgraph.checkpoint.memory import InMemorySaver


# Keeps conversation state while the Python process is running.
# For production, replace this with a persistent checkpointer.
checkpointer = InMemorySaver()
