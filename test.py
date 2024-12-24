import os
import random
import time

# File to store progress
PROGRESS_FILE = "progress.txt"

# Inflation rate
INFLATION_RATE = 0.01

# List of common, short, and simple names (extended to ensure uniqueness)
common_names = ["Alice", "Bob", "Eve", "Tom", "Jim", "Sam", "Max", "Zoe", "Lee", "Ray", "Sue", "Ben", "Lia", "Jan", "Kai", "Leo", "Jay", "Kim", "Amy", "Chloe", "Jade", "Luke", "Ella", "Owen", "Nina", "Mia", "Ryan", "Jack", "Liam", "Sophia", "Daniel", "Maya", "Ava", "Ben", "Ella", "Mason", "Liam", "Emma", "Olivia", "Isla", "Sophia", "Matthew", "Grace", "Jacob", "Charlotte", "Michael", "Lily", "Chloe"]

# Ensure unique user names by randomly selecting and removing names from the list
def generate_unique_names(num_users):
    names = random.sample(common_names, num_users)  # Select num_users unique names
    return names

# Initialize users with unique names and investments logic
users = [
    {
        "name": generate_unique_names(1)[0],  # Assign a unique name to each user
        "money": random.randint(50, 200),
        "level": 1,
        "job": None,
        "life_score": 100,
        "tags": [],
        "decision_weights": [1, 1, 1, 1, 1],
        "investments": []  # Track user's investments in companies
    }
    for i in range(1, 51)  # Now creating 50 users
]

# Initialize jobs
jobs = [
    {"title": "Software Engineer", "salary": 50},
    {"title": "Teacher", "salary": 30},
    {"title": "Artist", "salary": 20},
    {"title": "Mechanic", "salary": 40}
]

# Initialize companies
companies = []
company_names = ["TechNova", "GreenPeak", "Skyline Dynamics", "QuantumCore", "EcoFlow Ventures"]
for _ in range(5):
    companies.append({
        "name": random.choice(company_names),
        "stock_price": random.randint(50, 200),
        "growth_rate": random.uniform(-0.1, 0.2),
        "investors": []  # Track list of users investing in the company
    })

# Bank system
bank = {
    "loans": {},  # {username: amount}
    "loan_records": [],  # Record of all loans granted
    "interest_rate": 0.05
}

# Define rules for the economy
RULES = [
    {"event": "earn_money", "amount": lambda: random.randint(10, 50)},
    {"event": "spend_money", "amount": lambda: random.randint(5, 30)},
    {"event": "level_up", "requirement": lambda user: user["money"] >= 200},
    {"event": "collect_salary", "requirement": lambda user: user["job"] is not None},
    {"event": "pay_other_user", "amount": lambda: random.randint(5, 20)}
]

