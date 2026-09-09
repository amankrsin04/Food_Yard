# FoodYard – Food Donation Management System

FoodYard is a Flask + SQLite college project for managing surplus food donations.

## Main features

- Professional responsive UI
- Donor registration and login
- **Separate Admin Login**
- **Separate Donor Login**
- Role-based route protection
- Donor dashboard with personal donation history
- Admin dashboard with all donations
- Donation status workflow
- Donor management view
- Contact messages visible to admin
- Password hashing with Werkzeug
- SQLite database
- Mobile responsive design

## Role access

### Donor
URL: `/donor/login`

A donor can:
- Register an account
- Login
- Submit food donations
- View only their own donations
- Track donation status
- Logout

### Admin
URL: `/admin/login`

Demo credentials:

```text
Email: admin@foodyard.com
Password: admin123
```

An admin can:
- View all donations
- View donor information
- Update donation status
- View contact messages
- Logout

## Important security rule

The registration page always creates a `donor` account. Admin accounts are not created through public registration.

The application checks the user's database role during login and also protects routes with role-based decorators.

## Run locally

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Project structure

```text
FoodYard_Final/
├── app.py
├── foodyard.db
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── donate.html
│   ├── admin.html
│   ├── about.html
│   ├── contact.html
│   └── 404.html
└── static/
    ├── css/style.css
    ├── js/app.js
    └── images/logo.svg
```

## Technology

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Werkzeug password hashing

## College-project explanation

FoodYard solves a simple problem: surplus food can be recorded and managed digitally instead of being wasted.

There are two roles:

1. **Donor** – adds food donation details and tracks their own submissions.
2. **Admin** – manages the complete donation workflow and can see all donor submissions.

The backend uses SQLite for storage and Flask handles routing, authentication and role-based access.
