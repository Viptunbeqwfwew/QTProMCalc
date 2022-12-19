import socket
from Event import Event
import threading
from netcon.IThreadNet import IThreadNet
import io
import os


class Connect(IThreadNet):
    thread_connect: threading.Thread
    got_a_message: Event = Event()
    socket_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip: str = ""
    port: int = 0

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def start(self):
        if self.ping():
            self._run = self.__run()
            self.socket_connect.connect((self.ip, self.port))
            self.thread_connect = threading.Thread(target=lambda: next(self._run), daemon=True)
            self.thread_connect.start()
        else:
            raise Exception("Не удалось подключится.")

    def stop(self):
        try:
            self.WORK = False
        except Exception:
            raise Exception("LOL")

    def resume(self):
        if self.ping():
            self.PAUSE = False
            self.thread_connect = threading.Thread(target=lambda: next(self._run), daemon=True)
        else:
            raise Exception("Не удалось возобновить подключение.")

    def ping(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
                soc.connect((self.ip, self.port))
            return True
        except socket.error:
            soc.close()
            del soc
            return False

    def __run(self):
        while self.WORK:
            if self.PAUSE:
                yield 0
            n = int(self.socket_connect.recv(1024))
            data = self.socket_connect.recv(1024)
            if data != b"":
                self.got_a_message.invoke(self, data)
        self.EVENT_STOP.invoke(self)

    def send(self, massage: bytes):
        self.socket_connect.send(massage)

    def sendFile(self, file: str, n: int = 0):
        stats = os.stat(file)
        d = stats.st_size - n
        with open(file, mode="rb") as f:
            self.send(bytes(d))
            f.seek(n)
            for _ in range(d // 1024 + (0 if d % 1024 == 0 else 1)):
                self.send(f.read(1024))


class Server(IThreadNet):
    accepted: Event = Event()
    server_thread: threading.Thread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip: str, port: int):
        self.server_socket.bind((ip, port))
        self.listen(1)

    def listen(self, n: int):
        self.server_socket.listen(n)

    def accept(self):
        self.accepted.invoke(self.server_socket.accept())

    def __run(self):
        while self.WORK:
            if self.PAUSE:
                yield 0
            self.accept()
        self.EVENT_STOP.invoke(self)


class ClientP2P:
    server: Server
    connected_client: list

    def __init__(self, ip: str, port: int, bl: list):
        self.black_list = bl
        self.server = Server(ip, port)


class Massager:
    def sendMassage(self, con: socket.socket, msg: str):
        con.send(msg)


