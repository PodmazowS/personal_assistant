from collections import UserDict
from collections.abc import Iterable
from datetime import date

from .fields import Field


class Name(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name is required.")
        super().__init__(value.strip())


class Phone(Field):
    """A contact phone number."""


class Email(Field):
    """A contact email address."""


class Address(Field):
    """A contact's physical address."""


class Birthday(Field):
    """A contact's date of birth, without a time component."""

    def __init__(self, value: date):
        if type(value) is not date:
            raise ValueError("Birthday must be a datetime.date.")
        super().__init__(value)


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
