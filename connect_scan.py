import socket
import threading
import argparse

def check_port(host, port, timeout, output_file=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        if result == 0:
            message = f"Success: {host}:{port}"
        else:
            message = f"Failure: {host}:{port}"
        
        if output_file:
            with open(output_file, "a") as f:
                f.write(message + "\n")
        print(message)
        
        sock.close()
    except Exception as e:
        print(f"Error checking {host}:{port}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Check if hosts are reachable on port 445.")
    parser.add_argument("host_file", help="Path to the file containing a list of hosts")
    parser.add_argument("--port", type=int, default=445, help="Port to check (default: 445)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use (default: 10)")
    parser.add_argument("--timeout", type=int, default=5, help="Connection timeout in seconds (default: 5)")
    parser.add_argument("--output", help="Output file for results")
    args = parser.parse_args()

    with open(args.host_file, "r") as file:
        hosts = file.read().splitlines()

    threads = []
    max_threads = args.threads

    for host in hosts:
        thread = threading.Thread(target=check_port, args=(host, args.port, args.timeout, args.output))
        threads.append(thread)
        thread.start()

        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
