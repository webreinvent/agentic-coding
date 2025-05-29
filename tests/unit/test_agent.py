"""
Unit tests for the Agent class.

This module contains unit tests for the Agent class in the agentic_coding package.
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root to the Python path to allow importing the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the Agent class
from src.core.agent import Agent

class TestAgent(unittest.TestCase):
    """Test cases for the Agent class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a default agent for testing
        self.agent = Agent(name="TestAgent")
    
    def tearDown(self):
        """Clean up after each test method."""
        # Nothing to clean up for now
        pass
    
    def test_initialization(self):
        """Test that the Agent initializes with the correct default values."""
        # Test with default parameters
        default_agent = Agent()
        self.assertEqual(default_agent.name, "CodeAgent")
        self.assertListEqual(default_agent.capabilities, ["code_generation", "code_explanation", "code_refactoring"])
        self.assertEqual(default_agent.context, {})
        
        # Test with custom parameters
        custom_capabilities = ["custom_capability_1", "custom_capability_2"]
        custom_agent = Agent(name="CustomAgent", capabilities=custom_capabilities)
        self.assertEqual(custom_agent.name, "CustomAgent")
        self.assertListEqual(custom_agent.capabilities, custom_capabilities)
        self.assertEqual(custom_agent.context, {})
    
    def test_solve_task_empty_description(self):
        """Test that solve_task raises ValueError for empty task descriptions."""
        with self.assertRaises(ValueError):
            self.agent.solve_task("")
    
    def test_solve_task_with_context(self):
        """Test that solve_task correctly updates the context."""
        context = {"key": "value"}
        self.agent.solve_task("Test task", context=context)
        self.assertEqual(self.agent.context, context)
    
    def test_explain_code_empty_code(self):
        """Test that explain_code raises ValueError for empty code."""
        with self.assertRaises(ValueError):
            self.agent.explain_code("")
    
    def test_explain_code_missing_capability(self):
        """Test that explain_code raises NotImplementedError when the capability is missing."""
        # Create an agent without the code_explanation capability
        agent = Agent(capabilities=["code_generation"])
        
        with self.assertRaises(NotImplementedError):
            agent.explain_code("def test(): pass")
    
    def test_refactor_code_empty_code(self):
        """Test that refactor_code raises ValueError for empty code."""
        with self.assertRaises(ValueError):
            self.agent.refactor_code("", "Refactor instructions")
    
    def test_refactor_code_empty_instructions(self):
        """Test that refactor_code raises ValueError for empty instructions."""
        with self.assertRaises(ValueError):
            self.agent.refactor_code("def test(): pass", "")
    
    def test_refactor_code_missing_capability(self):
        """Test that refactor_code raises NotImplementedError when the capability is missing."""
        # Create an agent without the code_refactoring capability
        agent = Agent(capabilities=["code_generation"])
        
        with self.assertRaises(NotImplementedError):
            agent.refactor_code("def test(): pass", "Refactor instructions")
    
    def test_string_representation(self):
        """Test the string representation of the Agent."""
        expected_str = "TestAgent (capabilities: code_generation, code_explanation, code_refactoring)"
        self.assertEqual(str(self.agent), expected_str)
    
    def test_repr_representation(self):
        """Test the repr representation of the Agent."""
        expected_repr = "Agent(name='TestAgent', capabilities=['code_generation', 'code_explanation', 'code_refactoring'])"
        self.assertEqual(repr(self.agent), expected_repr)

if __name__ == '__main__':
    unittest.main()