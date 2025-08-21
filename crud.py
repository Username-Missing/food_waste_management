import sqlite3
DB_NAME = "food_wastage.db"

# -------------------------
# Generic Helper -- 
# this is to reduce the generic boilerplate code which is making connection to our DB, commiting changes and closing connection
# -------------------------
def run_query(query, params=(), fetchone=False, fetchall=False):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    result = None
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()
    conn.close()
    return result


# -------------------------
# Providers CRUD
# -------------------------
def add_provider(provider_id, name, type_, address, city, contact):
    run_query("""
        INSERT INTO Providers (Provider_ID, Name, Type, Address, City, Contact)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (provider_id, name, type_, address, city, contact))

def get_provider_by_id(provider_id):
    return run_query("SELECT * FROM Providers WHERE Provider_ID = ?", (provider_id,), fetchone=True)

def get_providers():
    return run_query("SELECT * FROM Providers", fetchall=True)

def update_provider(provider_id, **kwargs):
    updates = ", ".join([f"{col} = ?" for col in kwargs.keys()])
    values = list(kwargs.values())
    values.append(provider_id)
    query = f"UPDATE Providers SET {updates} WHERE Provider_ID = ?"
    run_query(query, tuple(values))

def delete_provider(provider_id):
    run_query("DELETE FROM Providers WHERE Provider_ID = ?", (provider_id,))


# -------------------------
# Receivers CRUD
# -------------------------
def add_receiver(receiver_id, name, type_, city, contact):
    run_query("""
        INSERT INTO Receivers (Receiver_ID, Name, Type, City, Contact)
        VALUES (?, ?, ?, ?, ?)
    """, (receiver_id, name, type_, city, contact))

def get_receiver_by_id(receiver_id):
    return run_query("SELECT * FROM Receivers WHERE Receiver_ID = ?", (receiver_id,), fetchone=True)

def get_receivers():
    return run_query("SELECT * FROM Receivers", fetchall=True)

def update_receiver(receiver_id, **kwargs):
    updates = ", ".join([f"{col} = ?" for col in kwargs.keys()])
    values = list(kwargs.values())
    values.append(receiver_id)
    query = f"UPDATE Receivers SET {updates} WHERE Receiver_ID = ?"
    run_query(query, tuple(values))

def delete_receiver(receiver_id):
    run_query("DELETE FROM Receivers WHERE Receiver_ID = ?", (receiver_id,))


# -------------------------
# Food Listings CRUD
# -------------------------
def add_food(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    run_query("""
        INSERT INTO Food_Listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))

def get_food_by_id(food_id):
    return run_query("SELECT * FROM Food_Listings WHERE Food_ID = ?", (food_id,), fetchone=True)

def get_food_listings():
    return run_query("SELECT * FROM Food_Listings", fetchall=True)

def update_food(food_id, **kwargs):
    updates = ", ".join([f"{col} = ?" for col in kwargs.keys()])
    values = list(kwargs.values())
    values.append(food_id)
    query = f"UPDATE Food_Listings SET {updates} WHERE Food_ID = ?"
    run_query(query, tuple(values))

def delete_food(food_id):
    run_query("DELETE FROM Food_Listings WHERE Food_ID = ?", (food_id,))


# -------------------------
# Claims CRUD
# -------------------------
def add_claim(claim_id, food_id, receiver_id, status, timestamp):
    run_query("""
        INSERT INTO Claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (claim_id, food_id, receiver_id, status, timestamp))

def get_claim_by_id(claim_id):
    return run_query("SELECT * FROM Claims WHERE Claim_ID = ?", (claim_id,), fetchone=True)

def get_claims():
    return run_query("SELECT * FROM Claims", fetchall=True)

def update_claim(claim_id, **kwargs):
    updates = ", ".join([f"{col} = ?" for col in kwargs.keys()])
    values = list(kwargs.values())
    values.append(claim_id)
    query = f"UPDATE Claims SET {updates} WHERE Claim_ID = ?"
    run_query(query, tuple(values))

def delete_claim(claim_id):
    run_query("DELETE FROM Claims WHERE Claim_ID = ?", (claim_id,))