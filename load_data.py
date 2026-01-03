import pandas as pd
import pyodbc
from datetime import date
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Database Connection Function
# --------------------------------------------------
def get_connection():
    """
    Establish a trusted connection to SQL Server
    using Windows Authentication.
    """
    return pyodbc.connect(
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        "Trusted_Connection=yes;"
    )


# --------------------------------------------------
# Load CSV Data into Specified Table
# --------------------------------------------------
def load_csv(csv_path, insert_sql, table_name):
    df = pd.read_csv(csv_path)
    conn = get_connection()
    cursor = conn.cursor()

    try:
        for _, row in df.iterrows():
            cursor.execute(insert_sql, tuple(row))
        conn.commit()
        print(f"✓ Loaded {len(df)} rows into {table_name}")

    except Exception as e:
        conn.rollback()
        print(f"✗ Error loading {table_name}: {e}")

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# Insert Static Data (Certifications & Harvest Logs)
# --------------------------------------------------
def insert_static_data():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # -------- Certifications --------
        certifications = [
            (1, 'Organic Certified', 'SA Organic', '2024-01-01'),
            (2, 'Fair Trade', 'Fairtrade Africa', '2023-06-15'),
            (3, 'GlobalG.A.P', 'GLOBALG.A.P', '2024-03-10')
        ]

        cursor.executemany("""
            INSERT INTO Certifications (supplier_id, certification_name, issued_by, issue_date)
            VALUES (?, ?, ?, ?)
        """, certifications)

        # -------- Harvest Log --------
        harvests = [
            (1, '2025-10-05', 'Apples', 1200),
            (2, '2025-10-12', 'Grapes', 950),
            (3, '2025-11-01', 'Olives', 700),
            (1, '2025-11-18', 'Apples', 1300),
            (2, '2025-12-03', 'Grapes', 1100)
        ]

        cursor.executemany("""
            INSERT INTO Harvest_Log (supplier_id, harvest_date, crop_type, quantity_kg)
            VALUES (?, ?, ?, ?)
        """, harvests)

        conn.commit()
        print("✓ Certifications and Harvest_Log populated")

    except Exception as e:
        conn.rollback()
        print(f"✗ Error inserting static data: {e}")

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# Insert Additional Q4 Orders
# --------------------------------------------------
def insert_additional_orders():
    """
    Insert extra Q4 2025 orders to ensure
    at least 10 total orders exist for the quarter.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        additional_orders = [
            (9001, 1, '2025-10-08', 500, 18.50),
            (9002, 2, '2025-10-21', 620, 17.20),
            (9003, 3, '2025-11-04', 450, 19.00),
            (9004, 1, '2025-11-19', 700, 18.00),
            (9005, 2, '2025-12-02', 800, 17.80)
        ]

        cursor.executemany("""
            INSERT INTO Orders (order_id, supplier_id, order_date, quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
        """, additional_orders)

        conn.commit()
        print("✓ Additional Q4 2025 orders inserted")

    except Exception as e:
        conn.rollback()
        print(f"✗ Error inserting additional orders: {e}")

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# Insert Required Regional Sales Targets
# --------------------------------------------------
def insert_q4_sales_targets():
    """
    Insert Q4 2025 sales targets for required regions.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        targets = [
            ('Western Cape', 'Q4-2025', 250000.00),
            ('Eastern Cape', 'Q4-2025', 180000.00),
            ('Northern Cape', 'Q4-2025', 120000.00)
        ]

        cursor.executemany("""
            INSERT INTO Sales_Targets (region, quarter, target_amount)
            VALUES (?, ?, ?)
        """, targets)

        conn.commit()
        print("✓ Q4 2025 sales targets inserted")

    except Exception as e:
        conn.rollback()
        print(f"✗ Error inserting sales targets: {e}")

    finally:
        cursor.close()
        conn.close()

# --------------------------------------------------
# Main Execution
# --------------------------------------------------
if __name__ == "__main__":

    load_csv(
        "suppliers.csv",
        """
        INSERT INTO Suppliers (supplier_id, farm_name, region)
        VALUES (?, ?, ?)
        """,
        "Suppliers"
    )

    load_csv(
        "orders.csv",
        """
        INSERT INTO Orders (order_id, supplier_id, order_date, quantity, unit_price)
        VALUES (?, ?, ?, ?, ?)
        """,
        "Orders"
    )

    load_csv(
        "targets.csv",
        """
        INSERT INTO Sales_Targets (region, quarter, target_amount)
        VALUES (?, ?, ?)
        """,
        "Sales_Targets"
    )

    insert_static_data()
    insert_additional_orders()
    insert_q4_sales_targets()

    print("\nAll tables populated,and additional data inserted.")
