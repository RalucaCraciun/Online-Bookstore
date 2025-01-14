import requests

BASE_URL = "http://localhost:8000"  # Update this if your app runs on a different port


def test_root():
    """
    Test the root endpoint.
    """
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Hellow World"}


# Authentication Routes
def test_register_user():
    """
    Test user registration.
    """
    response = requests.post(
        f"{BASE_URL}/register",
        params={
            "name": "Test User",
            "email": "test.user@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200 or response.status_code == 400  # Already exists check
    assert "userId" in response.json() or "detail" in response.json()


def test_login_user():
    """
    Test user login and retrieve access token.
    """
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": "test.user@example.com",
            "password": "password123",
            "grant_type": "password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    return response.json()["access_token"]


def test_get_profile():
    """
    Test retrieving the logged-in user's profile.
    """
    token = test_login_user()
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "email" in response.json()


def test_logout_user():
    """
    Test logging out the user.
    """
    token = test_login_user()
    response = requests.post(
        f"{BASE_URL}/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User logged out successfully"


# Books Routes
def test_retrieve_books():
    """
    Test retrieving all books.
    """
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    assert "books" in response.json()


def test_add_book():
    """
    Test adding a new book to the store.
    """
    response = requests.post(
        f"{BASE_URL}/books",
        json={
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "genre": "Fiction",
            "price": 15.99,
            "description": "A classic novel about the American Dream.",
            "stock": 50
        }
    )
    assert response.status_code == 201
    assert "bookId" in response.json()


def test_retrieve_book_details():
    """
    Test retrieving a specific book's details.
    """
    # Add a book first
    book_response = requests.post(
        f"{BASE_URL}/books",
        json={
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "genre": "Fiction",
            "price": 15.99,
            "description": "A classic novel about the American Dream.",
            "stock": 50
        }
    )
    book_id = book_response.json()["bookId"]

    # Retrieve book details
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 200
    assert "book" in response.json()


# Cart Routes
def test_add_item_to_cart():
    """
    Test adding an item to the user's cart.
    """
    token = test_login_user()
    response = requests.post(
        f"{BASE_URL}/cart",
        json={
            "bookId": "abc123",
            "quantity": 2
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "items" in response.json()


def test_retrieve_cart():
    """
    Test retrieving the current user's cart.
    """
    token = test_login_user()
    response = requests.get(
        f"{BASE_URL}/cart",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "items" in response.json()


def test_remove_item_from_cart():
    """
    Test removing an item from the user's cart.
    """
    token = test_login_user()
    # Add an item to cart
    requests.post(
        f"{BASE_URL}/cart",
        json={
            "bookId": "abc123",
            "quantity": 2
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Remove the item
    response = requests.delete(
        f"{BASE_URL}/cart/abc123",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Book abc123 removed from cart successfully."


# Order Routes
def test_create_order_from_cart():
    """
    Test creating an order from the user's cart.
    """
    token = test_login_user()
    # Add an item to cart
    requests.post(
        f"{BASE_URL}/cart",
        json={
            "bookId": "abc123",
            "quantity": 2
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Create an order
    response = requests.post(
        f"{BASE_URL}/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert "orderId" in response.json()


def test_place_order():
    """
    Test placing an order.
    """
    token = test_login_user()
    # Add an item to cart and create an order
    requests.post(
        f"{BASE_URL}/cart",
        json={
            "bookId": "abc123",
            "quantity": 2
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    order_response = requests.post(
        f"{BASE_URL}/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    order_id = order_response.json()["orderId"]

    # Place the order
    response = requests.post(
        f"{BASE_URL}/orders/{order_id}/place",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Placed"
