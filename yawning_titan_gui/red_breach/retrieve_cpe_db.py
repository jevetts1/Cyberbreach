__author__ = "Jayden Evetts"
__copyright__ = "Copyright 2023, Kaze"
__license__ = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__ = "1.0"
__email__ = "jayden.evetts@gmail.com"

from databricks import sql
import sys
import os

def retrieve_csv_vulnerabilities(access_token:str) -> dict:
    table = {}

    sql.logger = False

    connection = sql.connect(
                            server_hostname = "adb-350479030933577.17.azuredatabricks.net",
                            http_path = "/sql/1.0/warehouses/95b0b1d238d7ec24",
                            access_token = access_token)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * from red_score.cpe_red WHERE CONTAINS(cpe23Uri, 'siemens');")

        old_stdout = sys.stdout            # stops the cursor.fetchall()
        sys.stdout = open(os.devnull, "w") # function from being verbose

        result = cursor.fetchall()

        sys.stdout = old_stdout            # resetting the output to how it was before

        for row in result:
            table[row["cpe23Uri"]] = row["red_score"]

    cursor.close()
    connection.close()

    return table

retrieve_csv_vulnerabilities("dapia278e1cf00c56e0a53e2d96045a54878")