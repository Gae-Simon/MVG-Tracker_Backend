import sys
import time

import mariadb as mariadb
import mvg_api


def addToDatabase(check, product, label, destination, timestamp, cancelled, sev, delay, departure_id):
    if not cancelled:
        cancelled = 0
    else:
        cancelled = 1

    if not sev:
        sev = 0
    else:
        sev = 1

    cursor.execute("SELECT ID FROM T_DEPARTURE WHERE DEPARTURE_ID = '%s'", destination)

    try:
        for (id) in cursor:
            check = id
    except:
        pass

    if check == "":
        cursor.execute(
            "INSERT INTO T_DEPARTURE (PRODUCT, LABEL, DESTINATION, TIMESTAMP, CANCELLED, SEV, DELAY, DEPARTURE_ID) "
            "VALUES (%s, %s, %s, %s,%s, %s, %s, %s)",
            (product, label, destination, timestamp, cancelled, sev, delay, departure_id)
        )
    else:
        cursor.execute("UPDATE T_DEPARTURE SET CANCELLED = %s AND SEV = %s AND DELAY = %s "
                       "WHERE DEPARTURE_ID = %s",
                       (cancelled, sev, delay, departure_id))

    cursor.execute(
        "COMMIT"
    )

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
        departure_id = qry[i]['departureId']

        result_set.append(check)
        result_set.append(product)
        result_set.append(label)
        result_set.append(destination)
        result_set.append(timestamp)
        result_set.append(cancelled)
        result_set.append(sev)
        result_set.append(delay)
        result_set.append(departure_id)

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

# Get Cursor
cursor = conn.cursor()

stations = []

with open('stations_muc.txt') as f:
    station_with_id = f.readlines()

    for i in station_with_id:
        x = i.split(" | ")
        stations.append(x[1].removesuffix("\n"))

while True:

    for s in stations:

        try:
            departures = mvg_api.get_departures(s)
        except:
            pass

        try:
            result = getInformation(departures)
        except:
            pass
        for i in range(len(result)):
            addToDatabase(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4], result[i][5],
                          result[i][6], result[i][7], result[i][8])

    time.sleep(5)
