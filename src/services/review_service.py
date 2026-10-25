from src.repositories import review_repo, order_repo


STATUS_COMPLETED = 3

def rate_order(orderID: int, userID: int, rating: int) -> bool:
    if rating < 1 or rating > 5:
        print("Оценка должна быть от 1 до 5")
        return False


    order = order_repo.get_order_by_id(orderID)
    if not order:
        print(f"Заказ №{orderID} не найден")
        return False


    if order.userID != userID:
        print("Вы не можете оценивать чужой заказ")
        return False


    if order.orderStatus != STATUS_COMPLETED:
        print("Можно оценивать только выполненные заказы")
        return False


    if review_repo.has_review_for_order(orderID):
        print("Вы уже оценили этот заказ")
        return False


    success = review_repo.create_review(orderID=orderID, userID=userID, rating=rating)
    if success:
        print(f"Спасибо! Вы оценили заказ №{orderID} на {rating} звезд.")
    return success