<p align="center">

<img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/Framework-Flask-black?style=for-the-badge&logo=flask" />
<img src="https://img.shields.io/badge/Machine%20Learning-ScikitLearn-orange?style=for-the-badge&logo=scikitlearn" />
<img src="https://img.shields.io/badge/Deployment-Render-purple?style=for-the-badge&logo=render" />
<img src="https://img.shields.io/github/license/Sampath2910/house-price-prediction?style=for-the-badge" />

</p>

<h1 align="center">House Price Prediction System</h1>
<h3 align="center">Full Stack Regression-Based Property Valuation Platform</h3>

<p align="center">
<a href="https://house-price-prediction-7sk1.onrender.com"><strong>Live Demo</strong></a>
</p>

---

## Overview

A full-stack web application that predicts real estate prices using a trained regression model. The system integrates data preprocessing, model inference, and real-time prediction delivery via a Flask backend.

---

## System Architecture

User → Web Form → Flask Backend → Feature Processing → Trained Regression Model → Predicted Price Output

---

## Machine Learning Details

- Algorithm: Regression Model (Scikit-learn)
- Feature Engineering: Encoding & Scaling
- Output: Estimated Property Price

---

## Tech Stack

Backend: Python, Flask  
Machine Learning: Scikit-learn, Pandas, NumPy  
Frontend: HTML, CSS, JavaScript  
Deployment: Render  

---

## Workflow

1. User inputs property features.
2. Backend processes structured data.
3. Model predicts price.
4. Result displayed in UI.

---

## Run Locally

```bash
git clone https://github.com/Sampath2910/house-price-prediction.git
cd house-price-prediction
pip install -r requirements.txt
flask run
