from src.repositories import role_repo




def create_role(role: str):

    current_user_role = role_repo.get_role_by_name(role=role)

    if current_user_role:
        print("Роль уже есть!")
        return current_user_role

    role_repo.create_role(role)

    return role_repo.get_role_by_name(role=role)