import requests
import random

BASE_URL = "http://127.0.0.1:8001"

# Step 1: Register a user
print("Registering user...")
requests.post(f"{BASE_URL}/auth/register", json={
    "username": "admin",
    "email": "admin@placement.com",
    "password": "admin123"
})

# Step 2: Login and get token
print("Logging in...")
response = requests.post(f"{BASE_URL}/auth/login", data={
    "username": "admin",
    "password": "admin123"
})
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"Token received ✅")

# Step 3: Data to generate from
companies = [
    "Infosys", "TCS", "Wipro", "HCL", "Cognizant",
    "Accenture", "IBM", "Capgemini", "Tech Mahindra", "LTIMindtree",
    "Amazon", "Microsoft", "Google", "Zoho", "Freshworks",
    "Deloitte", "EY", "KPMG", "Hexaware", "Mphasis"
]

roles = [
    "Systems Engineer", "Software Engineer", "Associate Engineer",
    "Junior Developer", "Data Analyst", "Cloud Engineer",
    "DevOps Engineer", "QA Engineer", "Business Analyst",
    "Full Stack Developer", "Backend Developer", "Frontend Developer"
]

first_names = [
    "Rahul", "Priya", "Arjun", "Sneha", "Vikram", "Anjali", "Rohit",
    "Deepika", "Karthik", "Pooja", "Aditya", "Megha", "Suresh", "Divya",
    "Naveen", "Kavya", "Siddharth", "Lakshmi", "Harish", "Nandini",
    "Ravi", "Shreya", "Manoj", "Swathi", "Ganesh", "Revathi", "Ajay",
    "Bhavana", "Prasad", "Keerthi", "Varun", "Mounika", "Nikhil", "Sravya"
]

last_names = [
    "Sharma", "Reddy", "Kumar", "Singh", "Patel", "Rao", "Nair",
    "Iyer", "Gupta", "Verma", "Joshi", "Mehta", "Pillai", "Naidu",
    "Krishnan", "Choudhary", "Bhat", "Mishra", "Saxena", "Agarwal"
]

statuses = ["Offered", "Offered", "Offered", "Pending", "Rejected"]
years = [2022, 2023, 2024, 2025]

packages = {
    "Google": (18, 35), "Amazon": (14, 28), "Microsoft": (16, 30),
    "Zoho": (8, 14), "Freshworks": (9, 16), "Infosys": (5, 9),
    "TCS": (4, 8), "Wipro": (5, 9), "HCL": (5, 8), "Cognizant": (5, 9),
    "Accenture": (6, 10), "IBM": (6, 11), "Capgemini": (5, 9),
    "Tech Mahindra": (5, 8), "LTIMindtree": (7, 12),
    "Deloitte": (8, 14), "EY": (7, 12), "KPMG": (7, 13),
    "Hexaware": (5, 9), "Mphasis": (6, 10)
}

# Step 4: Insert 500 records
print("Inserting 500 placement records...")
success = 0

for i in range(500):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    company = random.choice(companies)
    role = random.choice(roles)
    low, high = packages[company]
    package = round(random.uniform(low, high), 1)
    status = random.choice(statuses)
    year = random.choice(years)

    response = requests.post(f"{BASE_URL}/placements/", headers=headers, json={
        "student_name": name,
        "company": company,
        "role": role,
        "package_lpa": package,
        "status": status,
        "year": year
    })

    if response.status_code == 200:
        success += 1
        if success % 50 == 0:
            print(f"  {success} records inserted...")

print(f"\n✅ Done! {success} placement records added to database.")
print("Your database now has real data!")