import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )
    print("SUCCESS")
except Exception as e:
    print("ERROR:", e)