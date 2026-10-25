from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS
import mysql.connector
import multiprocessing as mp
import Functions as f
import requests
app = Flask(__name__)
CORS(app)


#---------------------------------------------------------------------------------------------------------------------------------------#
# Important Note
# The Users and Drivers are stored in the same table in the database.
# The Users and Address tables are linked using user_id as key which is 
# auto-incremented.
# Hence while inserting a new user/driver, a blank address is also 
# be inserted to maintain the key integrity.
#---------------------------------------------------------------------------------------------------------------------------------------#
# Base Parameters (Stored IN TWO FILES Functions.py and Main.py) Update Both
url= "http://127.0.0.1:8001" # This is Localhost port used 8001
# SQL Database Parameters (Stored IN TWO FILES Functions.py and Main.py) Update Both
SQL_user = "root"
SQL_host = "localhost"
SQL_pass = "Aswdesgtyyn@26" # Please Enter Password Here
SQL_Data = "Ind_Smart" # Name of Database
#---------------------------------------------------------------------------------------------------------------------------------------#
# Flask Code
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(401)
def forbidden(e):
    return render_template('error/401.html'), 403

@app.route("/")
def home():
    return render_template("base/index.html")

@app.route("/about")
def about():
    return render_template("base/about.html")

@app.route("/contact")
def contact():
    return render_template("base/contact.html")

@app.route("/terms")
def terms():
    return render_template("base/terms.html")

