# Data Collation System

The **Data Collation System** is a web application designed for securely collecting, managing, and analyzing data for NDC members and monitors. The platform provides a robust system for data entry, report generation, and user management with a modern, user-friendly interface.

---

## Features

- **Role-Based Login**:
  - **Party Members**: Log in with a generated agent code to input personal details.
  - **Monitors**: Log in with an email and password to access reports, manage data, and export information.
  
- **Data Management**:
  - Collect and store party members' details securely.
  - Edit, delete, and export data (Excel, PDF).

- **Reports**:
  - View interactive charts and tables.
  - Filter data by parameters like age and occupation.

- **Responsive UI**:
  - Modern design with smooth effects.
  - Mobile-friendly and easy to navigate.

---

## Technology Stack

- **Backend**: Python, Django
- **Frontend**: Bootstrap, Custom CSS
- **Database**:  MySQL
- **Deployment**: Docker

---

## Installation

### Prerequisites
- Python 3.10 or higher
- PostgreSQL or MySQL
- Docker (for containerized deployment)

### Clone the Repository
```bash
git clone https://github.com/mmanueljoe/datacollation.git
cd datacollation
```

### Set Up Environment
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and configure it:
   ```env
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1
   DJANGO_DB_NAME=datacollation_db
   DJANGO_DB_USER=your_db_user
   DJANGO_DB_PASSWORD=your_db_password
   DJANGO_DB_HOST=localhost
   DJANGO_DB_PORT=3306
   ```

### Database Setup
1. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

---

## Running the Application

1. Start the development server:
   ```bash
   python manage.py runserver
   ```
   Access the app at [http://127.0.0.1:8000](http://127.0.0.1:8000).

2. To run using Docker:
   ```bash
   docker build -t datacollation .
   docker run -d -p 8000:8000 datacollation
   ```

---

## Usage

### Member Login
- Navigate to the **Member Login** page.
- Enter the agent code and password.
- Fill out the data collection form.

### Monitor Dashboard
- Navigate to the **Monitor Login** page.
- Log in with your email and password.
- View, edit, and manage member data.

---

## Deployment

For VPS deployment, use the provided Dockerfile and `.env` file. Follow these steps:

1. Build the Docker image:
   ```bash
   docker build -t datacollation .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env datacollation
   ```

3. Access the app on your server's IP or domain at `http://<server-ip>:8000`.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributing

We welcome contributions! Feel free to fork the repository and submit a pull request.

---

## Contact

For any inquiries or issues, contact [emmanuelletsu18@gmail.com](mailto:your-email@example.com).

---