import sys
import time

import mariadb as mariadb
import mvg_api


def addToDatabase(check, product, label, destination, timestamp, cancelled, sev, delay):
    if not cancelled:
        cancelled = 0
    else:
        cancelled = 1

    if not sev:
        sev = 0
    else:
        sev = 1

    cursor.execute("SELECT * FROM T_DEPARTURE WHERE PRODUCT = %s AND LABEL = %s AND TIMESTAMP = %s AND DESTINATION = %s",
                   (product, label, timestamp, destination))

    try:
        for (id) in cursor:
            check = id
    except:
        pass

    if check == "":
        cursor.execute(
            "INSERT INTO T_DEPARTURE (PRODUCT, LABEL, DESTINATION, TIMESTAMP, CANCELLED, SEV, DELAY) "
            "VALUES (%s, %s, %s, %s,%s, %s, %s)", (product, label, destination, timestamp, cancelled, sev, delay)
        )
    else:
        cursor.execute("UPDATE T_DEPARTURE SET CANCELLED = %s AND SEV = %s AND DELAY = %s "
                       "WHERE PRODUCT = %s AND LABEL = %s AND DESTINATION = %s AND TIMESTAMP = %s",
                       (cancelled, sev, delay, product, label, destination, timestamp))


def getInformation(qry) -> list:

    result = []

    for i in range(len(qry)):
        result_set = []
        check = ""
        product = qry[i]['product']
        label = qry[i]['label']
        destination = qry[i]['destination']
        timestamp = mvg_api._convert_time(qry[i]['departureTime'])
        cancelled = qry[i]['cancelled']
        sev = qry[i]['sev']
        try:
            delay = qry[i]['delay']
        except:
            delay = 0

        result_set.append(check)
        result_set.append(product)
        result_set.append(label)
        result_set.append(destination)
        result_set.append(timestamp)
        result_set.append(cancelled)
        result_set.append(sev)
        result_set.append(delay)

        result.append(result_set)

    return result


if __name__ == '__main__':
    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3306,
            database="MVG-TRACKER"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

u_bahn_id = mvg_api.get_id_for_station("Olympia-Einkaufszentrum")

bus_id = mvg_api.get_id_for_station("Dessauerstraße")

# Get Cursor
cursor = conn.cursor()

while True:
    departures = mvg_api.get_departures(u_bahn_id)

    bus_departures = mvg_api.get_departures(bus_id)

    result = getInformation(departures)

    for i in range(len(result)):
        addToDatabase(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4], result[i][5],
                      result[i][6], result[i][7])

    bus_Result = getInformation(bus_departures)

    for r in range(len(bus_Result)):
        addToDatabase(bus_Result[r][0], bus_Result[r][1], bus_Result[r][2], bus_Result[r][3], bus_Result[r][4],
                      bus_Result[r][5], bus_Result[r][6], bus_Result[r][7])

    cursor.execute(
        "COMMIT"
    )

    time.sleep(5)
