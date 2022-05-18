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
            "VALUES (%s, %s, %s, %s ,%s, %s, %s)", (product, label, destination, timestamp, cancelled, sev, delay)
        )
    else:
        cursor.execute("UPDATE T_DEPARTURE SET CANCELLED = %s AND SEV = %s AND DELAY = %s "
                       "WHERE PRODUCT = %s AND LABEL = %s AND DESTINATION = %s AND TIMESTAMP = %s",
                       (cancelled, sev, delay, product, label, destination, timestamp))


def getInformation(qry) -> list:
    for i in range(len(qry)):
        check = ""
        product = qry[i]['product']
        label = qry[i]['label']
        destination = qry[i]['destination']
        timestamp = mvg_api._convert_time(qry[i]['departureTime'])
        cancelled = qry[i]['cancelled']
        sev = qry[i]['sev']
        delay = qry[i]['delay']

        result = []
        result.append(check)
        result.append(product)
        result.append(label)
        result.append(destination)
        result.append(timestamp)
        result.append(cancelled)
        result.append(sev)
        result.append(delay)

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

    addToDatabase(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])

    bus_result = getInformation(bus_departures)

    addToDatabase(bus_result[0], bus_result[1], bus_result[2], bus_result[3], bus_result[4], bus_result[5],
                  bus_result[6], bus_result[7])

    cursor.execute(
        "COMMIT"
    )

    time.sleep(10)
