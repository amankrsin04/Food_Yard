# 🍱 FoodYard — Food Donation & Management System

FoodYard is a web-based **Food Donation and Management System** designed to connect food donors with administrators who manage food donation records and distribution activities.

The system provides separate access for **Donors** and **Admins**, making it easier to manage donations, track food availability, and maintain organized records through a simple web interface.

---

## 🚀 Features

### 👤 Donor Module

* Donor registration and login
* Secure donor access
* Add new food donations
* Enter food details and quantity
* Specify food availability
* View submitted donations
* Track donation status

### 🛡️ Admin Module

* Separate admin login
* Admin dashboard
* View all donations
* Manage donation records
* Update donation status
* Monitor available food
* Manage donor information

### 📊 Dashboard

* Total donations
* Pending donations
* Completed donations
* Available food
* Donor statistics
* Recent donation activity

---

## 🧠 How FoodYard Works

```text
              ┌─────────────────┐
              │     FoodYard    │
              │      System     │
              └────────┬────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
     👤 Donor                   🛡️ Admin
          │                         │
     Login/Register             Admin Login
          │                         │
     Add Donation              Dashboard
          │                         │
     Food Details               Manage Data
          │                         │
          └────────────┬────────────┘
                       │
                  🗄️ Database
                       │
                  SQLite Database
```

---

## 🛠️ Technologies Used

| Technology   | Purpose                       |
| ------------ | ----------------------------- |
| 🐍 Python    | Backend development           |
| 🌐 Flask     | Web application framework     |
| 🗄️ SQLite   | Database management           |
| 🎨 HTML5     | Web page structure            |
| 🎨 CSS3      | Styling and responsive design |
| ⚡ JavaScript | Frontend interactions         |
| 🔐 Sessions  | Login and access control      |

---

## 📁 Project Structure

```text
FoodYard/
│
├── app.py
├── foodyard.db
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── donor_dashboard.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── ...
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FoodYard.git
```

### 2. Open the project

```bash
cd FoodYard
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

### 7. Open in browser

```text
http://127.0.0.1:5000
```

---

## 🔐 User Roles

FoodYard uses separate access levels.

### Donor

Donors can:

```text
Register
   ↓
Login
   ↓
Donor Dashboard
   ↓
Submit Food Donation
   ↓
Track Donation
```

### Admin

Admins can:

```text
Admin Login
   ↓
Admin Dashboard
   ↓
View Donations
   ↓
Manage Donations
   ↓
Update Status
```

This separation prevents donors from accessing administrative functionality.

---

## 🗃️ Database

FoodYard uses **SQLite** for storing application data.

The database can contain information such as:

* Donor accounts
* Food donations
* Food quantity
* Food type
* Pickup/delivery information
* Donation status
* Timestamps

SQLite makes the project lightweight and easy to run locally without requiring a separate database server.

---

## 📊 Donation Status

A donation can move through different stages:

```text
Pending
   ↓
Accepted
   ↓
Collected
   ↓
Completed
```

This allows administrators to monitor the progress of food donations.

---

## 🎯 Project Objectives

The main objectives of FoodYard are:

1. Create a digital platform for food donation management.
2. Make food donation submission easier.
3. Provide separate donor and admin access.
4. Maintain organized donation records.
5. Allow administrators to monitor donations.
6. Reduce manual record keeping.
7. Encourage efficient food redistribution.

---

## 🌍 Social Impact

FoodYard is designed around the idea of reducing **food wastage** while helping organizations coordinate surplus food donations.

The platform can potentially be extended to connect:

```text
Restaurants
     │
     ├── Surplus Food
     │
     ↓
  FoodYard
     │
     ↓
Organizations / Volunteers
     │
     ↓
People in Need
```

---

## 🔮 Future Enhancements

Possible future improvements include:

* 📍 Location-based donation matching
* 🗺️ Google Maps integration
* 📱 Mobile application
* 🔔 Email/SMS notifications
* 📦 Real-time donation tracking
* 👥 NGO/volunteer accounts
* 📈 Advanced analytics dashboard
* ☁️ Cloud database
* 🔐 Password hashing and stronger authentication
* 🤖 AI-based food demand prediction

---

## 🧪 Testing

The application can be tested by creating separate accounts and checking each role.

### Donor Testing

```text
Register → Login → Add Donation → View Donation
```

### Admin Testing

```text
Admin Login → Dashboard → View Donations → Update Status
```

---

## 🎓 Academic Project

**Project Name:** FoodYard — Food Donation & Management System

**Project Type:** Web Application

**Backend:** Python + Flask

**Database:** SQLite

**Frontend:** HTML, CSS & JavaScript

**Purpose:** Food Donation Management

---

## 👨‍💻 Author

**Aman Kumar Singh**

MCA — Computer Applications
SRM Institute of Science and Technology, Ghaziabad

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

### 📌 Disclaimer

FoodYard is developed as an **academic/college project** to demonstrate web development, database management, authentication, and role-based access control.
