import json
import os
import argparse
import time
from datetime import datetime, date, time as dtime, timedelta
from typing import Tuple
import urllib.request
import urllib.error


DATA_FILE = 'forest_data.json'


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_hours(friend, date_str, hours):
    data = load_data()
    friend_data = data.get(friend, {})
    friend_data[date_str] = friend_data.get(date_str, 0) + hours
    data[friend] = friend_data
    save_data(data)


def show_hours(friend):
    data = load_data()
    return data.get(friend, {})


def total_hours(friend):
    friend_data = show_hours(friend)
    return sum(friend_data.values())


def fetch_forest_hours(profile_url: str) -> Tuple[str, float]:
    """Fetch today's hours from a Forest profile URL.

    This function assumes the URL returns JSON with ``date`` and ``hours``
    fields for the current day. If the API differs, adjust the parsing logic
    accordingly.
    """
    try:
        with urllib.request.urlopen(profile_url, timeout=10) as resp:
            body = resp.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(f'Failed to fetch profile data: {exc}') from exc

    data = json.loads(body.decode())
    return data["date"], float(data["hours"])


def track_daily(friend: str, profile_url: str) -> None:
    """Continuously record a friend's hours each day at 23:59."""
    while True:
        now = datetime.now()
        target = datetime.combine(now.date(), dtime(23, 59))
        if now >= target:
            target += timedelta(days=1)
        time.sleep((target - now).total_seconds())

        date_str, hours = fetch_forest_hours(profile_url)
        add_hours(friend, date_str, hours)



def parse_args():
    parser = argparse.ArgumentParser(description='Track daily Forest study hours for a friend.')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add hours for a date.')
    add_parser.add_argument('friend')
    add_parser.add_argument('date', help='Date in YYYY-MM-DD format')
    add_parser.add_argument('hours', type=float)

    show_parser = subparsers.add_parser('show', help='Show hours by date.')
    show_parser.add_argument('friend')

    total_parser = subparsers.add_parser('total', help='Show total hours.')
    total_parser.add_argument('friend')

    track_parser = subparsers.add_parser('track', help='Auto record daily hours.')
    track_parser.add_argument('friend')
    track_parser.add_argument('profile_url', help='URL returning today\'s hours')

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == 'add':
        # Validate date format
        try:
            datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            raise SystemExit('Date must be in YYYY-MM-DD format')
        add_hours(args.friend, args.date, args.hours)
    elif args.command == 'show':
        data = show_hours(args.friend)
        for date, hours in sorted(data.items()):
            print(f'{date}: {hours}')
    elif args.command == 'total':
        print(total_hours(args.friend))

    elif args.command == 'track':
        print(f'Tracking {args.friend}... press Ctrl+C to stop')
        track_daily(args.friend, args.profile_url)

    else:
        print('No command specified')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
