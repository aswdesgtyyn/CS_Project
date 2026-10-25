import os
import sys


print('This Script will attempt to Download the Modules listed below')
print("""
      
    1. mysql.connector
    2. Flask

Press Enter to Containue with the Installation
""")

try:
    os.system("pip install Flask")
    os.system("pip install mysql-connector-python")
    os.system("pip install flask-cors")
except:
    print("E1")
    try:
        os.system("python -m pip install Flask")
        os.system("python -m pip install mysql-connector-python")
        os.system("python -m pip install flask-cors")
    except:
        print("E2")
        try:
            os.system("python -m pip install Flask")
            os.system("python -m pip install mysql-connector-python")
            os.system("python -m pip install flask-cors")
        except:
            print("Pip or Python does not seem to be installed on your system !")
            sys.exit(-1)

print("Modules should be installed!")