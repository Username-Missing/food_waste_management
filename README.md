# 🍽 Local Food Wastage Management System

A **Streamlit + SQLite-powered web application** that connects surplus food providers (restaurants, grocery stores, supermarkets) with NGOs and individuals in need.  

The system helps reduce food wastage by efficiently managing donations, claims, and distribution.

---

## 🚀 Features
- **Providers Management**: Add, update, delete, and view food providers.  
- **Receivers Management**: Manage NGOs/individuals as receivers of surplus food.  
- **Food Listings**: Track food donations with details like quantity, expiry, and type.  
- **Claims Management**: Manage requests/claims from receivers for available food.  
- **Analysis Dashboard**:  
  - Providers per city  
  - Top receivers  
  - Claim status distribution  
  - Most donated food types  
  - Monthly claim trends  

---

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Database**: SQLite3  
- **Backend**: Python (CRUD operations + SQL queries)  
- **Visualization**: Pandas + Streamlit tables/charts  

---

## 📂 Project Structure
```bash
food_waste_management/
│── app.py           # Streamlit application
│── crud.py          # CRUD operations for DB
│── queries.py       # SQL queries for analysis
│── food_wastage.db  # SQLite database
│── requirements.txt # Dependencies
│── README.md        # Project documentation
│── notebooks/       # (Optional) Jupyter experiments
```

---

## ⚡ How to Run Locally
1. Clone this repo:
   ```bash
   git clone https://github.com/Username-Missing/food_waste_management.git
   cd food_waste_management
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 📊 Demo Screenshots
(Add screenshots here of your Providers, Receivers, Food Listings, and Analysis dashboards)

---

## 🤝 Contribution
Want to improve this project? Fork it and submit a pull request!  

---

## 📧 Contact
👤 **Prateek Singh**  
📩 [Email](mailto:your_email@example.com) | 🌐 [LinkedIn](https://www.linkedin.com/in/your-linkedin/) | 🐙 [GitHub](https://github.com/Username-Missing)  
