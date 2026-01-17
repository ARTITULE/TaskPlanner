from dataclasses import dataclass


@dataclass
class Task:
    id: str
    title: str
    completed: bool = False
