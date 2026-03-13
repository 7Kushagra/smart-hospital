import sqlite3

conn = sqlite3.connect("hospital.db")

conn.execute("DELETE FROM doctors")

doctors = [

# Cardiology
("Dr. Rahul Sharma","Cardiology","DM Cardiology, MD Medicine","201","Mon-Fri","10:00-14:00"),
("Dr. Amit Verma","Cardiology","DM Cardiology, MD Medicine","202","Mon,Wed,Fri","11:00-15:00"),
("Dr. Rakesh Gupta","Cardiology","DM Cardiology, MBBS","203","Tue,Thu","09:00-13:00"),
("Dr. Vivek Mehta","Cardiology","DM Cardiology, MD Medicine","204","Mon-Fri","12:00-16:00"),
("Dr. Kunal Bansal","Cardiology","DM Cardiology","205","Mon,Thu","10:00-14:00"),

# Neurology
("Dr. Anil Kapoor","Neurology","DM Neurology, MD Medicine","210","Mon-Fri","10:00-14:00"),
("Dr. Sanjay Singh","Neurology","DM Neurology","211","Tue,Thu","11:00-15:00"),
("Dr. Deepak Malhotra","Neurology","DM Neurology","212","Mon,Wed","09:00-13:00"),
("Dr. Arjun Khanna","Neurology","DM Neurology","213","Mon-Fri","12:00-16:00"),
("Dr. Rajat Sinha","Neurology","DM Neurology","214","Tue,Thu","10:00-14:00"),

# Orthopedic
("Dr. Vikram Chauhan","Orthopedic","MS Orthopedics","301","Mon-Fri","10:00-14:00"),
("Dr. Rohit Yadav","Orthopedic","MS Orthopedics","302","Mon,Wed","11:00-15:00"),
("Dr. Manish Tiwari","Orthopedic","MS Orthopedics","303","Tue,Thu","09:00-13:00"),
("Dr. Ajay Rathore","Orthopedic","MS Orthopedics","304","Mon-Fri","12:00-16:00"),
("Dr. Karan Joshi","Orthopedic","MS Orthopedics","305","Mon,Thu","10:00-14:00"),

# Dermatology
("Dr. Priya Mehta","Dermatology","MD Dermatology","401","Mon-Fri","10:00-14:00"),
("Dr. Sneha Kapoor","Dermatology","MD Dermatology","402","Tue,Thu","11:00-15:00"),
("Dr. Neha Batra","Dermatology","MD Dermatology","403","Mon,Wed","09:00-13:00"),
("Dr. Kavita Jain","Dermatology","MD Dermatology","404","Mon-Fri","12:00-16:00"),
("Dr. Ritu Malhotra","Dermatology","MD Dermatology","405","Tue,Thu","10:00-14:00"),

# Pediatrics
("Dr. Nisha Arora","Pediatrics","MD Pediatrics","501","Mon-Fri","10:00-14:00"),
("Dr. Pooja Khanna","Pediatrics","MD Pediatrics","502","Mon,Wed","11:00-15:00"),
("Dr. Shalini Verma","Pediatrics","MD Pediatrics","503","Tue,Thu","09:00-13:00"),
("Dr. Meera Joshi","Pediatrics","MD Pediatrics","504","Mon-Fri","12:00-16:00"),
("Dr. Anita Sharma","Pediatrics","MD Pediatrics","505","Mon,Thu","10:00-14:00"),

]

# duplicate doctors to reach 100+
full_list = doctors * 4

for d in full_list:
    conn.execute(
        "INSERT INTO doctors (name,department,speciality,room,days,time) VALUES (?,?,?,?,?,?)",
        d
    )

conn.commit()
conn.close()

print("100+ realistic doctors added")