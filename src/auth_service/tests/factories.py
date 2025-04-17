import factory
from src.auth_service.app.models import User
from src.auth_service.app.enums import UserRoleEnum


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    hashed_password = factory.Faker("password")
    is_deleted = False
    is_active = True
    role = UserRoleEnum.USER
