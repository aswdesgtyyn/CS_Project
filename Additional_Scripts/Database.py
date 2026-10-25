import sys
import mysql.connector

print('This Script will Attempt to Create the Tables and/or Database for Indigo Smart')
print('User is Assumed to be root')

print('\r\n\r\n')

pas = input('Please Enter Your MySQL Password : ')
stuff = {
    "user": "root",
    "password": pas,
    "host": "localhost",
}

stuff_database = {
    "user": "root",
    "password": pas,
    "host": "localhost",
    "database": "Ind_Smart"
}

try:
    con = mysql.connector.connect(**stuff)
except:
    print("MySQL Conncetion Error")
    print("Check Userid or Password !")
    sys.exit(-1)

cursor = con.cursor()
cursor.execute("DROP DATABASE IF EXISTS `Ind_Smart`;")
cursor.execute("CREATE DATABASE IF NOT EXISTS `Ind_Smart`;")
cursor.close()
con.close()


con = mysql.connector.connect(**stuff_database)
cursor = con.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE users (
User_Id INT PRIMARY KEY AUTO_INCREMENT,
Name TEXT NOT NULL,
Username TEXT NOT NULL,
Phone_Number VARCHAR(20) NOT NULL,
Email_Address TEXT NOT NULL,
Type ENUM('User','Driver') NOT NULL,
Password TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE Addresses (
       User_Id INT PRIMARY KEY,
       Home_Address TEXT,
       Work_Address TEXT,
       Other_Address TEXT,
    FOREIGN KEY (User_Id) REFERENCES Users(User_Id)
);
""")

cursor.execute("""
CREATE TABLE Drivers (
    Driver_Id INT AUTO_INCREMENT PRIMARY KEY,
    User_Id INT NOT NULL,
    Vehicle_Number VARCHAR(20),
    Vehicle_Type VARCHAR(50),
    Status ENUM('On Trip', 'Available') NOT NULL DEFAULT 'Available',
    FOREIGN KEY (User_Id) REFERENCES Users(User_Id)
);
""")

cursor.execute("""
CREATE TABLE Order_History (
    Order_Id INT AUTO_INCREMENT PRIMARY KEY,
    User_Id INT NOT NULL,
    Driver_Id INT NOT NULL,
    Date DATE NOT NULL,
    Start_Location VARCHAR(255) NOT NULL,
    End_Location VARCHAR(255) NOT NULL,
    Ongoing ENUM('Yes', 'No') NOT NULL DEFAULT 'No',
    FOREIGN KEY (User_Id) REFERENCES Users(User_Id),
    FOREIGN KEY (Driver_Id) REFERENCES Drivers(Driver_Id)
);""")

# Insert Values
cursor.execute("""
INSERT INTO users (Name, Username, Phone_Number, Email_Address, Type, Password) VALUES 
('Admin', 'Admin', '0000000000', 'maester@citadel.com', 'User', 'pass123'),
('Jon Snow', 'kingNorth', '9876543210', 'jon.snow@winterfell.com', 'User', 'ghost123'),
('Daenerys Targaryen', 'mother_dragons', '9876543211', 'dany@dragonstone.com', 'Driver', 'dragons3'),
('Gandalf Grey', 'mithrandir', '9876543212', 'gandalf@istari.com', 'Driver', 'youshall!'),
('Frodo Baggins', 'ring_bearer', '9876543213', 'frodo@shire.com', 'User', 'precious1'),
('Harry Potter', 'chosen_one', '9876543214', 'harry@hogwarts.edu', 'User', 'expecto1'),
('Hermione Granger', 'brightest', '9876543215', 'hermione@hogwarts.edu', 'Driver', 'leviosa!'),
('Tyrion Lannister', 'half_man', '9876543216', 'tyrion@casterly.com', 'User', 'wine123'),
('Aragorn', 'strider', '9876543217', 'aragorn@gondor.com', 'Driver', 'ranger1'),
('Arya Stark', 'no_one', '9876543218', 'arya@winterfell.com', 'User', 'needle!'),
('Dumbledore', 'elder_wand', '9876543219', 'albus@hogwarts.edu', 'Driver', 'phoenix1'),
('Legolas', 'elf_eyes', '9876543220', 'legolas@mirkwood.com', 'Driver', 'bowman1'),
('Sansa Stark', 'lady_winter', '9876543221', 'sansa@winterfell.com', 'User', 'lemoncake'),
('Samwise Gamgee', 'loyal_sam', '9876543222', 'sam@shire.com', 'User', 'potatoes'),
('Ron Weasley', 'keeper', '9876543223', 'ron@hogwarts.edu', 'Driver', 'scabbers'),
('Cersei Lannister', 'queen_lion', '9876543224', 'cersei@landing.com', 'User', 'power123'),
('Gimli', 'axe_bearer', '9876543225', 'gimli@erebor.com', 'Driver', 'andmyaxe'),
('Luna Lovegood', 'ravenclaw', '9876543226', 'luna@hogwarts.edu', 'User', 'nargles1'),
('Thorin Oakenshield', 'king_under', '9876543227', 'thorin@erebor.com', 'Driver', 'arkenstone'),
('Draco Malfoy', 'slytherin', '9876543228', 'draco@hogwarts.edu', 'User', 'pureblood'),
('Eddard Stark', 'ned_honor', '9876543229', 'ned@winterfell.com', 'Driver', 'honor123'),
('Bilbo Baggins', 'burglar', '9876543230', 'bilbo@shire.com', 'User', 'adventure'),
('Severus Snape', 'half_prince', '9876543231', 'snape@hogwarts.edu', 'Driver', 'lily4ever'),
('Tywin Lannister', 'old_lion', '9876543232', 'tywin@casterly.com', 'User', 'legacy1'),
('Galadriel', 'lady_light', '9876543233', 'galadriel@lorien.com', 'Driver', 'nenya123'),
('Sirius Black', 'padfoot', '9876543234', 'sirius@grimmauld.com', 'User', 'marauder'),
('Boromir', 'son_steward', '9876543235', 'boromir@gondor.com', 'Driver', 'horn123'),
('Bellatrix Lestrange', 'bella_dark', '9876543236', 'bella@azkaban.com', 'User', 'crucio!'),
('Elrond', 'half_elven', '9876543237', 'elrond@rivendell.com', 'Driver', 'vilya123'),
('Dobby', 'free_elf', '9876543238', 'dobby@hogwarts.edu', 'User', 'socks123');
""")

cursor.execute("""
INSERT INTO Addresses (User_Id, Home_Address, Work_Address, Other_Address) VALUES 
(1, 'The Citadel, Oldtown', 'Grand Maester Chamber, Red Keep', 'Isle of Ravens'),
(2, 'Winterfell Castle, North', 'Castle Black, The Wall', 'Beyond the Wall'),
(3, 'Dragonstone Castle', 'Great Pyramid, Meereen', 'Dothraki Sea'),
(4, 'Istari Tower, Valinor', 'Orthanc, Isengard', 'Mines of Moria'),
(5, 'Bag End, Hobbiton', 'Green Dragon Inn, Bywater', 'Rivendell Valley'),
(6, '4 Privet Drive, Surrey', 'Gryffindor Tower, Hogwarts', 'The Burrow'),
(7, 'Granger Residence, London', 'Ministry of Magic', 'Hogwarts Library'),
(8, 'Casterly Rock', 'Small Council Chamber, Red Keep', 'The Inn at the Crossroads'),
(9, 'Ranger Post, Eriador', 'Throne Room, Minas Tirith', 'Paths of the Dead'),
(10, 'House of Black and White, Braavos', 'Great Hall, Winterfell', 'Frey Towers'),
(11, 'Headmaster Tower, Hogwarts', 'Ministry of Magic', 'Hogs Head Inn, Hogsmeade'),
(12, 'Woodland Realm, Mirkwood', 'Helm Deep, Rohan', 'Lonely Mountain'),
(13, 'Winterfell, North', 'Red Keep, Kings Landing', 'Eyrie, Vale'),
(14, 'Gamgee Home, Hobbiton', 'Gardens of Gondor', 'Mount Doom Base Camp'),
(15, 'The Burrow, Ottery St Catchpole', 'Gryffindor Tower', 'Three Broomsticks'),
(16, 'Red Keep, Kings Landing', 'Great Sept of Baelor', 'Tower of the Hand'),
(17, 'Glittering Caves, Rohan', 'Mines of Moria', 'Erebor Halls'),
(18, 'Lovegood House, Ottery St Catchpole', 'Ravenclaw Tower', 'Room of Requirement'),
(19, 'Erebor, Lonely Mountain', 'Treasury Halls', 'Dale Markets'),
(20, 'Malfoy Manor, Wiltshire', 'Slytherin Dungeon', 'Borgin and Burkes'),
(21, 'Tower of the Hand, Red Keep', 'Godswood, Winterfell', 'Great Sept of Baelor'),
(22, 'Bag End, Hobbiton', 'Rivendell Library', 'Erebor Guest Chambers'),
(23, 'Spinners End, Cokeworth', 'Potions Classroom, Hogwarts', 'Shrieking Shack'),
(24, 'Casterly Rock', 'Small Council Chamber', 'Golden Tooth'),
(25, 'Caras Galadhon, Lothlórien', 'Mirror Grove', 'Shores of Valinor'),
(26, '12 Grimmauld Place, London', 'Defense Class, Hogwarts', 'Azkaban Prison'),
(27, 'Captains Quarters, Minas Tirith', 'White Tree Courtyard', 'Osgiliath Ruins'),
(28, 'Lestrange Manor', 'Gringotts Vault', 'Malfoy Manor'),
(29, 'Rivendell Valley', 'White Council Chamber', 'Grey Havens'),
(30, 'Hogwarts Kitchen', 'Room of Requirement', 'Gryffindor Common Room');
""")


cursor.execute("""
INSERT INTO Drivers (User_Id, Vehicle_Number, Vehicle_Type, Status) VALUES 
(3,  'DL-01-HK-1111', 'Sedan', 'Available'),
(4,  'MH-02-JS-2222', 'SUV', 'Available'),
(7,  'KA-03-MG-3333', 'Hatchback', 'Available'),
(8,  'TN-04-RT-4444', 'Sedan', 'Available'),
(9,  'AP-05-XL-1234', 'SUV', 'Available'),
(11, 'GJ-05-PQ-5555', 'SUV', 'Available'),
(12, 'RJ-06-YU-6666', 'Sedan', 'Available'),
(15, 'WB-07-TY-7777', 'Hatchback', 'Available'),
(16, 'HR-08-QW-8888', 'Sedan', 'Available'),
(17, 'AS-09-ER-4321', 'SUV', 'Available'),
(19, 'PB-09-ER-9999', 'SUV', 'Available'),
(20, 'CH-10-DF-1010', 'Sedan', 'Available'),
(21, 'UP-10-ZX-1122', 'Hatchback', 'Available'),
(23, 'UP-11-GH-1212', 'Hatchback', 'Available'),
(24, 'MP-12-IJ-1313', 'SUV', 'Available'),
(25, 'DL-13-LO-1414', 'Sedan', 'Available'),
(27, 'OR-13-KL-1414', 'Sedan', 'Available'),
(28, 'BR-14-UV-3456', 'SUV', 'Available'),
(29, 'JK-15-MN-1515', 'Hatchback', 'Available');
""")
con.commit()


cursor.execute("""
INSERT INTO Order_History (User_Id, Driver_Id, Date, Start_Location, End_Location)
VALUES
(2, 1, '2025-08-01', '28.6139° N, 77.2090° E', '28.6129° N, 77.2295° E'),
(3, 2, '2025-08-01', '19.0760° N, 72.8777° E', '19.1176° N, 72.8790° E'),
(4, 3, '2025-08-02', '12.9716° N, 77.5946° E', '12.9784° N, 77.6408° E'),
(5, 4, '2025-08-02', '13.0827° N, 80.2707° E', '13.0500° N, 80.2121° E'),
(6, 5, '2025-08-03', '17.3850° N, 78.4867° E', '17.4400° N, 78.3489° E'),
(7, 6, '2025-08-03', '18.5204° N, 73.8567° E', '18.5642° N, 73.7768° E'),
(8, 7, '2025-08-04', '22.5726° N, 88.3639° E', '22.5958° N, 88.4734° E'),
(9, 8, '2025-08-04', '26.8467° N, 80.9462° E', '26.8381° N, 81.0421° E'),
(10, 9, '2025-08-05', '23.0225° N, 72.5714° E', '23.0134° N, 72.5974° E'),
(11, 10, '2025-08-05', '26.9124° N, 75.7873° E', '26.9529° N, 75.7777° E'),
(12, 11, '2025-08-06', '23.2599° N, 77.4126° E', '23.2312° N, 77.4338° E'),
(13, 12, '2025-08-06', '25.5941° N, 85.1376° E', '25.6207° N, 85.1722° E'),
(14, 13, '2025-08-07', '21.1702° N, 72.8311° E', '21.1959° N, 72.8302° E'),
(15, 14, '2025-08-07', '30.7333° N, 76.7794° E', '30.7460° N, 76.7797° E'),
(2, 1, '2025-08-08', '23.3441° N, 85.3096° E', '23.3700° N, 85.3250° E'),
(3, 2, '2025-08-08', '21.1458° N, 79.0882° E', '21.1498° N, 79.0849° E'),
(4, 3, '2025-08-09', '22.3072° N, 73.1812° E', '22.3039° N, 73.2028° E'),
(5, 4, '2025-08-09', '30.9010° N, 75.8573° E', '30.8965° N, 75.8559° E'),
(6, 5, '2025-08-10', '18.5204° N, 73.8567° E', '18.5195° N, 73.8553° E'),
(7, 6, '2025-08-10', '21.2514° N, 81.6296° E', '21.2335° N, 81.6296° E'),
(8, 7, '2025-08-11', '9.9312° N, 76.2673° E', '9.9659° N, 76.2832° E'),
(9, 8, '2025-08-11', '8.5241° N, 76.9366° E', '8.5459° N, 76.9150° E'),
(10, 9, '2025-08-12', '13.0827° N, 80.2707° E', '13.0850° N, 80.2707° E'),
(11, 10, '2025-08-12', '18.5204° N, 73.8567° E', '18.5528° N, 73.8707° E'),
(12, 11, '2025-08-13', '12.9716° N, 77.5946° E', '12.9783° N, 77.6271° E'),
(13, 12, '2025-08-13', '28.4595° N, 77.0266° E', '28.4751° N, 77.0266° E'),
(14, 13, '2025-08-14', '19.0760° N, 72.8777° E', '19.0896° N, 72.8777° E'),
(15, 14, '2025-08-14', '23.0225° N, 72.5714° E', '23.0276° N, 72.5714° E'),
(2, 1, '2025-08-15', '12.9716° N, 77.5946° E', '12.9850° N, 77.5946° E'),
(3, 1, '2025-08-16', '28.5355° N, 77.3910° E', '28.5245° N, 77.4040° E'),
(4, 2, '2025-08-16', '12.9801° N, 77.5890° E', '12.9716° N, 77.5946° E'),
(5, 3, '2025-08-17', '19.0790° N, 72.8828° E', '19.0760° N, 72.8777° E'),
(6, 4, '2025-08-17', '22.5726° N, 88.3639° E', '22.5958° N, 88.4734° E'),
(7, 5, '2025-08-18', '17.3850° N, 78.4867° E', '17.4400° N, 78.3489° E'),
(8, 6, '2025-08-18', '13.0827° N, 80.2707° E', '13.0850° N, 80.2707° E'),
(9, 7, '2025-08-19', '23.0225° N, 72.5714° E', '23.0276° N, 72.5714° E'),
(10, 8, '2025-08-19', '26.8467° N, 80.9462° E', '26.8381° N, 81.0421° E'),
(11, 9, '2025-08-20', '18.5204° N, 73.8567° E', '18.5195° N, 73.8553° E'),
(12, 10, '2025-08-20', '30.7333° N, 76.7794° E', '30.7460° N, 76.7797° E'),
(13, 11, '2025-08-21', '26.9124° N, 75.7873° E', '26.9529° N, 75.7777° E'),
(14, 12, '2025-08-21', '25.5941° N, 85.1376° E', '25.6207° N, 85.1722° E'),
(15, 13, '2025-08-22', '20.2961° N, 85.8245° E', '20.2960° N, 85.8245° E'),
(2, 14, '2025-08-22', '23.2599° N, 77.4126° E', '23.2312° N, 77.4338° E'),
(3, 1, '2025-08-23', '31.1471° N, 75.3412° E', '31.1460° N, 75.3412° E'),
(4, 2, '2025-08-23', '26.4499° N, 80.3319° E', '26.4499° N, 80.3389° E'),
(5, 3, '2025-08-24', '27.1767° N, 78.0081° E', '27.1750° N, 78.0081° E'),
(6, 4, '2025-08-24', '21.1458° N, 79.0882° E', '21.1498° N, 79.0849° E'),
(7, 5, '2025-08-25', '22.3072° N, 73.1812° E', '22.3039° N, 73.2028° E'),
(8, 6, '2025-08-25', '11.0168° N, 76.9558° E', '11.0168° N, 76.9994° E'),
(9, 7, '2025-08-26', '15.2993° N, 74.1240° E', '15.4881° N, 73.8278° E'),
(10, 8, '2025-08-26', '28.7041° N, 77.1025° E', '28.6129° N, 77.2295° E'),
(11, 9, '2025-08-27', '12.9716° N, 77.5946° E', '12.9784° N, 77.6408° E'),
(12, 10, '2025-08-27', '19.0760° N, 72.8777° E', '19.0896° N, 72.8777° E'),
(13, 11, '2025-08-28', '23.0225° N, 72.5714° E', '23.0276° N, 72.5714° E'),
(14, 12, '2025-08-28', '22.5726° N, 88.3639° E', '22.5958° N, 88.4734° E'),
(15, 13, '2025-08-29', '17.3850° N, 78.4867° E', '17.4400° N, 78.3489° E'),
(2, 14, '2025-08-29', '13.0827° N, 80.2707° E', '13.0500° N, 80.2121° E'),
(3, 1, '2025-08-30', '26.9124° N, 75.7873° E', '26.9529° N, 75.7777° E'),
(4, 2, '2025-08-30', '18.5204° N, 73.8567° E', '18.5642° N, 73.7768° E'),
(5, 3, '2025-08-31', '22.3072° N, 73.1812° E', '22.3039° N, 73.2028° E'),
(6, 4, '2025-08-31', '21.1458° N, 79.0882° E', '21.1498° N, 79.0849° E'),
(7, 5, '2025-09-01', '23.3441° N, 85.3096° E', '23.3700° N, 85.3250° E'),
(8, 6, '2025-09-01', '27.1767° N, 78.0081° E', '27.1750° N, 78.0081° E'),
(9, 7, '2025-09-02', '31.1471° N, 75.3412° E', '31.1460° N, 75.3412° E'),
(10, 8, '2025-09-02', '30.7333° N, 76.7794° E', '30.7460° N, 76.7797° E'),
(11, 9, '2025-09-03', '25.5941° N, 85.1376° E', '25.6207° N, 85.1722° E'),
(12, 10, '2025-09-03', '28.4595° N, 77.0266° E', '28.4751° N, 77.0266° E'),
(13, 11, '2025-09-04', '19.0760° N, 72.8777° E', '19.1176° N, 72.8790° E'),
(14, 12, '2025-09-04', '18.5204° N, 73.8567° E', '18.5528° N, 73.8707° E'),
(15, 13, '2025-09-05', '22.5726° N, 88.3639° E', '22.5958° N, 88.4734° E'),
(2, 14, '2025-09-05', '17.3850° N, 78.4867° E', '17.4400° N, 78.3489° E'),
(3, 1, '2025-09-06', '23.0225° N, 72.5714° E', '23.0276° N, 72.5714° E'),
(4, 2, '2025-09-06', '30.9010° N, 75.8573° E', '30.8965° N, 75.8559° E'),
(5, 3, '2025-09-07', '12.9716° N, 77.5946° E', '12.9783° N, 77.6271° E'),
(6, 4, '2025-09-07', '26.8467° N, 80.9462° E', '26.8381° N, 81.0421° E'),
(7, 5, '2025-09-08', '20.2961° N, 85.8245° E', '20.2960° N, 85.8245° E'),
(8, 6, '2025-09-08', '11.0168° N, 76.9558° E', '11.0168° N, 76.9994° E'),
(9, 7, '2025-09-09', '13.0827° N, 80.2707° E', '13.0850° N, 80.2707° E'),
(10, 8, '2025-09-09', '22.3072° N, 73.1812° E', '22.3039° N, 73.2028° E'),
(11, 9, '2025-09-10', '21.1702° N, 72.8311° E', '21.1959° N, 72.8302° E'),
(12, 10, '2025-09-10', '26.9124° N, 75.7873° E', '26.9529° N, 75.7777° E'),
(13, 11, '2025-09-11', '23.2599° N, 77.4126° E', '23.2312° N, 77.4338° E'),
(14, 12, '2025-09-11', '28.6139° N, 77.2090° E', '28.6129° N, 77.2295° E'),
(15, 13, '2025-09-12', '23.3441° N, 85.3096° E', '23.3700° N, 85.3250° E'),
(2, 14, '2025-09-12', '21.1458° N, 79.0882° E', '21.1498° N, 79.0849° E'),
(3, 1, '2025-09-13', '12.9716° N, 77.5946° E', '12.9784° N, 77.6408° E'),
(4, 2, '2025-09-13', '23.0225° N, 72.5714° E', '23.0276° N, 72.5714° E'),
(5, 3, '2025-09-14', '22.5726° N, 88.3639° E', '22.5958° N, 88.4734° E'),
(6, 4, '2025-09-14', '17.3850° N, 78.4867° E', '17.4400° N, 78.3489° E'),
(7, 5, '2025-09-15', '19.0760° N, 72.8777° E', '19.0896° N, 72.8777° E'),
(8, 6, '2025-09-15', '13.0827° N, 80.2707° E', '13.0500° N, 80.2121° E');
""")



try:
    con.commit()
except:
    print("Commit Error Rolling Back")
    con.rollback()
    sys.exit(-1)

cursor.close()
con.close()
sys.exit(0)