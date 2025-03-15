# shopproject
Django basic eshop project.

Quick start
-----------

1. Clone repo  like this::

      git clone  https://github.com/dimkoug/shopproject.git

2. Create a virtualenv inside backend folder::

    python -m venv venv

3. Activate venv

4. Install packages from requirements.txt file

5. Create settings_local.py with settings from settings_local_sample.py

6. Run `python manage.py makemigrations addresses baskets brands heroes logos media offers orders profiles products tags users`

7. Run `python manage.py migrate`

8. Start the development server and visit http://127.0.0.1:8000/
