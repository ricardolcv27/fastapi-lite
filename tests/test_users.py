import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test de creación de usuario usando fixture de cliente con DB en memoria"""
    response = await client.post(
        "/users", 
        json={"email": "test@example.com", "full_name": "Test User"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_duplicate_user(client: AsyncClient):
    """Test que verifica que no se pueden crear usuarios duplicados"""
    user_data = {"email": "duplicate@example.com", "full_name": "Duplicate User"}
    
    # Crear primer usuario
    response1 = await client.post("/users", json=user_data)
    assert response1.status_code == 200
    
    # Intentar crear usuario duplicado
    response2 = await client.post("/users", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_read_user(client: AsyncClient):
    """Test de lectura de usuario por ID"""
    # Crear usuario
    create_response = await client.post(
        "/users", 
        json={"email": "read@example.com", "full_name": "Read User"}
    )
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]
    
    # Leer usuario
    read_response = await client.get(f"/users/{user_id}")
    assert read_response.status_code == 200
    data = read_response.json()
    assert data["email"] == "read@example.com"
    assert data["full_name"] == "Read User"


@pytest.mark.asyncio
async def test_read_nonexistent_user(client: AsyncClient):
    """Test que verifica el manejo de usuarios inexistentes"""
    response = await client.get("/users/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
