# ProjectF1 – Automated F1 2024 Driver Standings Dashboard

**Live Frontend:** [zealous-stone-02173020f.4.azurestaticapps.net](https://zealous-stone-02173020f.4.azurestaticapps.net/)  
**Live Backend API:** [f1-api-verstappen-free.azurewebsites.net](https://f1-api-verstappen-free.azurewebsites.net/)  
**GitHub Repo:** [github.com/ShivaniDM/ProjectF1](https://github.com/ShivaniDM/ProjectF1)

---

## 🧩 Summary

**ProjectF1** is a fully automated, end-to-end data pipeline and web dashboard that scrapes, transforms, stores, and visualizes 2024 Formula 1 driver standings.

Built using Python, PostgreSQL, FastAPI, React (Vite), and Azure, it features a modular architecture with CI/CD automation via GitHub Actions.

---

## ⚙️ Architecture Overview

### 🔁 ETL Pipeline

- **Extract:** Web scraper using `BeautifulSoup` pulls structured data from the official F1 race results page.
    
- **Transform:** Data cleaning and manipulation using `pandas` and `pyarrow`, exported to Parquet for efficient downstream use.
    
- **Load:** PostgreSQL integration using `SQLAlchemy` and `psycopg2`, with dynamic schema generation and secure connection handling.
    

### 🧠 Automation

- GitHub Actions run scheduled workflows **every Monday and Tuesday** to:
    
    - Pull the latest race data
        
    - Process and push to the database
        
    - Ensure the frontend reflects updated standings automatically
        

### ☁️ Cloud Infrastructure

- **PostgreSQL Flexible Server (Azure):** Secure, scalable RDBMS hosting structured F1 standings
    
- **FastAPI Backend (Azure App Service):** REST API serving data to the frontend
    
- **React Vite Frontend (Azure Static Web Apps):** Dynamic and fast UI for users
    

---

## 💡 Features

- Automated web scraping + transformation pipeline
    
- Dynamic PostgreSQL integration
    
- Cloud-hosted, full-stack deployment with Azure
    
- GitHub Actions-powered data refresh cycles
    
- REST API backend using FastAPI
    
- Frontend dashboard using React and Vite
    
- (In Progress) Responsive design for mobile/tablets
    

---

## 🛠️ Tech Stack

|Layer|Technologies|
|---|---|
|Scraping|Python, BeautifulSoup, Requests|
|Transformation|Pandas, PyArrow, Parquet|
|Database|PostgreSQL Flexible Server (Azure), SQLAlchemy|
|Backend API|FastAPI, Uvicorn, Azure App Service|
|Frontend|React (Vite), HTML/CSS/JS, Azure Static Web Apps|
|Automation|GitHub Actions (cron workflows)|

---


---

## 🧪 Live Demo

> View the [live dashboard](https://zealous-stone-02173020f.4.azurestaticapps.net/) to explore up-to-date 2024 F1 driver standings, powered entirely by automated data pipelines and cloud infrastructure.

---

