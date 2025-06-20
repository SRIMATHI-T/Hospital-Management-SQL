import sqlite3
import os
import time

def create_database():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    
    sql_file_path = os.path.join(base_dir, 'database', 'hospital_management.sql')
    db_file_path = os.path.join(base_dir, 'database', 'hospital_management.db')
    
   
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()
    
    
    statements = sql_script.split(';')
    
   
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            if os.path.exists(db_file_path):
                os.remove(db_file_path)
                print(f"Removed existing database at {db_file_path}")
            break
        except PermissionError as e:
            if attempt < max_attempts - 1:
                print(f"Database is in use, retrying in 1 second... (Attempt {attempt+1}/{max_attempts})")
                time.sleep(1)
            else:
                print(f"Warning: Could not remove existing database: {e}")
                print("Continuing with existing database...")
    
    try:
        
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        
       
        for statement in statements:
           
            if statement.strip():
               
                statement = statement.replace('NUMBER', 'INTEGER')
                statement = statement.replace('VARCHAR2', 'TEXT')
                
                
                if 'TO_DATE' in statement:
                   
                    import re
                    date_pattern = r"TO_DATE\('([^']+)', '[^']+'\)"
                    statement = re.sub(date_pattern, r"'\1'", statement)
                
                try:
                    cursor.execute(statement)
                except sqlite3.Error as e:
                    print(f"Error executing statement: {statement}")
                    print(f"Error message: {e}")
        
      
        conn.commit()
        conn.close()
        
        print(f"Database created successfully at {db_file_path}")
        return True
    except sqlite3.Error as e:
        print(f"Failed to create database: {e}")
        return False

if __name__ == "__main__":
    create_database()