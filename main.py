#!/usr/bin/env python3

import logging
import time

import psutil


def main():
    setup_logging()

    # Track how long memory has been high
    high_memory_min_duration = 120
    high_memory_threshold = 80

    print("Memory Monitor Started...")
    print("Monitoring for:")
    print(
        f"  - Memory usage > {high_memory_threshold}% for {high_memory_min_duration // 60} minutes"
    )
    print("  - Swap memory usage")
    print("  - OOM kill events")

    high_memory_start_time = None
    used_swap = None

    while True:
        try:
            high_memory_start_time = check_memory_usage(
                high_memory_start_time,
                duration=high_memory_min_duration,
                threshold=high_memory_threshold,
            )
            used_swap = check_swap_usage(used_swap)
            check_oom_kills()
            time.sleep(10)
        except KeyboardInterrupt:
            print("Memory monitoring stopped.")
            break
        except Exception as e:
            logging.error(f"Error during monitoring: {e}")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="memory_monitor.log",
    )


def check_memory_usage(high_memory_start_time: float | None, **kwargs) -> float | None:
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    duration = kwargs.get("duration", 120)
    threshold = kwargs.get("threshold", 80)

    if mem_percent > threshold:
        if high_memory_start_time is None:
            high_memory_start_time = time.time()
            logging.warning(f"Memory usage high: {mem_percent:.1f}%")
        else:
            duration = time.time() - high_memory_start_time
            if duration >= duration:
                logging.critical(
                    f"HIGH MEMORY ALERT: {mem_percent:.1f}% for {duration:.0f} seconds"
                )
    else:
        if high_memory_start_time is not None:
            logging.info(f"Memory usage returned to normal: {mem_percent:.1f}%")
            high_memory_start_time = None

    return high_memory_start_time


def check_swap_usage(used_swap: float | None) -> float | None:
    swap = psutil.swap_memory()
    if swap.used > 0 and used_swap != swap.used:
        swap_percent = swap.percent
        used_swap = swap.used
        logging.warning(
            f"Swap memory in use: {swap.used / (1024**2):.2f} MB ({swap_percent:.1f}%)"
        )
    return used_swap


def check_oom_kills():
    try:
        with open("/proc/vmstat", "r") as f:
            for line in f:
                if "oom_kill" in line:
                    parts = line.strip().split()
                    if len(parts) >= 2 and int(parts[1]) > 0:
                        logging.critical(f"OOM kill detected: {parts[1]} occurrences")
    except Exception as e:
        logging.error(f"Error checking OOM kills: {e}")


if __name__ == "__main__":
    main()
