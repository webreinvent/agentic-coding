"""
Agent module for the Agentic Coding project.

This module defines the Agent class, which is responsible for executing coding tasks
using AI-powered capabilities.
"""
from typing import Dict, List, Optional, Union
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Agent:
    """
    A class representing an AI agent that can perform coding tasks.
    
    The Agent class is the main interface for interacting with the AI capabilities
    of the system. It can understand natural language task descriptions and
    generate or modify code accordingly.
    
    Attributes:
        name (str): The name of the agent.
        capabilities (List[str]): A list of capabilities this agent has.
        context (Dict[str, any]): The current context the agent is operating in.
    """
    
    def __init__(self, name: str = "CodeAgent", capabilities: Optional[List[str]] = None):
        """
        Initialize a new Agent instance.
        
        Args:
            name (str, optional): The name of the agent. Defaults to "CodeAgent".
            capabilities (List[str], optional): A list of capabilities this agent has.
                Defaults to None, which will use a default set of capabilities.
        """
        self.name = name
        self.capabilities = capabilities or ["code_generation", "code_explanation", "code_refactoring"]
        self.context: Dict[str, any] = {}
        logger.info(f"Agent '{name}' initialized with capabilities: {self.capabilities}")
    
    def solve_task(self, task_description: str, context: Optional[Dict[str, any]] = None) -> str:
        """
        Solve a coding task based on the provided description.
        
        This method takes a natural language description of a coding task and
        returns the solution as code.
        
        Args:
            task_description (str): A description of the coding task to solve.
            context (Dict[str, any], optional): Additional context for the task.
                Defaults to None.
                
        Returns:
            str: The solution to the task, typically as code.
            
        Raises:
            ValueError: If the task description is empty or invalid.
            NotImplementedError: If the agent doesn't have the capability to solve the task.
        """
        if not task_description:
            raise ValueError("Task description cannot be empty")
        
        # Update context if provided
        if context:
            self.context.update(context)
        
        logger.debug(f"Solving task: {task_description}")
        
        # This is a placeholder for the actual implementation
        # In a real implementation, this would call an AI model or service
        solution = f"# Solution for: {task_description}\n\n"
        solution += "def example_solution():\n"
        solution += "    # Implementation would go here\n"
        solution += "    return 'Task completed'\n"
        
        logger.info(f"Task solved: {task_description[:50]}...")
        return solution
    
    def explain_code(self, code: str) -> str:
        """
        Generate an explanation for the provided code.
        
        Args:
            code (str): The code to explain.
            
        Returns:
            str: A natural language explanation of the code.
            
        Raises:
            ValueError: If the code is empty or invalid.
        """
        if not code:
            raise ValueError("Code cannot be empty")
        
        if "code_explanation" not in self.capabilities:
            raise NotImplementedError("This agent doesn't have the capability to explain code")
        
        # Placeholder implementation
        explanation = f"This code appears to be a Python function or script.\n"
        explanation += f"It consists of approximately {len(code.split('\n'))} lines.\n"
        explanation += f"A more detailed explanation would be provided by the actual AI implementation."
        
        return explanation
    
    def refactor_code(self, code: str, instructions: str) -> str:
        """
        Refactor the provided code according to the instructions.
        
        Args:
            code (str): The code to refactor.
            instructions (str): Instructions for how to refactor the code.
            
        Returns:
            str: The refactored code.
            
        Raises:
            ValueError: If the code or instructions are empty or invalid.
        """
        if not code:
            raise ValueError("Code cannot be empty")
        
        if not instructions:
            raise ValueError("Refactoring instructions cannot be empty")
        
        if "code_refactoring" not in self.capabilities:
            raise NotImplementedError("This agent doesn't have the capability to refactor code")
        
        # Placeholder implementation
        refactored_code = f"# Refactored according to: {instructions}\n\n"
        refactored_code += code
        
        return refactored_code
    
    def __str__(self) -> str:
        """Return a string representation of the Agent."""
        return f"{self.name} (capabilities: {', '.join(self.capabilities)})"
    
    def __repr__(self) -> str:
        """Return a string representation of the Agent for debugging."""
        return f"Agent(name='{self.name}', capabilities={self.capabilities})"


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Create an agent
    agent = Agent(name="PythonExpert")
    
    # Solve a task
    result = agent.solve_task("Create a function that calculates the factorial of a number")
    print(result)
    
    # Explain some code
    code_to_explain = """
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)
    """
    explanation = agent.explain_code(code_to_explain)
    print(explanation)