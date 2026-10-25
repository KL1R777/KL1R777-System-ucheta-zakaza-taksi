from enum import Enum

class OrderStatus(str, Enum):

    FREE = "free"                
    IN_PROGRESS = "in_progress"  
    CANCELLED = "cancelled"      
    COMPLETED = "completed"      