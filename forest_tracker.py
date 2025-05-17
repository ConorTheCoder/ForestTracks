import json
import os
import argparse
from datetime import datetime

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
    else:
        print('No command specified')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
