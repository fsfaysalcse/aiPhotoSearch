import psycopg2
import pickle

# Update these with your actual database credentials
DATABASE = 'facerecognition'
USER = 'fsfaysalcse'  # Replace with your PostgreSQL username
PASSWORD = 'password'  # Replace with your PostgreSQL password
HOST = 'localhost'  # Use 'localhost' if your database is on the local machine

def create_connection():
    """ Create a database connection to the PostgreSQL database """
    try:
        conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
    return None

# The create_table function might be redundant if you've already created the table manually
def create_table():
    """ Create a table for storing face encodings and image paths """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS faces (
        id SERIAL PRIMARY KEY,
        encoding BYTEA NOT NULL,
        image_path TEXT NOT NULL
    );
    """
    conn = create_connection()
    if conn is not None:
        try:
            conn.autocommit = True  # Setting autocommit to True
            c = conn.cursor()
            c.execute(create_table_sql)
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

def insert_face_encoding(encoding, image_path):
    """ Insert a new face encoding into the faces table """
    conn = create_connection()
    if conn is not None:
        sql = ''' INSERT INTO faces(encoding, image_path) VALUES(%s,%s) '''
        try:
            cur = conn.cursor()
            binary_encoding = pickle.dumps(encoding)
            cur.execute(sql, (binary_encoding, image_path))
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error inserting encoding into database: {e}")
        finally:
            conn.close()

def get_all_faces():
    """ Retrieve all face encodings and image paths from the database """
    conn = create_connection()
    all_faces = []
    if conn is not None:
        sql = ''' SELECT * FROM faces '''
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                encoding = pickle.loads(row[1])
                image_path = row[2]
                all_faces.append((encoding, image_path))
        except psycopg2.Error as e:
            print(f"Error retrieving faces from database: {e}")
        finally:
            conn.close()
    return all_faces

# You can comment out this line if you've already created the table manually
# create_table()
