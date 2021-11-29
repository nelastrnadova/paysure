import argparse
import json
import socket
from json import JSONDecodeError

from paysure.core import Core
from paysure.lib.database import Database

parser = argparse.ArgumentParser()
parser.add_argument("-ip", type=str, help="Ip to run on", default="127.0.0.1")
parser.add_argument("-port", type=int, help="port to run on", default=8000)
parser.add_argument("-db", type=str, help="Path to db file", default="database.db")
args = parser.parse_args()

db = Database(args.db)


def main(ip="127.0.0.1", port=8000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()

    running = True

    try:
        while running:
            connection, client_address = sock.accept()
            data = connection.recv(1024)
            request = data.decode().split("\r\n")
            request_info = request[0].split(" ")
            method = request_info[0]
            endpoint = request_info[1][1:]
            try:
                request_body = json.loads(data.decode().split("\r\n\r\n")[1])
            except JSONDecodeError:
                request_body = {}
            response = router(method=method, endpoint=endpoint, body=request_body)
            connection.sendall(create_http_response(response[0], response[1]))
            connection.close()
    except KeyboardInterrupt:
        pass

    sock.close()


def router(method: str, endpoint: str, body: json):
    if endpoint == "pay":
        return handle_payment_route(method, body)
    return "", 404


def handle_payment_route(method, body):  # TODO: move
    if not check_method("POST", method):
        return "", 405
    if 'payment_message_request_xml' not in body:
        return "", 400
    return Core().handle_payment(body['payment_message_request_xml'])


def check_method(target_method: str, method: str) -> bool:
    return target_method == method


def create_http_response(response_body: str, status_code: int):
    return f"HTTP/1.1 {status_code}\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}".encode(
        "utf-8"
    )


if __name__ == "__main__":
    print("starting server")
    main(ip=args.ip, port=args.port)
