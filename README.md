# Network Connectivity Tester

A Python-based network connectivity tester that uses the `scapy` library to send ICMP (ping) requests to a list of hosts, measure the round-trip time, and log the results. It also plots the ping test results over time and uses `matplotlib` library to display the results in a functional graph after the run.

## Installation

Make sure you have Python 3.x installed. Then, install the required Python modules using the following command:

```bash
pip install scapy matplotlib
```

## Running the Script

### Command-Line Arguments

- `--hosts`: Comma-separated list of hosts to ping (e.g., '8.8.4.4,1.0.0.1'). Default is `8.8.8.8,1.1.1.1`.
- `--duration`: Test duration in seconds. Default is `30`.
- `--interval`: Ping interval in seconds. Default is `1`.
- `--packet_size`: Packet size in bytes. Default is `32`.
- `--ttl`: TTL (Time to Live). Default is `64`.
- `--nolog`: Skips the creation of a logfile.

### Example Usage

1. **Running with defaults (8.8.8.8, 1.1.1.1)**:

    ```bash
    python network_tester.py
    ```

2. **Running with custom hosts and other arguments**:

    ```bash
    python network_tester.py --hosts "8.8.4.4,1.0.0.1" --duration 10 --interval 2 --packet_size 64 --ttl 128 --nolog
    ```

## Known Issues

- **Windows Native Raw Sockets Error**: On Windows, raw sockets require administrator privileges. You may encounter the following error:

    ```
    Error pinging 8.8.8.8: Windows native L3 Raw sockets are only usable as administrator !
    ```

    **Solution**:
    - **Run the Script as Administrator**:
      - In Windows, raw sockets (which are used to send ICMP pings) require administrator privileges.
      - If you are using Command Prompt, VSCode or any other software to run the code. Run the software elevated then try running the script again.
