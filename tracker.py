#!/usr/bin/env python3
"""BFD Application Tracker - tracks volunteer service applications."""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List

DATA_FILE = os.path.expanduser("~/.bfd_tracker.json")


@dataclass
class Application:
    org: str
    contact: str
    email: str
    status: str
    field: str
    city: str
    date_sent: str
    notes: str = ""


class Tracker:
    def __init__(self):
        self.apps: List[Application] = []
        self._load()

    def _load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as f:
                data = json.load(f)
                self.apps = [Application(**a) for a in data]

    def _save(self):
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(a) for a in self.apps], f, indent=2)

    def add(self, org: str, contact: str, email: str, field: str, city: str, notes: str = ""):
        app = Application(
            org=org,
            contact=contact,
            email=email,
            status="sent",
            field=field,
            city=city,
            date_sent=datetime.now().isoformat()[:10],
            notes=notes,
        )
        self.apps.append(app)
        self._save()
        print(f"Added: {org} ({city})")

    def list(self):
        if not self.apps:
            print("No applications yet.")
            return
        for i, a in enumerate(self.apps, 1):
            print(f"{i}. [{a.status.upper()}] {a.org} | {a.city} | {a.field} | {a.date_sent}")

    def update(self, index: int, status: str, notes: str = ""):
        if 1 <= index <= len(self.apps):
            self.apps[index - 1].status = status
            if notes:
                self.apps[index - 1].notes += f"; {notes}"
            self._save()
            print(f"Updated #{index} -> {status}")
        else:
            print("Invalid index.")

    def seed(self):
        defaults = [
            ("DRK BW", "Anne Müller", "Anne.Mueller@drk-bw.de", "Verwaltung", "Stuttgart", "Coordinator"),
            ("DRK Reutlingen", "Verwaltung", "verwaltung@rettungsdienst-reutlingen.de", "Verwaltung", "Reutlingen", "Mixed admin/warehouse"),
            ("DRK Böblingen", "Ehrenamt", "ehrenamt@drkbb.org", "Verwaltung", "Böblingen", "Bounced - resent"),
            ("DRK Landesschule", "M. Schwarz", "m.schwarz@drk-ls.de", "Schule/Verwaltung", "Stuttgart", "Admin for training school"),
            ("DRK Landesverband BW", "Jennifer Schier", "Jennifer.Schier@drk-bw.de", "Bevölkerungsschutz", "Stuttgart", "Crisis mgmt/project work"),
            ("DRK Tübingen", "Carola Bahlinger", "c.bahlinger@drk-tuebingen.de", "Bevölkerungsschutz", "Tübingen", "Auto-reply received"),
            ("DRK Ludwigsburg", "Wehner", "wehner@drk-ludwigsburg.de", "Bevölkerungsschutz", "Ludwigsburg", "Simple admin tasks"),
        ]
        for org, contact, email, field, city, notes in defaults:
            self.add(org, contact, email, field, city, notes)
        print("Seeded with your current applications.")


if __name__ == "__main__":
    import sys
    t = Tracker()

    if len(sys.argv) < 2:
        print("Usage: python tracker.py <command> [args]")
        print("Commands: add, list, update, seed")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "seed":
        t.seed()
    elif cmd == "list":
        t.list()
    elif cmd == "add" and len(sys.argv) >= 7:
        t.add(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7] if len(sys.argv) > 7 else "")
    elif cmd == "update" and len(sys.argv) >= 4:
        t.update(int(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    else:
        print("Unknown command or missing args.")
