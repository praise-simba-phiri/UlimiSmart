# 🌾 Ulimi-Smart: Smart Agricultural Assistant for Malawi 🇲🇼

**Ulimi-Smart** is an intelligent, user-friendly, web-based agricultural management system designed specifically for Malawian farmers. This platform empowers farmers to manage crop records, predict crop yields (maize and tobacco), plan farming schedules, and track expenses and profits. Developed by **Group 5**, this system leverages machine learning and modern web technologies to support data-driven farming.

---

## 📌 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Model Training](#model-training)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Features

- 🌽 Predict crop yields for **maize** and **tobacco** using machine learning models.
- 🧾 Record and manage multiple **farms**, **crops**, and **expenses**.
- 📆 Plan and track **planting**, **harvesting**, and **seasonal activities**.
- 📊 Monitor **profitability** and financial health over time.
- 📂 Keep logs of **weather**, **soil**, and **growth** observations.
- 📅 Forecast crop output to inform market planning and household food security.
- 🔒 Secure login and authentication (JWT-ready).
- 🌐 Built by Malawians, for Malawians — tailored to local needs.

---

## 🛠 Tech Stack

| Category          | Technology               |
|------------------|--------------------------|
| Backend          | Django 4.2+, Django REST Framework |
| Frontend         | HTML5, Tailwind CSS      |
| Database         | PostgreSQL               |
| ML Frameworks    | scikit-learn, pandas, joblib |
| Authentication   | djangorestframework-simplejwt |
| Other Tools      | dotenv, CORS headers     |

---

## 🧱 Architecture

Ulimi-Smart is structured using Django's modular app system. Each functional domain is a separate Django app:

- `core`: Core utilities and base models
- `farms`: Farm profiles and locations
- `crops`: Crop types and attributes
- `records`: Historical crop records
- `observations`: Soil, weather, and growth notes
- `expenses`: Cost tracking for each farm and season
- `profits`: Revenue and profit calculations
- `models`: Machine learning model training and loading
- `predictions`: Yield prediction logic
- `planning`: Future crop planning and calendar management

---

## 📦 Installation

1. **Clone the repo**:
    ```bash
    git clone https://github.com/group5/ulimi-smart.git
    cd ulimi-smart
    ```

2. **Create virtual environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate   # On Windows
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Start server**:
    ```bash
    python manage.py runserver
    ```

---

## 📁 Folder Structure (Simplified)

ulimi-smart/
├── apps/
│ ├── crops/
│ ├── expenses/
│ ├── farms/
│ ├── models/
│ ├── planning/
│ └── ...
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md


---

## 🧠 Model Training

### Dataset Format:
Upload `.csv` datasets for maize and tobacco with features like:
- Rainfall, Soil Type, Fertilizer Type, Farm Size, etc.
- Target column: `yield` or `production`

### Steps:
1. Place your dataset in `apps/models/datasets/`.
2. Run training scripts provided in `apps/models/train.py`.
3. Trained models are saved using `joblib` and loaded in the prediction app.

---

## 👥 Contributing

> This is a university group project developed by **Group 5**, ICT Department, Mzuzu University.

If you'd like to contribute, please fork the repo and submit a pull request. Let’s help Malawi’s agriculture thrive through smart solutions! 🇲🇼

---

## 📄 License

This project is licensed for academic purposes only. For public or enterprise use, please contact the maintainers.

---

**Group 5 | Mzuzu University | 2025**
