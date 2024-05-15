# auth_controller.py
from database_class import DatabaseConnector

def authenticate_user(username, password):
    db = DatabaseConnector()
    db.connect()

    try:
        cursor = db.connection.cursor()
        query = "SELECT employee_id, employee_name FROM Employees WHERE employee_username = %s AND employee_password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            employee_id, employee_name = result
            user_details = {
                'employee_id': employee_id,
                'employee_name': employee_name
            }
            return True, user_details
        else:
            return False, {}

    except Exception as e:
        print("Error occurred during authentication:", e)
        return False, {}

    finally:
        db.disconnect()
