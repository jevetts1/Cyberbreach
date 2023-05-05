__author__ = "Jayden Evetts"
__copyright__ = "Copyright 2023, Kaze"
__license__ = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__ = "1.0"
__email__ = "jayden.evetts@gmail.com"

import pyodbc

def retrieve_csv_vulnerabilities(num_rows = 1000) -> dict:
    server = 'kaze-sql-server.database.windows.net'
    database = 'cpe_red'
    username = 'kazeadmin'
    password = '{KazeConsulting001}'
    driver= '{ODBC Driver 18 for SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT TOP {num_rows} * FROM red_score_cpe_view")
            row = cursor.fetchone()

            table = {}

            while row:
                table[row[1]] = row[2]

                row = cursor.fetchone()

    return table