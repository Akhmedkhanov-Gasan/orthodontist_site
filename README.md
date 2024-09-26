Вот форматированный `README.md` с вашим описанием:

```markdown
# Orthodontist Appointment Booking

## Description

The **Orthodontist Appointment Booking** system is a web application designed to allow users to easily book appointments for dental services. 
The project is built using Django and offers a simple interface for users to submit their name, contact information, appointment date, and time. 
The data is saved in a text file for easy management.

Key features include:
- Simple appointment booking form with date and time pickers.
- Responsive design using Bootstrap and Wow.js for animations.
- Static pages such as "About Us", "Pricing", "Contact", and "Testimonials".
- Appointment data stored in a text file for easy access.

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone git@github.com:Akhmedkhanov-Gasan/orthodontist_site.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd orthodontist-site
    ```

3. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8. **Open your browser and go to:**
    ```
    http://127.0.0.1:8000/
    ```


## Directory Structure

```plaintext
.
├── orthodontist_site/        # Django project folder
├── main/        			  # Main Django App
├── appointments/             # App for managing appointment bookings
├── static/                   # Static files (CSS, JavaScript, images)
├── templates/                # HTML templates
├── appointments.txt          # Text file storing appointment data
├── manage.py                 # Django management script
├── Procfile                  # For deployment on services like Render
└── README.md                 # This README file
```
```

## License

This project is open-source and available under the [MIT License](LICENSE).
```