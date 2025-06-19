from faker import Faker

from app.users.models import User
from app.utils.id_generator import generate_id


def test_user_from_dynamo_parses_correctly(faker: Faker) -> None:
    user_id = generate_id("usr")
    name = faker.name()
    date_of_birth = faker.date_of_birth()

    dynamo_item = {
        "id": {"S": user_id},
        "name": {"S": name},
        "date_of_birth": {"S": date_of_birth.isoformat()},
    }

    expected_user = User(id=user_id, name=name, date_of_birth=date_of_birth)

    user = User.from_dynamo(dynamo_item)

    assert user == expected_user

def test_user_to_dynamo_parses_correctly(faker: Faker) -> None:
    user_id = generate_id("usr")
    name = faker.name()
    date_of_birth = faker.date_of_birth()

    user = User(id=user_id, name=name, date_of_birth=date_of_birth)

    expected_item = {
        "id": {"S": user_id},
        "name": {"S": name},
        "date_of_birth": {"S": date_of_birth.isoformat()}
    }

    assert user.to_dynamo() == expected_item

