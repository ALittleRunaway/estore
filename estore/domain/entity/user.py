from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    surname: str
    patronymic: str
    role: str
