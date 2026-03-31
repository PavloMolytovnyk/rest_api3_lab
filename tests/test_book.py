import pytest
from httpx import AsyncClient
from main import app
from uuid import uuid4

BASE_URL = "http://testserver"

@pytest.mark.asyncio
async def test_create_book():
    """Тест створення книги через API"""
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        payload = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "description": "A Handbook of Agile Software Craftsmanship",
            "status": "available",
            "year": 2008
        }
        response = await ac.post("/books/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Clean Code"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_books_cursor_pagination():
    """Тест Cursor пагінації: перевіряємо, що запит повертає список"""
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/books/?limit=1")
        assert response.status_code == 200
        
        books = response.json()
        if len(books) > 0:
            last_id = books[0]["id"]
            next_response = await ac.get(f"/books/?limit=1&cursor={last_id}")
            assert next_response.status_code == 200

@pytest.mark.asyncio
async def test_get_book_by_id_not_found():
    """Тест отримання неіснуючої книги"""
    fake_id = uuid4()
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get(f"/books/{fake_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"