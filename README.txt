Forest Tracker
==============

This repository provides a simple command-line tool to track the daily study
hours for friends using the "Forest" study tracking app. Hours are stored in a
JSON file (`forest_data.json`) in the repository.

Usage
-----

Add hours for a friend on a specific date:

```
python3 forest_tracker.py add <friend> <YYYY-MM-DD> <hours>
```

Show recorded hours by date for a friend:

```
python3 forest_tracker.py show <friend>
```

Show the total number of hours recorded for a friend:

```
python3 forest_tracker.py total <friend>
```

Running Tests
-------------

Run the unit tests with:

```
python3 -m unittest discover -s tests
```
