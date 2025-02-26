from langchain.agents import AgentType

def get_agent_types():
    """Retrieve and return available AgentType values sorted alphabetically."""
    return sorted(AgentType.__members__.keys())

if __name__ == "__main__":
    agent_types = get_agent_types()
    
    print("Available Agent Types in LangChain:")
    for agent in agent_types:
        print(f"- {agent}")
