import sqlite3


def create_account():
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your Name: ")
    pin = input("Create your PIN: ")
    balance = float(input("Enter Initial Balance: "))

    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO accounts(name, pin, balance) VALUES (?, ?, ?)",
        (name, pin, balance)
    )

    conn.commit()
    conn.close()

    print("\nAccount Created Successfully!")
    print("Welcome,", name)


def login():
    print("\n========== ATM LOGIN ==========")

    pin = input("Enter your PIN: ")

    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM accounts WHERE pin=?",
        (pin,)
    )

    account = cursor.fetchone()
    conn.close()

    if account:
        print("\nLogin Successful!")
        print("Welcome,", account[1])
        print("Your Balance: ₹", account[3])

        print("\n========== ATM MENU ==========")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Logout")
        print("5. Transaction History")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nYour Current Balance: ₹", account[3])

        elif choice == "2":
            deposit = float(input("\nEnter Deposit Amount: ₹ "))

            if deposit > 0:
                new_balance = account[3] + deposit

                conn = sqlite3.connect("atm.db")
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE accounts SET balance=? WHERE id=?",
                    (new_balance, account[0])
                )

                conn.commit()
                conn.close()

                print("\nDeposit Successful!")
                print("Deposited Amount: ₹", deposit)
                print("New Balance: ₹", new_balance)

                conn = sqlite3.connect("atm.db")
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO transactions(account_id, transaction_type, amount, balance) VALUES (?, ?, ?, ?)",
                    (account[0], "Deposit", deposit, new_balance)
                )

                conn.commit()
                conn.close()

            else:
                print("\nInvalid Deposit Amount!")

        elif choice == "3":
            withdraw = float(input("\nEnter Withdrawal Amount: ₹ "))

            if withdraw <= 0:
                print("\nInvalid Withdrawal Amount!")

            elif withdraw > account[3]:
                print("\nInsufficient Balance!")

            else:
                new_balance = account[3] - withdraw

                conn = sqlite3.connect("atm.db")
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE accounts SET balance=? WHERE id=?",
                    (new_balance, account[0])
                )

                conn.commit()
                conn.close()

                print("\nWithdrawal Successful!")
                print("Withdrawn Amount: ₹", withdraw)
                print("Remaining Balance: ₹", new_balance)

                conn = sqlite3.connect("atm.db")
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO transactions(account_id, transaction_type, amount, balance) VALUES (?, ?, ?, ?)",
                    (account[0], "Withdraw", withdraw, new_balance)
                )

                conn.commit()
                conn.close()

        elif choice == "4":
            print("\nLogged Out Successfully!")

        elif choice == "5":
            print("\n========== TRANSACTION HISTORY ==========")

            conn = sqlite3.connect("atm.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT transaction_type, amount, balance FROM transactions WHERE account_id=?",
                (account[0],)
            )

            transactions = cursor.fetchall()
            conn.close()

            if transactions:
                for transaction in transactions:
                    print(
                        "Type:", transaction[0],
                        "| Amount: ₹", transaction[1],
                        "| Balance: ₹", transaction[2]
                    )
            else:
                print("No Transactions Found!")

        else:
            print("\nInvalid Choice")

    else:
        print("\nInvalid PIN!")


print("\n========== ATM MANAGEMENT SYSTEM ==========")
print("1. Create Account")
print("2. Login")
print("3. Exit")
print("==========================================")

choice = input("Enter your choice: ")

if choice == "1":
    create_account()

elif choice == "2":
    login()

elif choice == "3":
    print("Thank You!")

else:
    print("Invalid Choice")