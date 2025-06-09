# Restaurant Portal — Django Project

This is a Django-based restaurant review portal.

---

## Setup Instructions

### Common Steps for All Setups

1. **Clone the repository**

   ```bash
   git clone https://github.com/Mikokii/Internet-application
   ```

2. **Activate the virtual environment**

   ```bash
   Restaurant_Venv\Scripts\activate
   ```

3. **Install required packages**

   ```bash
   cd Restaurant_Portal
   pip install -r requirements.txt
   ```

---

## Option 1: Normal Setup (Fresh Database)

If you want to start with a clean database:

1. **Delete the existing database file**

   ```bash
   del db.sqlite3
   ```

2. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

3. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server**

   ```bash
   python manage.py runserver
   ```

5. **Go to the admin panel**

   ```
   http://127.0.0.1:8000/admin/
   ```

6. **Log in using the superuser you created and add content to the database**

7. **Go to the app**

   ```
   http://127.0.0.1:8000/
   ```

---

## Option 2: Included Database (With Preloaded Data)

If you're using the project with the pre-existing `db.sqlite3` (included in the repository):

1. **Run the development server**

   ```bash
   python manage.py runserver
   ```
2. **Go to the admin panel**

   ```
   http://127.0.0.1:8000/admin/
   ```

3. **Log in using the following credentials**:

   * **Username**: `mikokii`
   * **Password**: `1234`

4. **Add or modify content in the database through the admin interface**

5. **Go to the app**
   ```
   http://127.0.0.1:8000/
   ```
---