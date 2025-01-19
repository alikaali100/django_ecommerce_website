# Online Shop Project

## Table of Contents
- [Overview](#overview)
- [Features](#features)
  - [Authentication](#authentication)
  - [Shopping Cart](#shopping-cart)
  - [Product Management](#product-management)
  - [Search](#search)
  - [Other Features](#other-features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
  - [User Authentication](#user-authentication)
  - [Browse Products](#browse-products)
  - [Search](#search-1)
  - [Manage Cart](#manage-cart)
  - [Checkout](#checkout)
- [API Documentation](#api-documentation-if-applicable)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview
This project is an **Online Shop** with separate frontend and backend implementations, both developed using **Django**. The application provides a seamless shopping experience with modern e-commerce features.

## Features

### Authentication:
- Register and Login with a password.
- Login with OTP (One-Time Password).

### Shopping Cart:
- Add items to the cart.
- Increment/Decrement item quantities in the cart.
- Remove items from the cart.

### Product Management:
- Categorized and sub-categorized items.
- Detailed view for each product.

### Search:
- Search functionality to find products quickly.

### Other Features:
- User-friendly UI.
- Optimized for scalability and maintainability.

## Technologies Used
- **Backend**: Django (Django REST Framework for APIs if applicable).
- **Frontend**: Django Templates (or another frontend framework if specified).
- **Database**: SQLite/PostgreSQL (or the database you're using).
- **Authentication**: Django's built-in authentication and custom OTP implementation.

## Project Structure



## Installation and Setup

Follow these steps to run the project locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo-name/online-shop.git
   cd online-shop
2. **Set up a virtual environment:**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install dependencies:**
   ```bash
    pip install -r requirements.txt
4. **Run Migrations:**
   ```bash
    python manage.py makemigrations
    python manage.py migrate    
5. **Run the Development Server:**
   ```bash
    python manage.py runserver
## 6. Access the Application
Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Usage

### User Authentication:
- Register for a new account or log in using a password or OTP.

### Browse Products:
- Explore products by categories and subcategories.

### Search:
- Use the search bar to find specific products.

### Manage Cart:
- Add, update, or remove items in your shopping cart.

### Checkout:
- Proceed to purchase your selected items.

---

## API Documentation 
Django REST Framework

- **Base URL**: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
- **Example Endpoints**:
  - `GET /products/` - List all products.
  - `POST /cart/add/` - Add item to the cart.
  - `POST /auth/login/` - Log in using credentials.

---
### Contact
If you have any questions or feedback, feel free to contact us at alikaramouzian@icloud.com