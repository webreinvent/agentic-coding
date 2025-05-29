"""
Basic usage examples for the Agent class.

This file demonstrates how to use the Agent class from the agentic_coding package
for various coding tasks.
"""
import logging
import sys
import os

# Add the project root to the Python path to allow importing the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Agent class
from src.core.agent import Agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def example_code_generation():
    """Demonstrate code generation capabilities."""
    logger.info("Demonstrating code generation")
    
    # Create an agent with default capabilities
    agent = Agent(name="CodeGenerator")
    
    # Define a coding task
    task = "Create a function that calculates the Fibonacci sequence up to n terms"
    
    # Generate code for the task
    solution = agent.solve_task(task)
    
    # Print the solution
    print("\nGenerated solution:")
    print("-" * 40)
    print(solution)
    print("-" * 40)

def example_code_explanation():
    """Demonstrate code explanation capabilities."""
    logger.info("Demonstrating code explanation")
    
    # Create an agent with code explanation capability
    agent = Agent(name="CodeExplainer")
    
    # Define some code to explain
    code = """
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    
    return fib_sequence
"""
    
    # Get an explanation of the code
    explanation = agent.explain_code(code)
    
    # Print the explanation
    print("\nCode explanation:")
    print("-" * 40)
    print(explanation)
    print("-" * 40)

def example_code_refactoring():
    """Demonstrate code refactoring capabilities."""
    logger.info("Demonstrating code refactoring")
    
    # Create an agent with code refactoring capability
    agent = Agent(name="CodeRefactorer")
    
    # Define some code to refactor
    code = """
def calculate_stats(numbers):
    total = 0
    for num in numbers:
        total += num
    mean = total / len(numbers)
    
    squared_diffs = []
    for num in numbers:
        squared_diffs.append((num - mean) ** 2)
    
    variance = sum(squared_diffs) / len(numbers)
    std_dev = variance ** 0.5
    
    return mean, variance, std_dev
"""
    
    # Define refactoring instructions
    instructions = "Refactor to use NumPy for better performance and readability"
    
    # Get the refactored code
    refactored_code = agent.refactor_code(code, instructions)
    
    # Print the refactored code
    print("\nRefactored code:")
    print("-" * 40)
    print(refactored_code)
    print("-" * 40)

def main():
    """Run all examples."""
    logger.info("Starting Agent usage examples")
    
    example_code_generation()
    example_code_explanation()
    example_code_refactoring()
    
    logger.info("All examples completed")

if __name__ == "__main__":
    main()