# Personalized Learning Path Recommendation

## Project Overview

A machine-learning-based personalized learning platform that recommends
learning resources based on student profile, interests, engagement,
assessment performance, and learning preferences.

## Technologies

- Python
- Pandas
- Scikit-learn
- Flask
- HTML
- CSS
- JavaScript

## Machine Learning Algorithm

K-Nearest Neighbors (KNN)

## Workflow

Student Input
→ Data Preprocessing
→ Feature Encoding
→ Feature Scaling
→ KNN
→ Similar Resource Recommendation
→ Performance-Level Filtering
→ Personalized Learning Path

## Performance Levels

- Beginner: Performance < 0.60
- Intermediate: Performance 0.60–0.79
- Advanced: Performance >= 0.80

## Project Structure

flask_app/
│
├── app.py
├── preprocessing.py
├── dataset/
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── index.html
    └── result.html