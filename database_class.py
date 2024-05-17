
import mysql
import mysql.connector
from datetime import datetime


class DatabaseConnector:
    def __init__(self):
        self.host = 'sql8.freesqldatabase.com'
        self.user = 'sql8707280'
        self.password = 'ZwRRg72v9H'
        self.dbname = 'sql8707280'
        self.port = 3306  # Default port for MySQL

        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.dbname,
                port=self.port
            )
            print("Connected to database successfully!")
        except mysql.connector.Error as e:
            print("Unable to connect to the database:", e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from database.")


    def execute_query(self, query):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                print("Query executed successfully!")
            except mysql.connector.Error as e:
                print("Error executing query:", e)
        else:
            print("Not connected to the database.")

    # fetching transactions for all transactions
    def fetch_all_transactions(self):
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM transactions")
                result = cursor.fetchall()
                return result
            except mysql.connector.Error as e:
                print("Error fetching transactions:", e)
                return None

    # fetching specific account details
    def search_account(self, account_number):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT * FROM accounts_data WHERE account_number = %s"
                cursor.execute(query, (account_number,))
                result = cursor.fetchone()
                cursor.close()
                return result
            except mysql.connector.Error as e:
                print("Error searching for account:", e)
                return None
        else:
            print("Not connected to the database.")
            return None

    # for updating total balance amount in accounts_data table from selected account
    def update_balance(self, account_number, amount):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE accounts_data SET total_balance = total_balance - %s WHERE account_number = %s"
            cursor.execute(query, (amount, account_number))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error updating balance:", e)
            return False

    # for adding data in the transactions table for selected account
    def record_transaction(self, account_number, amount, transaction_type, details=""):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO transactions (account_number, date_time, amount, transaction_type, transaction_details)
            VALUES (%s, %s, %s, %s, %s)
            """
            current_time = datetime.now()
            cursor.execute(query, (account_number, current_time, amount, transaction_type, details))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error recording transaction:", e)
            return False


    #transfer funds query function

    def transfer_transactions(self, sender_account_number, receiver_account_number, transfer_amount):
        try:
            cursor = self.connection.cursor()

            # Check sender's balance
            cursor.execute("SELECT total_balance FROM accounts_data WHERE account_number = %s",
                           (sender_account_number,))
            sender_balance = cursor.fetchone()[0]
            if sender_balance < transfer_amount:
                raise Exception("Insufficient funds")

            # Update sender's balance
            cursor.execute("UPDATE accounts_data SET total_balance = total_balance - %s WHERE account_number = %s",
                           (transfer_amount, sender_account_number))

            # Update receiver's balance
            cursor.execute("UPDATE accounts_data SET total_balance = total_balance + %s WHERE account_number = %s",
                           (transfer_amount, receiver_account_number))

            # Record transaction for sender
            cursor.execute("""
                INSERT INTO transactions (account_number, date_time, amount, transaction_type, transaction_details)
                VALUES (%s, %s, %s, %s, %s)
                """, (sender_account_number, datetime.now(), -transfer_amount, 'txn_fd.sent',
                      f'Transferred to {receiver_account_number}'))

            # Record transaction for receiver
            cursor.execute("""
                INSERT INTO transactions (account_number, date_time, amount, transaction_type, transaction_details)
                VALUES (%s, %s, %s, %s, %s)
                """, (receiver_account_number, datetime.now(), transfer_amount, 'txn_fd.rcvd',
                      f'Received from {sender_account_number}'))

            # Commit all changes
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Database error:", e)
            self.connection.rollback()
            cursor = self.connection.cursor()
            cursor.close()
            return False
        except Exception as e:
            print("Transaction failed:", e)
            self.connection.rollback()
            cursor = self.connection.cursor()
            cursor.close()
            return False


    #checking transactions query function
    def fetch_transactions(self, account_number):
        query = """
        SELECT *
        FROM transactions
        WHERE account_number = %s
        ORDER BY date_time DESC
        """
        try:
            cursor = self.connection.cursor(dictionary=True)  # Use dictionary cursor to return data as dictionaries
            cursor.execute(query, (account_number,))
            transactions = cursor.fetchall()
            cursor.close()
            return transactions
        except mysql.connector.Error as e:
            print(f"Error fetching transactions: {e}")
            return []


    #authenticate user

