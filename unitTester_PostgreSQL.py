__author__ = 'Fujiwara'


import psycopg2


def main():

    try:
        conn = psycopg2.connect("dbname='database SE Y2' user='postgres' host='localhost' password='admin' port='5432'")
    except:
        print ("I am unable to connect to the database")
        return

    cur = conn.cursor()
    cur.execute("SELECT pres_name from president")
    rows = cur.fetchall()

    print("\nShow me the databases:\n")
    for row in rows:
        print("   ", row[0])

if __name__ == '__main__':
    main()