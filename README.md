# Online-Bookstore

The Online Bookstore is a comprehensive platform designed to streamline the process of discovering, searching for, and purchasing books online.The application caters to book enthusiasts and provides tools for both readers and administrators to manage the platform effectively.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Group Members](#group-members)

## Project Overview 
The Online Bookstore is a web application that integrates Elasticsearch to demonstrate its potential in building search-driven solutions. The platform offers users the ability to explore a rich collection of books through advanced search features, facilitating a smooth and enjoyable browsing experience.

## Features
- **User Registration and Authentication**: Register and authenticate securely with unique user credentials.
- **Search and Filtering**: Books can be easily found by keyword-based searches across titles, authors, genre and can be filtered by tpublication date, price range, ratings, and availability.
- **Book Management System**: Users can browse categorized book collections for better discoverability and ccess detailed book information, including author details, descriptions, pricing, and stock levels
- **Shopping Cart and Checkout**: Users can add books to the shopping cart and modify the contents before proceeding to checkout where they have available secure payment systems for order processing.


## Group Members
- Craciun Raluca
- Gradinaru Alina
- Ion Ioana Nicola
- Nastase Ana-Maria

## RESTFUL Resources
1. Authentication and User Management:
   
- POST /register: 
Register a new user with required details (e.g., name, email, password).
Request Body: name, email, password
Response: Status code 201 if successful, with user ID and token.
- POST /login:
Authenticate a user and return a JWT token for authorized access.
Request Body: email, password
Response: Status code 200 if successful, with JWT token.
POST /logout:
End the user session and invalidate the token.
Response: Status code 200 if successful.

2.Users:

- PUT /users/{userId}:
Update a user’s profile (authenticated users only).
Parameters: userId (path):
Request Body: Optional fields such as name, email, location
Response: Status code 200 with updated user data.

3.Books:

- GET /books:
Retrieve a list of books.
Query Parameters: Optional filters such as title, author, genre, priceRange, rating
Response: Status code 200 with a list of books matching filters.
- GET /books/{bookId}:
Retrieve details of a specific book.
Parameters: bookId (path)
Response: Status code 200 with book details (e.g., title, author, description).
- POST /books:
Add a new book to the store (admin-only action).
Request Body: title, author, genre, price, description, stock
Response: Status code 201 with the newly created book ID and details.
- PUT /books/{bookId}:
Update details of a book (admin-only action).
Parameters: bookId (path)
Request Body: Fields to update such as title, genre, price
Response: Status code 200 with updated book details.
- DELETE /books/{bookId}:
Remove a book from the store (admin-only action).
Parameters: bookId (path)
Response: Status code 204 if successful.

4.Shopping Cart:

- POST /cart:
  Add an item to the shopping cart.
Request Body: bookId, quantity
Response: Status code 201 if successful, with updated cart details.
- GET /cart:
  Retrieve the current contents of the shopping cart.
Response: Status code 200 with cart details.
- DELETE /cart/{bookId}:
Remove a specific book from the cart.
Parameters: bookId (path)
Response: Status code 204 if successful.

6.Orders:

- POST /orders:
Place an order for the items in the shopping cart.
Response: Status code 201 if successful, with order ID and details.

- GET /orders/{orderId}:
Retrieve the details of a specific order.
Parameters: orderId (path)
Response: Status code 200 with order details (e.g., items, totalPrice, status).






