import bcrypt

from src.auth_service.app.schemas import UserCreateInSchema
from src.auth_service.app.models import User


async def test_register_route(client, user, init_db):
    credential = UserCreateInSchema(
        username=user.username,
        password=user.hashed_password,
        email=user.email,
    ).model_dump()

    response = await client.post("/api/auth/register", json=credential)
    data = response.json()

    assert response.status_code == 201
    assert "refresh_token" in data
    assert "access_token" in data


async def test_login_route(client, user, init_db, session):
    hashed_password = bcrypt.hashpw(password=user.hashed_password.encode("utf-8"), salt=bcrypt.gensalt()).decode("utf-8")
    user_in_db = User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
    )
    session.add(user_in_db)
    await session.commit()

    form_data = {
        "username": user.username,
        "password": user.hashed_password,
    }

    response = await client.post("/api/auth/login", data=form_data)
    data = response.json()

    assert response.status_code == 200
    assert "refresh_token" in data
    assert "access_token" in data


async def test_token_route(client, jwt_service, user):
    refresh_token = jwt_service.get_refresh_token(str(user.id))
    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }

    response = await client.post("/api/auth/token", headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert "refresh_token" in data
    assert "access_token" in data
    assert data.get("refresh_token") == refresh_token
