"""
Nurse Mentor AI - Database backup and restore.

Copies the SQLite database file to a chosen location
and restores it from a backup file.
"""

import os
import shutil
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "clinic.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")


def _ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        try:
            os.makedirs(BACKUP_DIR)
        except Exception:
            pass


def create_backup():
    """
    Create a timestamped backup of clinic.db inside backups/.
    Returns the backup file path or None on failure.
    """
    if not os.path.exists(DB_PATH):
        return None

    _ensure_backup_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = "clinic_backup_{}.db".format(timestamp)
    backup_path = os.path.join(BACKUP_DIR, filename)

    try:
        shutil.copy2(DB_PATH, backup_path)
        return backup_path
    except Exception as e:
        print("Backup failed:", repr(e))
        return None


def list_backups():
    """
    Return a list of (filename, full_path, size_kb, modified_time)
    for all backups, newest first.
    """
    _ensure_backup_dir()
    items = []
    try:
        for name in os.listdir(BACKUP_DIR):
            if not name.endswith(".db"):
                continue
            path = os.path.join(BACKUP_DIR, name)
            stat = os.stat(path)
            items.append({
                "filename": name,
                "path": path,
                "size_kb": round(stat.st_size / 1024.0, 1),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime(
                    "%Y-%m-%d %H:%M"
                ),
            })
    except Exception:
        pass

    items.sort(key=lambda x: x["modified"], reverse=True)
    return items


def restore_backup(backup_path):
    """
    Replace clinic.db with the given backup file.
    Returns True on success, False otherwise.
    """
    if not os.path.exists(backup_path):
        return False

    try:
        # Safety: backup current DB first
        if os.path.exists(DB_PATH):
            safety = DB_PATH + ".before_restore"
            shutil.copy2(DB_PATH, safety)

        shutil.copy2(backup_path, DB_PATH)
        return True
    except Exception as e:
        print("Restore failed:", repr(e))
        return False


def delete_backup(backup_path):
    try:
        if os.path.exists(backup_path):
            os.remove(backup_path)
            return True
    except Exception:
        pass
    return False


def backup_dir_path():
    _ensure_backup_dir()
    return BACKUP_DIR