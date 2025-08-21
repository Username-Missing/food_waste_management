import sqlite3
import pandas as pd

DB_NAME = "food_wastage.db"

# -------------------------
# Helper Function
# -------------------------
def run_sql(query, params=()):
    """Run SQL query and return result as pandas DataFrame"""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


# -------------------------
# Providers & Receivers
# -------------------------
def providers_per_city():
    return run_sql("SELECT City, COUNT(*) AS Provider_Count FROM Providers GROUP BY City;")

def receivers_per_city():
    return run_sql("SELECT City, COUNT(*) AS Receiver_Count FROM Receivers GROUP BY City;")

def top_provider_types():
    return run_sql("""
        SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
        FROM Food_Listings
        GROUP BY Provider_Type
        ORDER BY Total_Quantity DESC;
    """)

def provider_contacts_by_city(city):
    return run_sql("SELECT Name, Contact FROM Providers WHERE City = ?", (city,))

def top_receivers(limit=10):
    return run_sql("""
        SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims
        FROM Claims c
        JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Name
        ORDER BY Total_Claims DESC
        LIMIT ?;
    """, (limit,))


# -------------------------
# Food Listings & Availability
# -------------------------
def total_food_available():
    return run_sql("SELECT SUM(Quantity) AS Total_Food_Available FROM Food_Listings;")

def city_with_most_listings():
    return run_sql("""
        SELECT Location, COUNT(*) AS Total_Listings
        FROM Food_Listings
        GROUP BY Location
        ORDER BY Total_Listings DESC
        LIMIT 1;
    """)

def common_food_types():
    return run_sql("""
        SELECT Food_Type, COUNT(*) AS Count_Type
        FROM Food_Listings
        GROUP BY Food_Type
        ORDER BY Count_Type DESC;
    """)


# -------------------------
# Claims & Distribution
# -------------------------
def claims_per_food(limit=10):
    return run_sql("""
        SELECT f.Food_Name, COUNT(c.Claim_ID) AS Claim_Count
        FROM Claims c
        JOIN Food_Listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Food_Name
        ORDER BY Claim_Count DESC
        LIMIT ?;
    """, (limit,))

def top_successful_provider():
    return run_sql("""
        SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
        FROM Claims c
        JOIN Food_Listings f ON c.Food_ID = f.Food_ID
        JOIN Providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Name
        ORDER BY Successful_Claims DESC
        LIMIT 1;
    """)

def claim_status_percentage():
    return run_sql("""
        SELECT Status,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Claims), 2) AS Percentage
        FROM Claims
        GROUP BY Status;
    """)


# -------------------------
# Analysis & Insights
# -------------------------
def avg_quantity_per_receiver(limit=10):
    return run_sql("""
        SELECT r.Name, ROUND(AVG(f.Quantity),2) AS Avg_Quantity_Claimed
        FROM Claims c
        JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN Food_Listings f ON c.Food_ID = f.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY r.Name
        ORDER BY Avg_Quantity_Claimed DESC
        LIMIT ?;
    """, (limit,))

def most_claimed_meal_type():
    return run_sql("""
        SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims
        FROM Claims c
        JOIN Food_Listings f ON c.Food_ID = f.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY f.Meal_Type
        ORDER BY Total_Claims DESC;
    """)

def total_donated_per_provider(limit=10):
    return run_sql("""
        SELECT p.Name, SUM(f.Quantity) AS Total_Donated
        FROM Providers p
        JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Name
        ORDER BY Total_Donated DESC
        LIMIT ?;
    """, (limit,))

def top_donated_foods(limit=5):
    return run_sql("""
        SELECT Food_Name, COUNT(*) AS Donation_Count
        FROM Food_Listings
        GROUP BY Food_Name
        ORDER BY Donation_Count DESC
        LIMIT ?;
    """, (limit,))

def monthly_claim_trend():
    return run_sql("""
        SELECT strftime('%Y-%m', Timestamp) AS Month, COUNT(*) AS Total_Claims
        FROM Claims
        WHERE Status = 'Completed'
        GROUP BY Month
        ORDER BY Month;
    """)