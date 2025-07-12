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
            "username": "existing_user_1",
            "email": "existing_1@apriscout.com",
            "password": "athios",
        },
        follow_redirects=True,
    )

    assert b"Username already exists" in response.data


def test_login_logout(client, app):
    """
    Test the login and logout process.

    - Login fails with incorrect password.
    - Login succeeds with correct password.
    - Logout returns HTTP 200.
    """

    response = client.post(
        "/login",
        data={"username": "existing_user_1", "password": "wrong_password"},
        follow_redirects=True,
    )
    assert b"Invalid credentials" in response.data

    response = client.post(
        "/login",
        data={"username": "existing_user_1", "password": "athios"},
        follow_redirects=True,
    )
    assert b"My Page" in response.data

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200


def test_login_capitlisation(client, app):

    response = client.post(
        "/login",
        data={"username": "EXISTING_USER_1", "password": "athios"},
        follow_redirects=True,
    )

    assert b"My Page" in response.data


def test_search(client, app):

    response = client.get(
        "/search",
        query_string={"search_user": "existing_user_2"},
        follow_redirects=True,
    )
    assert b"existing_user_2" in response.data

    response = client.get(
        "/search",
        query_string={"search_user": " nonexisting_user"},
        follow_redirects=True,
    )
    assert b"Username not found" in response.data
