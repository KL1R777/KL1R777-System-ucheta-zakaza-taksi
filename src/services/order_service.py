from typing import Optional, List
from src.models.orders import Order
from src.repositories import order_repo


STATUS_FREE = 1
STATUS_IN_PROGRESS = 2
STATUS_COMPLETED = 3
STATUS_CANCELLED = 4


# --- СОЗДАНИЕ ЗАКАЗА ---
def create_order(userID: int, price: float, address: str) -> Optional[int]:
    if price <= 0:
        print("Ошибка: Цена должна быть больше нуля")
        return None


    active_orders = order_repo.get_all_orders(STATUS_FREE) + order_repo.get_all_orders(STATUS_IN_PROGRESS)

    for order in active_orders:
        if order.userID == userID:
            print("Ошибка: У вас уже есть активный заказ! Дождитесь его завершения.")
            return None


    new_id = order_repo.create_order(userID=userID, price=price, address=address)
    if new_id:
        print(f"Заказ №{new_id} успешно создан (ожидает водителя)")
    return new_id



def take_order(id: int, driverID: int) -> bool:

    in_progress_orders = order_repo.get_all_orders(STATUS_IN_PROGRESS)
    for order in in_progress_orders:
        if order.driverID == driverID:
            print("Ошибка: Вы уже везете заказ! Сначала завершите его.")
            return False


    free_orders = order_repo.get_all_orders(STATUS_FREE)
    target_order = None
    for order in free_orders:
        if order.id == id:
            target_order = order
            break

    if not target_order:
        print("Ошибка: Заказ не найден или его уже забрал другой водитель")
        return False


    order_repo.take_order(id=id, driverID=driverID)
    print(f"✅ Водитель {driverID} успешно взял заказ №{id}!")
    return True



def completed_order(id: int, driverID: int):
    order = order_repo.get_order_by_id(id)

    if not order:
        print(f"Заказ №{id} не найден.")
        return

    if order.driverID != driverID:
        print("Этот заказ принадлежит другому водителю.")
        return

    if order.orderStatus != STATUS_IN_PROGRESS:
        print("Нельзя завершить заказ, который отменен или еще не принят в работу.")
        return

    order_repo.completed_order(id=id, driverID=driverID)
    print(f"Заказ №{id} успешно выполнен.")



def cancelled_order(id: int, userID: int):
    order = order_repo.get_order_by_id(id)

    if not order:
        print(f"Заказ №{id} не найден.")
        return

    if order.userID != userID:
        print("Вы не можете отменить чужой заказ.")
        return

    if order.orderStatus in (STATUS_COMPLETED, STATUS_CANCELLED):
        print("Нельзя отменить уже выполненный или отмененный заказ.")
        return

    order_repo.cancelled_order(id=id)
    print(f"Заказ №{id} отменен.")


def get_available_orders() -> List[Order]:
    return order_repo.get_all_orders(STATUS_FREE)



def get_history(userID: int):
    orders = order_repo.get_orders_by_user_id(userID)
    if not orders:
        print("У вас еще нет заказов.")
        return []

    print(f"\n--- История заказов пользователя {userID} ---")
    for o in orders:
        status_text = "Неизвестно"
        if o.orderStatus == STATUS_FREE:
            status_text = "Ожидает водителя"
        elif o.orderStatus == STATUS_IN_PROGRESS:
            status_text = "В пути"
        elif o.orderStatus == STATUS_COMPLETED:
            status_text = "Выполнен"
        elif o.orderStatus == STATUS_CANCELLED:
            status_text = "Отменен"

        print(f"Заказ №{o.id} | Адрес: {o.address} | Цена: {o.price} | Статус: {status_text}")
    return orders



def check_status(orderID: int) -> int | None:
    order = order_repo.get_order_by_id(orderID)
    if not order:
        print(f"Заказ №{orderID} не найден.")
        return None

    statuses = {
        1: "Ожидает водителя",
        2: "Водитель в пути",
        3: "Выполнен",
        4: "Отменен"
    }
    print(f"Статус заказа №{orderID}: {statuses.get(order.orderStatus, 'Неизвестно')}")
    return order.orderStatus


import random

def calculate_price(address: str) -> float:

    if not address or len(address) < 5:
        return 0.0

    return float(150 + random.randint(50, 300))