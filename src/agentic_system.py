import re
from typing import List, Dict, Any, Callable

class Tool:
    """Base class for tools that the agent can use."""
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class Agent:
    """A simple ReAct-style agent."""
    def __init__(self, tools: List[Tool], system_prompt: str = ""):
        self.tools = {tool.name: tool for tool in tools}
        self.system_prompt = system_prompt
        # This is where you would initialize your LLM client
        
    def think(self, history: str) -> str:
        """
        Simulates the 'Think' step. 
        In a real scenario, this sends the history to an LLM to get the next thought/action.
        """
        # MOCK LLM LOGIC FOR DEMONSTRATION
        # This allows the code to run without an API key immediately.
        if "Action: Calculator" not in history:
            return "Thought: I need to calculate 25 * 4. \nAction: Calculator(25 * 4)"
        elif "Observation: 100" in history and "Final Answer" not in history:
            return "Thought: I have the result. \nFinal Answer: The result is 100."
        else:
            return "Final Answer: I cannot answer this yet."

    def execute_action(self, action_string: str) -> str:
        """Parses and executes a tool action."""
        # Simple regex to parse "ToolName(args)"
        match = re.search(r"(\w+)\((.*)\)", action_string)
        if not match:
            return "Error: Could not parse action."
        
        tool_name = match.group(1)
        args_str = match.group(2)
        
        if tool_name in self.tools:
            try:
                # modifying this to be safer in real prod, but eval is fine for this demo
                result = self.tools[tool_name].run(eval(args_str))
                return str(result)
            except Exception as e:
                return f"Error executing tool: {e}"
        else:
            return f"Error: Tool '{tool_name}' not found."

    def run(self, query: str, max_steps: int = 5):
        print(f"User Query: {query}\n" + "-"*30)
        history = f"System: {self.system_prompt}\nUser: {query}\n"
        
        for i in range(max_steps):
            response = self.think(history)
            print(response)
            history += response + "\n"
            
            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()
                
            if "Action:" in response:
                action_part = response.split("Action:")[1].strip()
                observation = self.execute_action(action_part)
                print(f"Observation: {observation}")
                history += f"Observation: {observation}\n"
                
        return "Max steps reached."

# --- Example Tools ---

def calculator_func(expression):
    # WARNING: eval is unsafe for untrusted input. Use with caution.
    return eval(expression)

# --- Main ---

if __name__ == "__main__":
    # Initialize Tools
    calc_tool = Tool(
        name="Calculator",
        description="Useful for math calculations. Input should be a valid python expression.",
        func=calculator_func
    )
    
    # Initialize Agent
    agent = Agent(
        tools=[calc_tool],
        system_prompt="You are a helpful assistant that uses tools to answer questions."
    )
    
    # Run Agent
    agent.run("What is 25 * 4?")
