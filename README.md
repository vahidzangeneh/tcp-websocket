# How to run project:

# create a new virtual environment
``python3 -m venv tonies``

# activate the virtual environment  
``cd tonies``  
``source bin/activate``

# install the requirements  
``cd tcp-websocket``

``pip install -r requirements.txt``

# run unit tests
You can run unit tests to make sure that everything is working well.

``python3 -m unittest -v``


# run the socket server
The setting parameters of the project are provided in the ``config.py`` file. 
You can change the settings in this file before run the server.

``python3 server.py``


Now server is ready to accept connections.

# run the socket client
``python3 client.py``

Now you can enter message and press enter. The server prints your message in stdout.
You can open multiple terminals and then run client to have multiple clients at the same time.