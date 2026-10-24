from enum import Enum

class OrderStatus(str, Enum):

    FREE = "free"                # Свободен (ожидает водителя)
    IN_PROGRESS = "in_progress"  # В процессе
    CANCELLED = "cancelled"      # Отменен
    COMPLETED = "completed"      # Выполнен