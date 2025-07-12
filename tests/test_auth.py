from apriscout.models import User


def test_register_and_login(client, app):

    response = client.post(
        "/register",
        data={
            "username": "new_user",
            "email": "new@apriscout.com",
            "password": "zaros",
        },
        follow_redirects=True,
    )

    assert b"Account created" in response.data

    with app.app_context():
        user = User.query.filter_by(username="new_user").first()
        assert user is not None

    # Login with that user
    response = client.post(
        "/login",
        data={"username": "new_user", "password": "zaros"},
        follow_redirects=True,
    )

    assert b"My Page" in response.data


def test_register_user_exists(client, app):

    response = client.post(
        "/register",
        data={
            "username": "existing_user",
            "email": "existing@apriscout.com",
            "password": "athios",
        },
        follow_redirects=True,
    )

    assert b"Username already exists" in response.data


def test_login_wrong_details(client, app):

    response = client.post(
        "/login",
        data={"username": "existing_user", "password": "wrong_password"},
        follow_redirects=True,
    )

    assert b"Invalid credentials" in response.data


def test_login_logout(client, app):

    response = client.post(
        "/login",
        data={"username": "existing_user", "password": "athios"},
        follow_redirects=True,
    )

    assert b"My Page" in response.data

    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