#---------------------------------------------------------------------------------------------------------------------------------------#
## Login Pages
@app.route("/login",methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        # Note: Error Codes
        # 0 : No Error
        # 1 : Incorrect Password
        # 2 : Username not found
        # 3 : Database Error
        # 4 : Login or Password empty
        try:
            users = f.fetch_username()
        except:
            return render_template("reg/login.html", error_cde=3)
        
        username = request.form.get('username')
        password = request.form.get('pwd')

        # Check for empty fields
        if not username or not password:
            return render_template("reg/login.html", error_cde=4)
        
        if username not in users:
            return render_template("reg/login.html", error_cde=2)
        elif users[username] != password:
            return render_template("reg/login.html", error_cde=1)
        
        if username == 'Admin' and users[username] == password: 
            resp = make_response("""<script>alert(" Admin Logged in Successfully!");window.location.href = "/admin-dashboard"; </script>""")
            resp.set_cookie('user', username)
            resp.set_cookie('type', 'Admin')
            return resp
        
        if users[username] == password:
            if not f.exists_driver(username):
                resp = make_response("""<script>alert(" Logged in Successfully!");window.location.href = "/user";alert("Logged In Successfully")</script>""")
                resp.set_cookie('user', username)
                resp.set_cookie('type', 'User')
                return resp
            else:
                resp = make_response("""<script>alert(" Driver Logged in Successfully!");window.location.href = "/driver"; </script>""")
                resp.set_cookie('user', username)
                resp.set_cookie('type', 'Driver')
                return resp

    else:
        return render_template("reg/login.html", error_cde=0)

#---------------------------------------------------------------------------------------------------------------------------------------#
# Registration Pages
@app.route("/register/user" ,methods = ['POST','GET'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        type_ = 'User'
        password = request.form.get('pwd')

        details = [name, username, phone, email, type_, password]

        if not f.validate_user_details(details):
            return render_template("reg/register_user.html", alert_cde=1, alert_msg='"Invalid Details! Please check and try again."')
        if request.form.get('czech') != '1':
            return render_template("reg/register_user.html", alert_cde=1, alert_msg='"Please accept the terms and conditions to proceed."')
        
        if not f.insert_user(details):
            return render_template("reg/register_user.html", alert_cde=1, alert_msg='"Error inserting into database. Please try again later."')
        
        return render_template("reg/register_user.html", alert_cde=1, alert_msg='"Registered Successfully!"')
    else:
        return render_template("reg/register_user.html")


@app.route("/register/driver" ,methods = ['POST','GET'])
def register_driver():
    if request.method == 'POST':

        name = request.form.get('name')
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        type_ = 'Driver'
        password = request.form.get('pwd')

        details = [name, username, phone, email, type_, password]
        print("Details to validate:", details) 


        if not f.validate_user_details(details):
            return render_template("reg/register_driver.html", alert_cde=1, alert="'Invalid Details! Please check and try again.'")
        if request.form.get('czech') != 'on':
            return render_template("reg/register_driver.html", alert_cde=1, alert="'Please accept the terms and conditions to proceed.'")
        if not f.insert_user(details):
            return render_template("reg/register_driver.html", alert_cde=1, alert="'Error inserting into database. Please try again later.'")
        
        return render_template("reg/register_driver.html", alert_cde=1, alert="'Registered Successfully!'")
    else:
        return render_template("reg/register_driver.html")


# -----------------------------------------------------------------#
## Admin Dashboard
@app.route("/admin-dashboard")
def admin_dashboard():
    username = request.cookies.get('user')
    if username == 'Admin':
        customers, drivers = f.get_admin_data()
        return render_template(
            "admin/admin_dashboard.html",
            username=username,
            customers=customers,
            drivers=drivers,
            total_customers=len(customers),
            total_drivers=len(drivers)
        )
    else:
        return render_template("error/401.html")

@app.route("/customers-dashboard")
def customer_dashboard():
    username = request.cookies.get('user')
    if username == 'Admin':
        conn = mysql.connector.connect(
            host=SQL_host,
            user=SQL_user,
            password=SQL_pass,
            database=SQL_Data
        )
        cursor = conn.cursor(dictionary=True)
            
        # Get detailed customer data
        cursor.execute("""
                SELECT 
                    u.User_Id as id,
                    u.Name as name,
                    u.Email_Address as email,
                    u.Phone_Number as phone,
                    a.Home_Address as home_address,
                    a.Work_Address as work_address,
                    a.Other_Address as other_address,
                    COUNT(o.Order_Id) as total_rides
                FROM Users u
                LEFT JOIN Addresses a ON u.User_Id = a.User_Id
                LEFT JOIN Order_History o ON u.User_Id = o.User_Id
                WHERE u.Type = 'User'
                GROUP BY u.User_Id
            """)
        customers = cursor.fetchall()
            
        # Get total customers count
        total_customers = len(customers)
            
        # Get active bookings count
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM Order_History o
            JOIN Drivers d ON o.Driver_Id = d.Driver_Id
            WHERE d.Status = 'On Trip'
        """)
        active_bookings = cursor.fetchone()['count']
            
        cursor.close()
        conn.close()
            
        return render_template(
                "admin/customers_dashboard.html",
                customers=customers,
                total_customers=total_customers,
                active_bookings=active_bookings
            )
        
    else:
        return render_template("error/401.html")
    

@app.route("/drivers-dashboard")
def driver_dashboard():
    username = request.cookies.get('user')
    if username == 'Admin':
        conn = mysql.connector.connect(
            host=SQL_host,
            user=SQL_user,
            password=SQL_pass,
            database=SQL_Data
        )
        cursor = conn.cursor(dictionary=True)
            
        # Get detailed driver data
        cursor.execute("""
            SELECT 
                u.User_Id as id,
                MAX(u.Name) as name,
                MAX(u.Email_Address) as email,
                MAX(u.Phone_Number) as phone,
                MAX(d.Vehicle_Number) as license,
                MAX(d.Vehicle_Type) as vehicle_type,
                MAX(d.Status) as status,
                MAX(a.Home_Address) as city
                FROM Users u LEFT JOIN Addresses a ON a.User_Id = u.User_Id LEFT JOIN Drivers   d ON d.User_Id = u.User_Id LEFT JOIN Order_History o ON o.Driver_Id = d.Driver_Id
            WHERE u.Type = 'Driver'
            GROUP BY u.User_Id
        """)
        drivers = cursor.fetchall()
            
        # Get active drivers count (assuming a driver is active if they have rides)
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM Users u
            JOIN Drivers d ON u.User_Id = d.User_Id
            WHERE u.Type = 'Driver'
            AND d.Status IN ('Available', 'On Trip')
        """)
        active_drivers = cursor.fetchone()['count']
            
        cursor.close()
        conn.close()
            
        return render_template(
            "admin/drivers_dashboard.html",
            drivers=drivers,
            total_drivers=len(drivers),
            active_drivers=active_drivers,
            inactive_drivers=len(drivers)-active_drivers
        )
    else:
        return render_template("error/401.html")

#------------------------------------------------#
## User Pages
@app.route("/user")
def user_page():
    username = request.cookies.get('user')
    if f.exists_user(username):
        return render_template("user/user_page.html", username=username)
    else:
        return make_response("""<script>alert(" User does not exist in Database");window.location.href = "/";</script>""")
    
@app.route("/make-booking", methods=['GET', 'POST'])
def make_booking():
    username = request.cookies.get('user')
    if not f.exists_user(username):
        return make_response("""<script>alert(" User does not exist in Database");window.location.href = "/";</script>""")
    
    if request.method == 'POST':
        pickup_lat = request.form.get('pickup_lat')
        pickup_lng = request.form.get('pickup_lng')
        dropoff_lat = request.form.get('dropoff_lat')
        dropoff_lng = request.form.get('dropoff_lng')
        scheduled_time = request.form.get('booking_time')
        pickup_location = f"{pickup_lat},{pickup_lng}"
        dropoff_location = f"{dropoff_lat},{dropoff_lng}"

        distance = round(f.calculate_distance(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng), 3)
        price = round(30*distance)

        con = mysql.connector.connect(
            host=SQL_host,
            user=SQL_user,
            password=SQL_pass,
            database=SQL_Data
        )
        cursor = con.cursor()
        user_id = f.get_userid(username)
        driver_id, driver  = f.assign_driver()
        if not driver_id:
            return render_template("user/make_booking.html", error="No Drivers Available")
        cursor.execute("""
            INSERT INTO Order_History (User_Id, Driver_Id, Start_Location, End_Location, Date, Ongoing)
            VALUES (%s, %s, %s, %s, %s, 'Yes')""", (user_id, driver_id, pickup_location, dropoff_location, scheduled_time))
        con.commit()
        cursor.close()
        con.close()
        
        return render_template("user/make_booking.html",driver_id = driver_id, driver=driver, price=price, distance=distance)
    
    return render_template("user/make_booking.html")

@app.route("/user/addresses" ,methods = ['POST','GET'])
def addresses():
    username = request.cookies.get('user')
    if not f.exists_user(username):
        return make_response("""<script>alert("User does not exist in Database!");window.location.href = "/";</script>""")
    
    if request.method == 'POST':
        home_address = request.form.get('home_address')
        work_address = request.form.get('work_address')
        other_address = request.form.get('other_address')

        if home_address:
            f.update_home_address(username, home_address)
        if work_address:
            f.update_work_address(username, work_address)
        if other_address:
            f.update_other_address(username, other_address)
        
        home_address, work_address, other_address = f.get_addresses(username)
        
        return render_template("user/addresses.html", updated=True, home_address=home_address, work_address=work_address, other_address=other_address)
    home_address, work_address, other_address = f.get_addresses(username)

    if not home_address:
        home_address = "Address Not Set"
    if not work_address:
        work_address = "Address Not Set"
    if not other_address:
        other_address = "Address Not Set"
    
    return render_template("user/addresses.html", home_address=home_address, work_address=work_address, other_address=other_address)
#------------------------------------------------#
## Driver Pages
@app.route("/driver", methods=['GET', 'POST'])
def driver_page():
    username = request.cookies.get('user')
    type_user = request.cookies.get('type')
    
    if request.method == 'GET':
        if (type_user == 'Driver' and f.exists_driver(username)) or username == 'Admin':

            booking = f.get_driver_current_booking(username)
            
            if booking:
                return render_template(
                    "driver/driver_page.html", 
                    username=username,
                    pickup_location=booking['Start_Location'],
                    dropoff_location=booking['End_Location'],
                    status=booking['Status'],
                    user_name=booking['User_Name'],
                    user_phone=booking['User_Phone'],
                    has_booking=True
                )
            else:
                return render_template(
                    "driver/driver_page.html", 
                    username=username,
                    pickup_location="No active booking",
                    dropoff_location="No active booking",
                    status="Available",
                    has_booking=False
                )
        else:
            return make_response("""<script>alert("You Are Not A Driver!");window.location.href = "/";</script>""")
    
    else:  # POST request
        if (type_user == 'Driver' and f.exists_driver(username)) or username == 'Admin':
            action = request.form.get('action')
            
            if action == 'complete_ride':
                if f.complete_ride(username):
                    return make_response("""<script>alert("Ride Completed Successfully!");window.location.href = "/driver";</script>""")
                else:
                    return make_response("""<script>alert("Error completing ride!");window.location.href = "/driver";</script>""")
            
        return make_response("""<script>alert("Unauthorized action!");window.location.href = "/";</script>""")

#---------------------------------------------------------------------------------------------------------------------------------------#
# Main (Execution Starts Here !)

if __name__ == "__main__":

    OpenWebBrowser = mp.Process(target=f.open_wb)
    OpenWebBrowser.start()
    
    app.run(host="0.0.0.0", port=8001, debug=True)
    OpenWebBrowser.join()
    
    
