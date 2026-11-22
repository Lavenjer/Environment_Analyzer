Firstly, the models file declares each variable and their datatype.
These variables will have their values taken from the public database which is managed by the fetch_data.py file.
This data should be processed using a service file (not made yet) and this service file will be called when the url of the page matches a pattern defined in url.py.
The url.py file will then connect to views.py. views.py will then connect the url files and the templates (html files).