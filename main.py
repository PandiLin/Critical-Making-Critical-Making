import os
import time
from datetime import datetime
from tqdm import tqdm

def rest(minutes):
    for _ in tqdm(range(minutes * 60), desc="Countdown", unit="s", leave=False):
        time.sleep(1)

def start_exec_at(desinated_time):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"Current time: {current_time}")
    if current_time == desinated_time:
        return True
    else:
        return False


def main_loop(rest_time: int):
    while True:
        print(f"This message is printed every {rest_time} minutes.")
        # Wait for rest_time minutes
        rest(rest_time)

def main(start_execute_time, rest_time):
    try:
        current_time = datetime.now()
        target_time = datetime.strptime(start_execute_time, "%H:%M:%S").replace(year=current_time.year, month=current_time.month, day=current_time.day)
    except ValueError:
        raise ValueError("start_execute_time must be in the format HH:MM:SS")

    while True:
        time_difference = target_time - current_time
        total_seconds = int(time_difference.total_seconds())

        if current_time >= target_time:
            print("Time difference is negative, exiting.")
            break

        # Display countdown
        for _ in tqdm(range(total_seconds), desc="Countdown to start", unit="s", leave=False):
            time.sleep(1)
        break  # Exit the loop when countdown is done

    main_loop(rest_time)

try:
    import sys
    start_execute_time = sys.argv[1]
    rest_time = int(sys.argv[2])
    main(start_execute_time, rest_time)
except KeyboardInterrupt:
    print("Timer stopped by user.")
