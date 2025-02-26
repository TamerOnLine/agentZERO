import pytest
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
import test_ollama3  # Import the corrected module

def setup_agent():
    """Setup test environment for agent initialization."""
    tools = []
    
    # Get the LLM instance correctly
    llm = test_ollama3.get_llm()
    
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True
    )

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
        max_iterations=3,
    )

    print("\nAgent initialized successfully")
    print("Agent details:")
    print(agent)

    return agent

if __name__ == "__main__":
    agent_instance = setup_agent()
    if agent_instance:
        print("\nTest passed: Agent is ready")
    else:
        print("\nTest failed: Agent initialization unsuccessful")
