"""
===============================================================
Check Registered Users
===============================================================
"""

from app.db.database import SessionLocal
from app.db.models import User


def check_users():

    print()

    print("=" * 70)

    print("REGISTERED USERS")

    print("=" * 70)

    database = SessionLocal()

    try:

        users = database.query(
            User
        ).all()

        if not users:

            print()

            print("No users found.")

            return

        for user in users:

            print()

            print(f"ID: {user.id}")

            print(
                f"Username: {user.username}"
            )

            print(
                f"Email: {user.email}"
            )

            print(
                f"Hashed Password: "
                f"{user.hashed_password}"
            )

            print(
                f"Created At: "
                f"{user.created_at}"
            )

            print("-" * 70)

    finally:

        database.close()


if __name__ == "__main__":

    check_users()