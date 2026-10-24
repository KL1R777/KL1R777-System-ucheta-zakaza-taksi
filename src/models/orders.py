from typing import Optional
from dataclasses import dataclass

@dataclass
class Order:
    id: int
    userID: int
    price: float
    driverID: Optional[int]  # Может быть NULL (если водитель еще не назначен)
    orderStatus: int