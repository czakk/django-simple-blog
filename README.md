# Simple Django Blog

This is a simple Django application for creating and managing a blog. It provides basic functionality for creating 
blog posts, as well as allowing users to view and comment on posts.
## Features

- Blog post management: Users can create blog posts.
- Post listing: Users can view a list of all published blog posts.
- Post details: Users can view the details of a specific blog post, including comments.
- Commenting: Users can leave comments on blog posts.
- Admin panel: Administrators can manage users, posts, and comments through the Django admin panel.
## Technology Used
- Django: a Python web framework for building the application backend.
- Python: the programming language used for developing the application.
- HTML: the markup language for creating web pages.
- CSS: the stylesheet language for styling web pages.
- Tailwind CSS: a utility-first CSS framework used for creating responsive and efficient user interfaces.
- SQLite: the default database engine used for development.

## Requirements

- Python 3.11
- Django 4.2

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/simple-blog-django.git
   ```
2. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```
3. Run docker-compose:

   ```shell
   docker-compose up
   ```

## Usage

1. Apply the database migrations:

   ```shell
   python manage.py migrate
   ```

2. Create a superuser (admin):

   ```shell
   python manage.py createsuperuser
   ```

3. Start the development server:

   ```shell
   python manage.py runserver
   ```

4. Access the application in your web browser at `http://localhost:8000`.

5. To access the admin panel, go to `http://localhost:8000/admin` and log in with the superuser credentials.
