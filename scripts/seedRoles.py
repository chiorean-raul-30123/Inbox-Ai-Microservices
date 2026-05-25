from inbox_shared.database import createDbSession
from inbox_shared.repositories import RoleRepository


def main():
    db = createDbSession()
    roleRepository = RoleRepository()

    try:
        roles = [
            ("ADMIN", "Administrator"),
            ("HR", "Human Resources"),
            ("FINANCE", "Finance Department"),
            ("LEGAL", "Legal Department"),
        ]

        for name, description in roles:
            existingRole = roleRepository.getByName(db, name)

            if existingRole is None:
                roleRepository.create(
                    db,
                    name=name,
                    description=description,
                )

        print("Roles seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()