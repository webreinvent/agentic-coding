"""
Task model for the Agentic Coding project.

This module defines the Task class, which represents a coding task to be performed
by an AI agent.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import uuid


@dataclass
class Task:
    """
    A class representing a coding task to be performed by an AI agent.
    
    The Task class encapsulates all the information needed to describe a coding task,
    including its description, context, and metadata.
    
    Attributes:
        id (str): A unique identifier for the task.
        description (str): A natural language description of the task.
        context (Dict[str, any]): Additional context for the task.
        created_at (datetime): When the task was created.
        updated_at (datetime): When the task was last updated.
        tags (List[str]): Tags associated with the task.
        priority (int): The priority of the task (1-5, with 5 being highest).
        status (str): The current status of the task.
        solution (Optional[str]): The solution to the task, if available.
    """
    
    description: str
    context: Dict[str, any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    priority: int = 3
    status: str = "pending"
    solution: Optional[str] = None
    
    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.description:
            raise ValueError("Task description cannot be empty")
        
        if self.priority < 1 or self.priority > 5:
            raise ValueError("Priority must be between 1 and 5")
    
    def update(self, **kwargs):
        """
        Update the task with new values.
        
        Args:
            **kwargs: The attributes to update and their new values.
            
        Returns:
            Task: The updated task (self).
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Task has no attribute '{key}'")
        
        self.updated_at = datetime.now()
        return self
    
    def add_tags(self, *tags):
        """
        Add tags to the task.
        
        Args:
            *tags: The tags to add.
            
        Returns:
            Task: The updated task (self).
        """
        for tag in tags:
            if tag not in self.tags:
                self.tags.append(tag)
        
        self.updated_at = datetime.now()
        return self
    
    def remove_tags(self, *tags):
        """
        Remove tags from the task.
        
        Args:
            *tags: The tags to remove.
            
        Returns:
            Task: The updated task (self).
        """
        for tag in tags:
            if tag in self.tags:
                self.tags.remove(tag)
        
        self.updated_at = datetime.now()
        return self
    
    def set_solution(self, solution: str):
        """
        Set the solution for the task and update its status.
        
        Args:
            solution (str): The solution to the task.
            
        Returns:
            Task: The updated task (self).
        """
        self.solution = solution
        self.status = "completed"
        self.updated_at = datetime.now()
        return self
    
    def to_dict(self) -> Dict[str, any]:
        """
        Convert the task to a dictionary.
        
        Returns:
            Dict[str, any]: A dictionary representation of the task.
        """
        return {
            "id": self.id,
            "description": self.description,
            "context": self.context,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": self.tags,
            "priority": self.priority,
            "status": self.status,
            "solution": self.solution
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Task':
        """
        Create a Task instance from a dictionary.
        
        Args:
            data (Dict[str, any]): A dictionary containing task data.
            
        Returns:
            Task: A new Task instance.
        """
        # Handle datetime fields
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        return cls(**data)


# Example usage
if __name__ == "__main__":
    # Create a task
    task = Task(
        description="Create a function that calculates the factorial of a number",
        tags=["math", "recursion"],
        priority=4
    )
    
    # Add some context
    task.update(context={"language": "python", "complexity": "medium"})
    
    # Add a tag
    task.add_tags("algorithm")
    
    # Set a solution
    task.set_solution("""
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
""")
    
    # Convert to dictionary
    task_dict = task.to_dict()
    print(task_dict)
    
    # Create from dictionary
    new_task = Task.from_dict(task_dict)
    print(new_task)