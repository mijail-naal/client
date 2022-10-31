#  "Client for sending metrics"


import socket
import time


class ClientError(Exception):

    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args[0] if args else None

    def __str__(self):
        return f"Error: {self.msg}"



class Client:
    """ Client for sending metrics """

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError("Cannot create connection", err)


    def _to_split(self, data):
        # Function to convert received data-bytes into a list
        if type(data) == bytes:
            s = data.decode("utf-8")
            return s.split()
        else:
            return data.split()


    def _convert_to_dict(self, data):
        # Function to convert  the received data into a dictionary in the format:
        # {'server': [(timestamp1, metric_value1), (timestamp2, metric_value2), …]…}
        # Convert the values "timestamp" and "metric_value" respectively to types int and float,
        # and sort the list by "timestamp" (ascending).
        def to_sort(e):
            return e[0]
        x = {}
        a = [x for x in data[1::3]]
        b = [x for x in data[2::3]]
        c = [x for x in data[3::3]]

        try:
            for i in range(len(a)):
                if a[i] in x:
                    w = x[a[i]]
                    w.append(tuple((int(c[i]), float(b[i]))))
                    w.sort(key=to_sort)
                    x[a[i]] = w
                else:
                    x[a[i]] = [tuple((int(c[i]), float(b[i])))]
            return x
        except:
            raise ClientError('Invalid data')


    def put(self, key, value, timestamp=None):

        if not timestamp:
            timestamp = int(time.time())

        try:
            self.connection.sendall(f"put {key} {value} {timestamp}\n".encode())
        except socket.error as err:
            raise ClientError("sending data to the server failed at last attempt")

        data = self.connection.recv(1024)
        data_split = self._to_split(data)

        if data_split[0] == 'error':
            raise ClientError('an error occurred while reading the data')


    def get(self, key):
        if key == "*":
            self.connection.send("get *\n".encode("utf-8"))
        else:
            self.connection.send(f"get {key}\n".encode("utf-8"))

        data = self.connection.recv(1024)
        data_split = self._to_split(data)

        if data_split == []:
            raise ClientError('No data')

        elif data_split[0] == 'ok':
            return self._convert_to_dict(data_split)

        else:
            raise ClientError('Invalid data')


    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientError("Do not close the connection", err)