def apply_rule(user):
    """Applies a rule to a user based on their decision weights."""
    decision = random.choices(RULES, weights=user["decision_weights"])[0]
    if decision["event"] == "earn_money":
        amount = decision["amount"]()
        user["money"] += amount
        adjust_weights(user, decision, success=True)
        return f"{user['name']} earned ${amount}."
    elif decision["event"] == "spend_money":
        amount = decision["amount"]()
        adjusted_amount = int(amount * (1 + INFLATION_RATE))
        if user["money"] >= adjusted_amount:
            user["money"] -= adjusted_amount
            user["life_score"] = max(0, user["life_score"] - adjusted_amount // 10)  # Faster life score decrease
            adjust_weights(user, decision, success=True)
            return f"{user['name']} spent ${adjusted_amount} and lost life points."
        else:
            adjust_weights(user, decision, success=False)
            return f"{user['name']} wanted to spend ${adjusted_amount} but didn't have enough money."
    elif decision["event"] == "level_up":
        if decision["requirement"](user):
            user["level"] += 1
            user["money"] -= 200  # Reset money after leveling up
            adjust_weights(user, decision, success=True)
            return f"{user['name']} leveled up to Level {user['level']}!"
    elif decision["event"] == "collect_salary":
        if decision["requirement"](user):
            job = next((job for job in jobs if job["title"] == user["job"]), None)
            if job:
                user["money"] += job["salary"]
                adjust_weights(user, decision, success=True)
                return f"{user['name']} collected a salary of ${job['salary']} from their job as a {user['job']}!"
    elif decision["event"] == "pay_other_user":
        if user["money"] >= 10:
            recipient = random.choice([u for u in users if u != user])
            amount = decision["amount"]()
            user["money"] -= amount
            recipient["money"] += amount
            adjust_weights(user, decision, success=True)
            return f"{user['name']} paid ${amount} to {recipient['name']}."
    adjust_weights(user, decision, success=False)
    return None

def adjust_weights(user, decision, success):
    """Adjusts decision weights based on success or failure."""
    index = RULES.index(decision)
    if success:
        user["decision_weights"][index] += 0.1
    else:
        user["decision_weights"][index] -= 0.1
    user["decision_weights"] = [max(0.1, w) for w in user["decision_weights"]]

def assign_job(user):
    """Assigns a random job to a user."""
    job = random.choice(jobs)
    user["job"] = job["title"]
    return f"{user['name']} got a new job as a {job['title']}!"

def update_companies(tick_count):
    """Updates stock prices for companies and tracks investment gains/losses."""
    for company in companies:
        growth = company["growth_rate"] * company["stock_price"]
        company["stock_price"] = max(1, round(company["stock_price"] + growth))
        
        # Apply investment gains/losses to users based on stock price changes
# Modify the investment logic to give Bob more money from investments
def update_companies(tick_count):
    """Updates stock prices for companies and tracks investment gains/losses."""
    for company in companies:
        growth = company["growth_rate"] * company["stock_price"]
        company["stock_price"] = max(1, round(company["stock_price"] + growth))
        
        # Apply investment gains/losses to users based on stock price changes
        for investor in company["investors"]:
            # After the 25th tick, increase investment gains
            investment_multiplier = 3 if tick_count > 25 else 1
            investment_change = company["growth_rate"] * 20 * investment_multiplier  # Assuming 50 was the initial investment amount
            
            # If the user's name is 'Bob', they gain more from investments
            if investor["name"] == "Bob":
                investment_change *= 2  # Bob gains more (double the normal amount)
            
            if investment_change != 0:
                investor["money"] += investment_change
                action = "gained" if investment_change > 0 else "lost"
                print(f"{investor['name']} {action} ${abs(investment_change)} from their investment in {company['name']}.")


def process_loans():
    """Processes loans for users more frequently, avoiding spam."""
    for user, loan_amount in list(bank["loans"].items()):
        interest = loan_amount * bank["interest_rate"]
        total_due = loan_amount + interest
        borrower = next((u for u in users if u["name"] == user), None)
        if borrower and borrower["money"] >= total_due:
            borrower["money"] -= total_due
            del bank["loans"][user]
        elif borrower:
            bank["loans"][user] = total_due
        else:
            bank["loans"][user] += interest  # Add more frequent interest

def grant_loan(user, amount):
    """Grants a loan to a user, avoiding loan spam."""
    if user["name"] not in bank["loans"]:  # Only grant a loan if they haven't received one already
        bank["loans"][user["name"]] = amount
        user["money"] += amount
        if "loan_receiver" not in user["tags"]:  # Avoid spamming the loan_receiver tag
            user["tags"].append("loan_receiver")
        # Record the loan details
        bank["loan_records"].append({"user": user["name"], "loan_amount": amount, "time": time.time()})
        print(f"{user['name']} received a loan of ${amount}.")

def save_progress(tick_count):
    """Saves the current state of all users and companies to a file."""
    with open(PROGRESS_FILE, "w") as f:
        for user in users:
            f.write(f"{user['name']} | Money: ${user['money']} | Level: {user['level']} | Job: {user['job']} | Life: {user['life_score']} | Tags: {', '.join(user['tags'])}\n")
        f.write("\nCompanies:\n")
        for company in companies:
            f.write(f"{company['name']} | Stock Price: ${company['stock_price']} | Investors: {', '.join([investor['name'] for investor in company['investors']])}\n")
        f.write("\nBank Loans:\n")
        for user, amount in bank["loans"].items():
            f.write(f"{user} owes ${amount}\n")
        f.write("\nLoan Records:\n")
        for record in bank["loan_records"]:
            f.write(f"{record['user']} received a loan of ${record['loan_amount']} at {time.ctime(record['time'])}\n")
        f.write(f"\nTick: {tick_count}\n")

def main():
    """Main function to run the simulation."""
    print("Starting the enhanced economy simulation. Press Ctrl+C to stop.")
    tick_count = 0
    try:
        while True:
            for user in users:
                if user["life_score"] <= 0 and "dead" not in user["tags"]:
                    print(f"{user['name']} has died and is tagged as 'dead'.")
                    user["tags"].append("patched_issue")  # Add  tag if user dies
                    continue
                if not user["job"]:
                    print(assign_job(user))
                result = apply_rule(user)
                if result:
                    print(result)
                
                # Increase the chance of investments at the start 
                if random.random() < 0.2:  # 20% chance for the first part of the simulation
                    company_to_invest = random.choice(companies)
                    if user["money"] >= 200:  # Only allow investing if they have at least $200
                        user["money"] -= 50
                        if "investor" not in user["tags"]:  # Prevent tag spamming
                            user["tags"].append("investor")
                        company_to_invest["investors"].append(user)
                        user["investments"].append(company_to_invest["name"])
                        print(f"{user['name']} invested in {company_to_invest['name']}.")

                # Offer loans more frequently
                if random.random() < 0.1:  # 10% chance to offer a loan every tick
                    loan_amount = random.randint(50, 200)
                    grant_loan(user, loan_amount)
            
            update_companies(tick_count)
            process_loans()  # More frequent processing of loans
            save_progress(tick_count)
            tick_count += 1
            time.sleep(1)  # Wait for 1 second before the next tick
    except KeyboardInterrupt:
        print("Simulation stopped. Progress saved.")

if __name__ == "__main__":
    main()
