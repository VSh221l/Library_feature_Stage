def test_create_reader(client, create_test_user):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/readers/", json={"name": "Иван Иванов", "email": "ivan@example.com"}, headers=headers)
    assert response.status_code == 201
    assert response.json()["email"] == "ivan@example.com"

    # Дублирование email
    response = client.post("/readers/", json={"name": "Петр Петров", "email": "ivan@example.com"}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email уже занят"

def test_update_reader(client, create_test_user, create_test_reader):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.put(f"/readers/{create_test_reader.id}", json={"name": "Новое имя"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Новое имя"

    # Дублирование email
    response = client.post("/readers/", json={"name": "Петр Петров", "email": "another@example.com"}, headers=headers)
    response = client.put(f"/readers/{response.json()['id']}", json={"email": "reader@example.com"}, headers=headers)
    assert response.status_code == 400
    assert "Email уже занят" in response.json()["detail"]

def test_delete_reader(client, create_test_reader, create_test_user):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete(f"/readers/{create_test_reader.id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Читатель успешно удален"}