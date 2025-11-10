# 🧮 gvcrud

A web application built with **Django 5.x** using **Generic Views**, designed for managing physical and legal persons (individuals and companies).  
It includes authentication, custom validation, and automatic report generation.

---

## ⚙️ General Features

- Developed with **Django 5.x**, leveraging the power of **Generic Class-Based Views (CBVs)** for CRUD operations.  
- Implements a complete **authentication system** (login, logout, access control).  
- Uses **Django messages** to provide user-friendly feedback.  
- Centralized **custom validation layer** for all data fields.  
- Organized according to Django’s **Model-View-Template (MVT)** architecture.  
- Includes **dynamic reporting** for income and demographic data.  
- Features **customized HTML5 and CSS3 forms**.  
- Fully integrated with Django’s **ORM** for database access and constraints.  

---

## 📊 Report Module

- Implements the **Singleton pattern**, ensuring only one instance exists.  
- Processes data dynamically from the Django ORM.  
- Automatically calculates **maximum, minimum, and average income**.  
- Identifies people **above, below, and at the income average**.  
- Counts the total number of people by **gender**.  
- Computes the **total income sum** across all records.  
- Provides ready-to-use data for **statistical reports**.  

---

## ✅ Validation Module

- Centralizes all **validation rules** across the project.  
- Ensures **data integrity and consistency** throughout.  
- Validates required fields, text lengths, and formats.  
- Performs full validation for **email, CPF, gender, and birth date**.  
- Enforces a **minimum age of 18 years**.  
- Handles **boolean status** and **monetary value validation**.  
- Formats and converts input values (e.g., to `Decimal`).  
- Provides **reusable validation** logic across multiple components.  

---

## 🧾 Forms

- Modular and reusable structure for various application contexts.  
- Built using **Django Forms** and **ModelForms**.  
- Designed with **inheritance and composition** to reduce code duplication.  
- Customized fields with **placeholders, CSS classes, and HTML widgets**.  
- Integrated with the validation module for consistent input checking.  
- Includes forms for **login, search, creation, and editing**.  
- Dynamically adjusts form requirements depending on the context.  
- Delivers a **smooth and validated user experience**.  

---

## 🧍 Data Modeling

- Structured using **model inheritance** for scalability.  
- Represents **generic, natural, and legal persons** separately.  
- Enforces **uniqueness and integrity constraints** at the database level.  
- Ensures that timestamps and relationships remain consistent.  
- Includes validations for **CPF, email, gender, and income range**.  
- Provides **future extensibility** for business entities.  
- Follows **relational modeling best practices** with strong data validation.  

---

## 🧭 View Layer (Application Flow)

- Organizes the full **application workflow** from authentication to reports.  
- Combines **function-based** and **class-based** views for flexibility.  
- Protects sensitive areas using **login requirements**.  
- Displays contextual **messages for success, warnings, and errors**.  
- Supports **dynamic filtering and searching** of records.  
- Handles **create, read, update, and delete (CRUD)** operations.  
- Generates **comprehensive reports** from the data stored.  
- Provides an **intuitive and cohesive user experience**.  

---

## 🧰 Technologies Used

- **Python 3.x**  
- **Django 5.x**  
- **HTML5 / CSS3 (Bootstrap)**  
- **SQLite / PostgreSQL**  
- **Django ORM**  
- **Class-Based Views (CBV)**  
- **Django Messages and Authentication Framework**

---

## 🚀 Project Goal

To deliver a practical and scalable example of a complete **CRUD system** using Django, emphasizing **organization, component reusability, strong validation**, and **automatic reporting**.

---

## 🧑‍💻 Author

Developed for learning and demonstration purposes, showcasing best practices in **modern Django 5.x web development**.

---
