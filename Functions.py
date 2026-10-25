import mysql.connector
from time import sleep
import webbrowser as wb
from math import radians, sin, cos, sqrt, atan2

#-----------------------------------------------------------------#
# Base Parameters (Stored IN TWO FILES Functions.py and Main.py) Update Both
url= "http://127.0.0.1:8001" # This is Localhost port used 8001
# SQL Database Parameters (Stored IN TWO FILES Functions.py and Main.py) Update Both
SQL_user = "root"
SQL_host = "localhost"
SQL_pass = "Aswdesgtyyn@26" # Please Enter Password Here
SQL_Data = "Ind_Smart" # Name of Database
#-----------------------------------------------------------------#
#Miscellaneous Functions

def open_wb():
    sleep(2)
    wb.open(url, new =0)

#-----------------------------------------------------------------#
# Functions for the Registration of Users

def validate_user_details(details):
    #details: [name, username, phone, email, type_, password]
    name, username, phone, email, type_, password = details 
    
    # Name: not null(none in python), only letters and spaces
    if name is None:
        return False 
    elif not all(char.isalpha() or char == " " for char in name):
            return False
    
    if username is None:
        return False
    
    # Phone: not null(none in python), 10 digits
    if phone is None:
        return False
    elif len(phone)!=10:
        return False
    
    # Email: not null(none in python), should contain @,. etc
    if email is None:
        return False
    for char in email:
        if not (char.isalnum() or char in ['@', '.','_']):
            return False

    # Type: not null(none in python), Driver or User(case sensitive)
    if type_ is None:
        return False
    elif type_ not in ['User','Driver']:
        return False
        
    # Password: not null(none in python), at least 6 chars, contains number and letter
    if password is None:
        return False
    elif len(password)<6:
        return False
    
    return True



def insert_user(details):
#details: [name, Username, phone, email, type_, password]
#Inserts user into the database
    
    try:
        conn = mysql.connector.connect(
            host=SQL_host,
            user=SQL_user,
            password=SQL_pass,
            database=SQL_Data
        )

        cursor = conn.cursor()
        sql = "INSERT INTO Users (Name, Username, Phone_Number, Email_Address, Type, Password) VALUES (%s, %s, %s, %s, %s,%s)"
        cursor.execute(sql, details)
        user_id = cursor.lastrowid

        # Insert blank address for the new user
        addr_sql = "INSERT INTO Addresses (User_Id, Home_Address, Work_Address, Other_Address) VALUES (%s, NULL, NULL, NULL)"
        cursor.execute(addr_sql, (user_id,))
        
        # If user is a driver, insert blank in Drivers table
        if details[4] == 'Driver':  # details[4] is Type
            driver_sql = "INSERT INTO Drivers (User_Id, Vehicle_Number, Vehicle_Type, Status) VALUES (%s, NULL, NULL, 'Available')"
            cursor.execute(driver_sql, (user_id,)) 
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print("MySQL Database Error: ", e)
        return False


#-----------------------------------------------------------------#
# Function to fetch Admin Data: Customers and Drivers

def get_admin_data():
    try:
        conn = mysql.connector.connect(
            host=SQL_host,
            user=SQL_user,
            password=SQL_pass,
            database=SQL_Data
        )
        cursor = conn.cursor(dictionary=True) 
        
        # Customers
        cursor.execute("""
            SELECT 
                u.User_Id as id, 
                u.Name as name, 
                u.Email_Address as email,
                u.Phone_Number as phone,
                a.Home_Address as city,
                COUNT(o.Order_Id) as total_rides
            FROM Users u
            LEFT JOIN Addresses a ON u.User_Id = a.User_Id
            LEFT JOIN Order_History o ON u.User_Id = o.User_Id
            WHERE u.Type='User'
            GROUP BY u.User_Id
        """)
        customers = cursor.fetchall()
        
        # Drivers
        cursor.execute("""
            SELECT 
                u.User_Id as id,
                u.Name as name,
                u.Email_Address as email,
                u.Phone_Number as phone,
                d.Vehicle_Number as license,
                d.Vehicle_Type as vehicle_type,
                d.Status as status,
                a.Home_Address as city,
                COUNT(o.Order_Id) as total_rides
            FROM Users u
            LEFT JOIN Addresses a ON u.User_Id = a.User_Id
            LEFT JOIN Drivers d ON u.User_Id = d.User_Id
            LEFT JOIN Order_History o ON d.Driver_Id = o.Driver_Id
            WHERE u.Type='Driver'
            GROUP BY u.User_Id, d.Driver_Id
        """)
        drivers = cursor.fetchall()

        cursor.close()
        conn.close()
        return customers, drivers
    except Exception as e:
        print("Error fetching admin data:", e)
        return [], []
#-----------------------------------------------------------------#
# Function to fetch Username and Password from Database
def fetch_username():
    conn = mysql.connector.connect(
        host=SQL_host,
        user=SQL_user,
        password=SQL_pass,
        database=SQL_Data
        )
    cursor = conn.cursor()
    cursor.execute("SELECT Username, Password FROM Users;")
    data = cursor.fetchall()
    users = {username: password for username, password in data}
    cursor.close()
    conn.close()
    return users

#-----------------------------------------------------------------#
# Functions to check existence of User and Driver in Database

def exists_user(username):
    try:
        con= mysql.connector.connect(
            host="localhost",
            user="root",
            password= SQL_pass,
            database="Ind_Smart")
        cur=con.cursor()
        sql="Select Username from users"
        cur.execute(sql)
        data=cur.fetchall()
        for i in data:
            if i[0]==username:
                con.close()
                return True
        con.close()
        return False
    except:
        return -1

