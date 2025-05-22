# 💺 Medical Diagnosis Support System

An AI-powered web application designed to assist users in identifying potential diseases based on their symptoms. This system leverages machine learning models and natural language processing to provide preliminary diagnostic support.

---

## 📋 Table of Contents

* [Overview](#overview)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Technologies Used](#technologies-used)
* [Contributing](#contributing)
* [License](#license)
* [Disclaimer](#disclaimer)

---

## 📖 Overview

The **Medical Diagnosis Support System** is a Django-based web application that predicts possible diseases based on user-inputted symptoms. By analyzing symptom data, the system provides users with potential diagnoses, aiming to offer preliminary insights before consulting healthcare professionals.

---

## ✨ Features

* **Symptom-Based Disease Prediction**: Input symptoms to receive a list of potential diseases.
* **Interactive Web Interface**: User-friendly interface for symptom input and result display.
* **Machine Learning Integration**: Utilizes trained models to analyze symptoms and predict diseases.
* **Modular Codebase**: Organized structure for scalability and maintenance.

---

## 🗂️ Project Structure

```
Medical-Diagnosis-Support-System/
├── assistant/
│   ├── templates/
│   │   ├── assistant/
│   │   │   ├── index.html
│   │   │   └── result.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── healthcare_assistant/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .gitignore
├── all_installed.txt
├── manage.py
├── requirements.txt
└── train_model.py
```

---

## 🛠️ Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Naveennainola/Medical-Diagnosis-Support-System.git
   cd Medical-Diagnosis-Support-System
   ```

2. **Create a Virtual Environment** (Optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:

   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 🚀 Usage

1. **Home Page**: Enter your symptoms separated by commas in the input field.
2. **Submit**: Click the "Submit" button to process the symptoms.
3. **Results**: View the list of potential diseases based on the entered symptoms.

---

## 🧰 Technologies Used

* **Frontend**: HTML, CSS
* **Backend**: Python, Django
* **Machine Learning**: scikit-learn
* **Others**: Pandas, NumPy

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---

## 📄 License

This project is licensed under the MIT License.

---

## ⚠️ Disclaimer

This project is developed solely for educational and demonstration purposes. It is not intended to be used as a substitute for professional medical advice, diagnosis, or treatment. The predictions and information provided by this system should not be considered conclusive or relied upon for making healthcare decisions.

Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read or seen in this project.

The authors and contributors of this project are not responsible for any decisions made based on the outputs of this application.

---
