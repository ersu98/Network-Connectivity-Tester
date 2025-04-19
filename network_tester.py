import time
import csv
import os
import scapy.all as scapy
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import asyncio
import argparse

# Disable Scapy warnings
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Function to ping a host asynchronously
async def ping_host(host, interval, duration, log_file, results, plot_data, packet_size, ttl):
    end_time = time.time() + duration
    ping_times = []

    while time.time() < end_time:
        try:
            start_time = time.time()  # Record time before sending ping
            response = scapy.sr1(scapy.IP(dst=host, ttl=ttl) / scapy.ICMP(), timeout=1, verbose=False)
            round_trip_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            if response:
                ping_times.append(round(round_trip_time, 4))
                status = f"Success ({round_trip_time:.4f} ms)"
                print(f"Ping to {host}: {status}")
            else:
                ping_times.append(None)
                status = "Failed"
                print(f"Ping to {host} failed.")

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            results.append(f"[{timestamp}] Ping to {host}: {status}")

            # Log result to CSV
            if log_file:
                with open(log_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, host, status])

            # Update plot data
            plot_data.setdefault(host, []).append(ping_times[-1])

        except Exception as e:
            print(f"Error pinging {host}: {e}")
            results.append(f"Error pinging {host}: {e}")

        await asyncio.sleep(interval)

    return host, ping_times


# Plotting the ping results
def plot_ping_results(plot_data):
    for host, ping_times in plot_data.items():
        plt.plot(ping_times, label=host)
    
    plt.title("Ping Test Results")
    plt.xlabel("Ping Count")
    plt.ylabel("Round-Trip Time (ms)")
    plt.legend()
    plt.show()


# Run the ping test
async def run_ping_test(hosts, duration, interval, packet_size, ttl, log_file):
    results = []
    plot_data = defaultdict(list)

    print(f"Starting ping test to hosts: {hosts}")
    print(f"Test duration: {duration}s, Interval: {interval}s, Packet size: {packet_size} bytes, TTL: {ttl}")

    # Create the results folder and log file if logging is enabled
    if log_file:
        os.makedirs("results", exist_ok=True)
        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
        log_file = os.path.join("results", log_filename)

    # Run the ping tests asynchronously
    tasks = [ping_host(host, interval, duration, log_file, results, plot_data, packet_size, ttl) for host in hosts]
    await asyncio.gather(*tasks)

    print("Test complete.")
    plot_ping_results(plot_data)


# Parse command-line arguments and start the test
def main():
    parser = argparse.ArgumentParser(description="Network Connectivity Tester")
    parser.add_argument("--hosts", type=str, help="Comma-separated list of hosts to ping (e.g., '1.1.1.1,8.8.8.8')")
    parser.add_argument("--duration", type=int, default=30, help="Test duration in seconds")
    parser.add_argument("--interval", type=int, default=1, help="Ping interval in seconds")
    parser.add_argument("--packet_size", type=int, default=32, help="Packet size in bytes")
    parser.add_argument("--ttl", type=int, default=64, help="TTL (Time to Live)")
    parser.add_argument("--nolog", action="store_true", help="Skip logging to CSV and creation of results folder")

    args = parser.parse_args()

    # Set default hosts if not provided
    hosts = args.hosts.split(',') if args.hosts else ["8.8.8.8", "1.1.1.1"]

    # Determine if logging should be enabled
    log_file = None if args.nolog else "log"

    # Run the ping test asynchronously
    try:
        asyncio.run(run_ping_test(hosts, args.duration, args.interval, args.packet_size, args.ttl, log_file))
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        exit(0)


if __name__ == "__main__":
    main()
