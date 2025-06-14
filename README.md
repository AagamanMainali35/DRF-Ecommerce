# DRF E-Commerce API

A robust e-commerce backend built with Django REST Framework (DRF), providing APIs for user authentication, product management, carts, orders, and more. The project uses JWT for authentication and Swagger for API documentation.

---

## Project Overview

This backend API handles:

- User registration, login, and JWT authentication  
- Product catalog management (CRUD)  
- Shopping cart functionality  
- Order processing  
- Swagger-based API documentation  
- Secure RESTful APIs for e-commerce operations

---

## Tech Stack

- Python 3.x  
- Django 5.x  
- Django REST Framework  
- djangorestframework-simplejwt (JWT Authentication)  
- drf-yasg (Swagger Documentation)  
- PostgreSQL / SQLite (configurable)  
- requests library

---

## Setup & Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/AagamanMainali35/DRF-Ecommerce.git
   cd DRF-Ecommerce
   ```

2. **Create and activate a virtual environment**

   - **Windows (PowerShell or CMD):**

     ```bash
     python -m venv env
     env\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r Documents/packages.txt
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

---

## API Documentation

Access Swagger UI for interactive API docs at:

```
http://127.0.0.1:8000/swagger/
```

---

## Testing API with Postman

Use the Postman collection at:

```
Documents/DRF-Ecommerce.postman_collection.json
```

- Open Postman  
- Import this collection file  
- Test all API endpoints easily  
- Ensure your Django server is running while testing

---

## Authentication

- JWT tokens are used for secure authentication  
- Obtain tokens at `/api/token/` endpoint  
- Use the access token in the `Authorization` header:  
  `Bearer <access_token>`  
- Refresh tokens via `/api/token/refresh/`

---

## Notes

- Configure your database in `settings.py` if you want to use PostgreSQL or other DB instead of SQLite  
- Use environment variables for sensitive info in production  
- APIs include full CRUD for products, carts, orders with role-based permissions

---

## Contributing

Contributions are welcome! Please open issues or pull requests.

---

## Contact

For questions or help, reach out at: [Your Email]

---

Happy coding! 🚀