def exists_driver(Username):
    try:
        con=mysql.connector.connect(
            host='localhost',
            user='root',
            password=SQL_pass,
            database='Ind_Smart')
        cur=con.cursor()
        sql="Select users.username from drivers LEFT JOIN users ON drivers.user_id=users.user_id"
        cur.execute(sql)
        data=cur.fetchall()
        for i in data:
            if i[0]==Username:
                con.close()
                return True
        con.close()
        return False
    except:
        return -1
    
#-----------------------------------------------------------------#
# Booking Page Functions
def assign_driver():
    con=mysql.connector.connect(
            host='localhost',
            user='root',
            password=SQL_pass,
            database='Ind_Smart')
    cur=con.cursor()
    sql="""SELECT 
    d.Driver_Id, 
    u.Name
FROM 
    Drivers AS d
LEFT JOIN 
    Users AS u 
    ON d.User_Id = u.User_Id
WHERE 
    d.Status = 'Available'
LIMIT 1;
"""
    cur.execute(sql)
    data=cur.fetchall()
    if len(data)==0:
        return None, None
    driver_id=data[0][0]
    driver =data[0][1]
    sql="Update drivers set status='On Trip' where Driver_Id=%s"
    cur.execute(sql,(driver_id,))
    con.commit()
    con.close()
    return driver_id, driver

def get_userid(username):
    con=mysql.connector.connect(
            host='localhost',
            user='root',
            password=SQL_pass,
            database='Ind_Smart')
    cur=con.cursor()
    cur.execute("Select User_Id from users where username=%s",(username,))
    data=cur.fetchall()
    con.close()
    return data[0][0]


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c
    
    return distance

#-----------------------------------------------------------------#
# Driver Booking Related Functions

def get_driver_current_booking(username):
    try:
        con=mysql.connector.connect(
            host='localhost',
            user='root',
            password=SQL_pass,
            database='Ind_Smart')
        cursor = con.cursor(dictionary=True)
        query = """
            SELECT 
                oh.Order_Id,
                oh.Start_Location,
                oh.End_Location,
                oh.Date,
                d.Status,
                u.Name as User_Name,
                u.Phone_Number as User_Phone
            FROM Order_History oh
            JOIN Drivers d ON oh.Driver_Id = d.Driver_Id
            JOIN Users du ON d.User_Id = du.User_Id
            JOIN Users u ON oh.User_Id = u.User_Id
            WHERE du.Username = %s 
            AND oh.Ongoing = 'Yes'
            ORDER BY oh.Date DESC, oh.Order_Id DESC
            LIMIT 1
        """
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        con.close()
        return result
    except Exception as e:
        print(f"Error fetching driver booking: {e}")
        con.close()
        return None

def complete_ride(username):
    try:
        con=mysql.connector.connect(
            host='localhost',
            user='root',
            password=SQL_pass,
            database='Ind_Smart')
        cursor = con.cursor()
        update_order = """
            UPDATE Order_History oh
            JOIN Drivers d ON oh.Driver_Id = d.Driver_Id
            JOIN Users u ON d.User_Id = u.User_Id
            SET oh.Ongoing = 'No'
            WHERE u.Username = %s AND oh.Ongoing = 'Yes'
        """
        cursor.execute(update_order, (username,))

        update_driver = """
            UPDATE Drivers d
            JOIN Users u ON d.User_Id = u.User_Id
            SET d.Status = 'Available'
            WHERE u.Username = %s
        """
        cursor.execute(update_driver, (username,))
        
        con.commit()
        cursor.close()
        con.close()
        return True
    except Exception as e:
        print(f"Error completing ride: {e}")
        con.rollback()
        con.close()
        return False

#-----------------------------------------------------------------#
# Address Related Functions

def get_addresses(username):
    con = mysql.connector.connect(
        host=SQL_host,
        user=SQL_user,
        password=SQL_pass,
        database=SQL_Data
    )
    cursor = con.cursor()

    query = """
        SELECT a.Home_Address, a.Work_Address, a.Other_Address
        FROM Users u
        JOIN Addresses a ON u.User_Id = a.User_Id
        WHERE u.Username = %s
    """
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    cursor.close()
    con.close()

    if result:
        return result[0], result[1], result[2]
    else:
        return None, None, None

def update_home_address(username, new_home):
    con = mysql.connector.connect(
        host=SQL_host,
        user=SQL_user,
        password=SQL_pass,
        database=SQL_Data
    )
    cursor = con.cursor()

    query = """
        UPDATE Addresses a
        JOIN Users u ON a.User_Id = u.User_Id
        SET a.Home_Address = %s
        WHERE u.Username = %s
    """
    cursor.execute(query, (new_home, username))
    con.commit()

    updated = cursor.rowcount > 0

    cursor.close()
    con.close()
    return updated

def update_work_address(username, new_work):
    con = mysql.connector.connect(
        host=SQL_host,
        user=SQL_user,
        password=SQL_pass,
        database=SQL_Data
    )
    cursor = con.cursor()

    query = """
        UPDATE Addresses a
        JOIN Users u ON a.User_Id = u.User_Id
        SET a.Work_Address = %s
        WHERE u.Username = %s
    """
    cursor.execute(query, (new_work, username))
    con.commit()

    updated = cursor.rowcount > 0

    cursor.close()
    con.close()
    return updated

def update_other_address(username, new_other):
    con = mysql.connector.connect(
        host=SQL_host,
        user=SQL_user,
        password=SQL_pass,
        database=SQL_Data
    )
    cursor = con.cursor()

    query = """
        UPDATE Addresses a
        JOIN Users u ON a.User_Id = u.User_Id
        SET a.Other_Address = %s
        WHERE u.Username = %s
    """
    cursor.execute(query, (new_other, username))
    con.commit()

    updated = cursor.rowcount > 0

    cursor.close()
    con.close()
    return updated