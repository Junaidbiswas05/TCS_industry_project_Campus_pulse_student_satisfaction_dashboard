# 📊 Campus Pulse – Student Satisfaction Dashboard  

**Industry Project | TCS**  
**Submitted by:** Junaid Biswas  
**Academic Year:** 2024–2025  

---

## 🧩 Project Overview  

Campus Pulse is a data-driven web dashboard designed to analyze and visualize student satisfaction across various campus facilities such as Library, Hostel, Cafeteria, and Sports Centre.  
The system converts raw feedback into meaningful insights using charts, filters, and analytics to support data-driven decision making.

---

## 🎯 Project Objectives  

- Analyze student satisfaction data  
- Visualize campus facility performance  
- Identify improvement areas  
- Support institutional decision making  
- Build an industry-standard dashboard  

---

## 🛠️ Technology Stack  

### Backend  
- Python 3.11  
- Flask  
- Pandas  
- NumPy  

### Frontend  
- HTML5  
- CSS3  
- Bootstrap 5  
- JavaScript  
- Chart.js  

---

## 📁 Project Structure  

CampusPulse  
├── app.py  
├── requirements.txt  
├── data  
│   └── feedback.csv  
├── templates  
│   └── index.html  
├── static  
│   ├── css  
│   │   └── style.css  
│   └── js  
│       └── dashboard.js  
└── README.md  

---

## 🔄 System Workflow  

1. Student feedback data is loaded from CSV  
2. Data is cleaned and processed using Pandas  
3. Satisfaction metrics and trends are calculated  
4. Flask APIs provide processed data  
5. Chart.js displays interactive charts  
6. Users filter and view insights  

---

## 📊 Dashboard Features  

- Overall satisfaction score  
- Facility-wise performance  
- Year-wise trends  
- Score distribution  
- Real-time filtering  
- Data export (CSV / JSON)  

---

## 📈 Visual Components  

- Bar Chart – Facility performance  
- Line Chart – Year-wise satisfaction trend  
- Pie Chart – Score distribution  
- Heatmap – Facility vs Year comparison  

---

## 📂 Dataset Schema  

student_id – Unique student ID  
academic_year – Year of study  
major – Student department  
facility_rated – Facility name  
satisfaction_score – Rating (1–5)  
timestamp – Feedback time  

---

## 🔗 API Endpoints  

/api/overall-metrics  
/api/facility-metrics  
/api/filtered-data  
/api/export  

---

## ▶️ How to Run the Project  

1. Install required libraries  
```bash
pip install -r requirements.txt
