# MVG-Tracker_Backend

This Python script fetches all information about buses and subways at the Munich stops Olympia Einkaufszentrum and Dessauerstraße at regular intervals. This is then stored in a local database for data analysis purposes.

#2 API
Used APIs are on the one hand the REST API of the Münchner Verkehrsgesellschaft (MVG) and an interface to address the database.

#2 Further information about the API
Information about the MVG interface can be found here: https://pypi.org/project/mvg-api/

#2 Python script
The Python script addresses this interface and requests the specific data. This data is then evaluated and stored in a database using an SQL command.

#2 Usage
The data collected is used for data analysis purposes only.
