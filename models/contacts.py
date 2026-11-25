import re
from collections import UserDict
from collections.abc import Iterable
from datetime import date, datetime, timedelta

from .fields import Field


class Name(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name is required.")
        super().__init__(value.strip())


class Phone(Field):
    """A contact phone number with validation."""

    def __init__(self, value: str):
        if not isinstance(value, str) or not re.fullmatch(
            r"[0-9]{10}", value
        ):
            raise ValueError(
                "Phone number must contain exactly 10 digits."
            )

        super().__init__(value)


class Email(Field):
    """A contact email address with validation."""

    def __init__(self, value: str):
        pattern = (
            r"[A-Za-z0-9_%+-]+"
            r"(?:\.[A-Za-z0-9_%+-]+)*"
            r"@"
            r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+"
            r"[A-Za-z]{2,}"
        )

        if not isinstance(value, str) or not re.fullmatch(
            pattern, value
        ):
            raise ValueError("Invalid email address.")

        super().__init__(value)

class Address(Field):
    """A contact's physical address."""


class Birthday(Field):
    """A contact's date of birth with validation."""

    def __init__(self, value: str | date):

        if isinstance(value, str):
            try:
                if not re.fullmatch(r"[0-9]{2}\.[0-9]{2}\.[0-9]{4}", value):
                    raise ValueError

                birthday = datetime.strptime(
                    value, "%d.%m.%Y"
                ).date()

            except ValueError:
                raise ValueError(
                    "Invalid date format. Use DD.MM.YYYY."
                )

        elif type(value) is date:
            birthday = value

        else:
            raise ValueError("Invalid birthday value.")

        if birthday > date.today():
            raise ValueError(
                "Birthday cannot be in the future."
            )

        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """A contact with a required name and optional contact details."""

    def __init__(
        self,
        name: str,
        *,
        phones: Iterable[str] = (),
        email: str | None = None,
        address: str | None = None,
        birthday: date | None = None,
    ):
        self.name = Name(name)
        if isinstance(phones, str):
            raise ValueError("Pass phone numbers as a collection of strings.")
        self.phones = [Phone(number) for number in phones]
        self.email = Email(email) if email is not None else None
        self.address = Address(address) if address is not None else None
        self.birthday = Birthday(birthday) if birthday is not None else None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str) -> Phone | None:
        for stored_phone in self.phones:
            if stored_phone.value == phone:
                return stored_phone
        return None

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        stored_phone = self.find_phone(old_phone)
        if stored_phone is None:
            raise ValueError("Phone number not found.")
        self.phones[self.phones.index(stored_phone)] = Phone(new_phone)

    def remove_phone(self, phone: str) -> None:
        stored_phone = self.find_phone(phone)
        if stored_phone is None:
            raise ValueError("Phone number not found.")
        self.phones.remove(stored_phone)

    def set_email(self, email: str | None) -> None:
        self.email = Email(email) if email is not None else None

    def set_address(self, address: str | None) -> None:
        self.address = Address(address) if address is not None else None

    def set_birthday(self, birthday: date | None) -> None:
        self.birthday = Birthday(birthday) if birthday is not None else None


class AddressBook(UserDict[str, Record]):
    """Store contacts by their exact, whitespace-trimmed names."""

    def add_record(self, record: Record) -> None:
        name = record.name.value
        if name in self.data:
            raise ValueError(f"Contact {name} already exists.")
        self.data[name] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name.strip())

    def search(self, query: str) -> list[Record]:
        """Find contacts by a case-insensitive substring in any searchable field."""
        query = query.strip().casefold()
        if not query:
            return []

        matches = []
        for record in self.data.values():
            fields = (record.name, *record.phones, record.email, record.address)
            if any(query in str(field).casefold() for field in fields if field is not None):
                matches.append(record)
        return matches

    def rename(self, name: str, new_name: str) -> None:
        old_key = name.strip()
        record = self.data[old_key]
        updated_name = Name(new_name)
        new_key = updated_name.value
        if new_key == old_key:
            return
        if new_key in self.data:
            raise ValueError(f"Contact {new_key} already exists.")
        record.name = updated_name
        self.data[new_key] = self.data.pop(old_key)

    def delete(self, name: str) -> None:
        del self.data[name.strip()]
        
    def get_upcoming_birthdays(self, days: int = 7) -> list:

        if type(days) is not int or days < 0:
            raise ValueError(
                "Days must be a non-negative integer."
            )

        today = date.today()
        end_date = today + timedelta(days=days)
        upcoming_birthdays = []

        for record in self.data.values():

            if record.birthday is None:
                continue

            birthday = record.birthday.value

            for year in range(today.year, end_date.year + 1):

                try:
                    birthday_this_year = birthday.replace(
                        year=year
                    )

                except ValueError:
                    birthday_this_year = date(year, 2, 28)

                if today <= birthday_this_year <= end_date:

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime(
                            "%d.%m.%Y"
                        )
                    })

        upcoming_birthdays.sort(
            key=lambda item: datetime.strptime(
                item["birthday"], "%d.%m.%Y"
            )
        )

        return upcoming_birthdays   
    