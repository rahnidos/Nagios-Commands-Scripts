import psycopg2
from dotenv import load_dotenv
import os
import sys

load_dotenv()

try:
    host = sys.argv[1]
except IndexError:
    print("UNKNOWN - Please provide the host as a command line argument.")
    sys.exit(3)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

if not db_user or not db_password:
    print("UNKNOWN - Missing database credentials in .env file.")
    sys.exit(3)

try:
    connection = psycopg2.connect(
        host=host,
        user=db_user,
        password=db_password
    )
except psycopg2.OperationalError as e:
    print(f"UNKNOWN - Failed to connect to the database: {e}")
    sys.exit(3)  

try:
    query = "SELECT public.get_long_running_queries();"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    if result is None or result[0] == 0:
        print("OK - Query returned 0.")
        sys.exit(0)
    elif result[0] < 5:
        print(f"WARNING - There are {result[0]} connections open longer than 5 minutes.")
        sys.exit(1)
    else:
        print(f"CRITICAL - There are {result[0]} connections open longer than 5 minutes.")
        sys.exit(2)
except Exception as e:
    print(f"UNKNOWN - Error while executing query: {e}")
    sys.exit(3)
finally:
    connection.close()



