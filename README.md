# URL Shortener

URL Shortener is a Django project that provides a simple and user-friendly way to shorten URLs. It includes a RESTful API built with Django REST framework for creating, updating, retrieving, and deleting short URLs. The short URLs are generated based on the structure of the original URLs, making them easy to remember and share. The project also includes a redirection feature that seamlessly redirects users from short URLs to their original destinations.

## Features

- Create short URLs from long URLs
- Retrieve short URLs and their corresponding long URLs
- Update existing short URLs
- Delete short URLs
- Redirect users from short URLs to original URLs

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/url-shortener.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run migrations:
   ```bash
   python manage.py migrate

4. Start the development server
   ```bash
   python manage.py runserver


## Endpoints

1. **Create a short URL**
   POST http://localhost:8000/api/urls/
   Body: {"long_url": "https://www.example.com/"}

2. **Retrieval a short URL**
   GET http://localhost:8000/api/urls/<id>

3. **Update a short URL**
   PUT http://localhost:8000/api/urls/<id>/
   Body: {"long_url": "https://www.example.com/new/"}

4. **Delete a short URL**
   DELETE http://localhost:8000/api/urls/<id>/

5. **Redirect from a short URL**
    Open `http://localhost:8000/<short_url>/` in your web browser

