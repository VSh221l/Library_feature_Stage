def test_register_user(client):
    response = client.post("/auth/register", json={"email": "new_user@example.com", "password": "password123"})
    assert response.status_code == 201, f"Failed to register user: {response.json()}"
    assert response.json() == {"message": "Пользователь успешно зарегистрирован"}

def test_register_duplicate_email(client, create_test_user):
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email уже зарегистрирован"}

def test_login_success(client, create_test_user):
    response = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client, create_test_user):
    response = client.post("/auth/token", json={"email": "wrong@example.com", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Неверный email или пароль"}

def test_protected_endpoint_no_token(client):
    response = client.get("/books/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}