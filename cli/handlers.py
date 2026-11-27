from datetime import datetime
from enum import Enum

from rich.table import Table

from cli.output import build_table
from models.contacts import AddressBook, Record
from models.notes import Note, Notebook
from utils.exceptions import input_error


class Command(str, Enum):
    HELLO = "hello"
    HELP = "help"
    CLOSE = "close"
    EXIT = "exit"

    # Contacts
    ADD = "add"
    CHANGE = "change"
    REMOVE_PHONE = "remove-phone"
    PHONE = "phone"
    ALL = "all"
    SEARCH = "search"
    ADD_EMAIL = "add-email"
    ADD_ADDRESS = "add-address"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"
    RENAME = "rename"
    DELETE = "delete"

    # Notes
    ADD_NOTE = "add-note"
    ALL_NOTES = "all-notes"
    EDIT_NOTE = "edit-note"
    DELETE_NOTE = "delete-note"
    SEARCH_NOTE = "search-note"
    ADD_TAG = "add-tag"
    REMOVE_TAG = "remove-tag"
    SEARCH_TAG = "search-tag"
    SORT_TAGS = "sort-tags"


EXIT_COMMANDS = (Command.CLOSE, Command.EXIT)
ALL_COMMANDS = tuple(cmd.value for cmd in Command)


def _contacts_table(title: str, records: list[Record]) -> Table:
    rows = []
    for record in records:
        phones = ", ".join(p.value for p in record.phones) if record.phones else "—"
        email = record.email.value if record.email else "—"
        address = record.address.value if record.address else "—"
        bday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "—"
        rows.append((record.name.value, phones, email, address, bday))

    return build_table(
        title=title,
        columns=("Name", "Phones", "Email", "Address", "Birthday"),
        rows=rows,
    )


def _notes_table(title: str, notes: list[Note]) -> Table:
    rows = []
    for note in notes:
        tags = ", ".join(f"#{t.value}" for t in note.tags) if note.tags else "—"
        rows.append((note.title, tags, note.text))

    return build_table(
        title=title,
        columns=("Title", "Tags", "Text"),
        rows=rows,
    )


# --- Contact Handlers ---


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name, phones=[phone])
        book.add_record(record)
        return f"[green]Contact '{name}' added.[/green]"
    record.add_phone(phone)
    return f"[green]Phone {phone} added to contact '{name}'.[/green]"


@input_error
def change_phone(args: list[str], book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.edit_phone(old_phone, new_phone)
    return f"[green]Phone updated for '{name}'.[/green]"


@input_error
def remove_phone(args: list[str], book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.remove_phone(phone)
    return f"[green]Phone {phone} removed from '{name}'.[/green]"


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    if not record.phones:
        return f"Contact '{name}' has no phone numbers."
    return f"[bold]{name}[/bold]: {', '.join(p.value for p in record.phones)}"


@input_error
def show_all_contacts(book: AddressBook):
    if not book.data:
        return "Address book is empty."
    return _contacts_table("Address Book", list(book.data.values()))


@input_error
def search_contacts(args: list[str], book: AddressBook):
    query = " ".join(args)
    if not query:
        raise IndexError
    matches = book.search(query)
    if not matches:
        return f"No contacts found matching '{query}'."
    return _contacts_table(f"Search Results: '{query}'", matches)


@input_error
def set_email(args: list[str], book: AddressBook):
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.set_email(email)
    return f"[green]Email set for '{name}'.[/green]"


@input_error
def set_address(args: list[str], book: AddressBook):
    if len(args) < 2:
        raise IndexError
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.set_address(address)
    return f"[green]Address set for '{name}'.[/green]"


@input_error
def set_birthday(args: list[str], book: AddressBook):
    name, bday_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    try:
        parsed_date = datetime.strptime(bday_str.strip(), "%d.%m.%Y").date()
    except ValueError as err:
        raise ValueError("Invalid date format. Use DD.MM.YYYY.") from err
    record.set_birthday(parsed_date)
    return f"[green]Birthday set for '{name}'.[/green]"


@input_error
def show_birthday(args: list[str], book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    if record.birthday is None:
        return f"Birthday is not set for '{name}'."
    return f"[bold]{name}[/bold]'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args: list[str], book: AddressBook):
    if not hasattr(book, "get_upcoming_birthdays"):
        return "[yellow]Upcoming birthdays feature is not available yet.[/yellow]"
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No birthdays in the next {days} days."
    rows = [(item["name"], item["congratulation_date"]) for item in upcoming]
    return build_table(
        title=f"Upcoming Birthdays (next {days} days)",
        columns=("Name", "Congratulation Date"),
        rows=rows,
    )


@input_error
def rename_contact(args: list[str], book: AddressBook):
    old_name, new_name, *_ = args
    if book.find(old_name) is None:
        raise KeyError(old_name)
    book.rename(old_name, new_name)
    return f"[green]Contact '{old_name}' renamed to '{new_name}'.[/green]"


@input_error
def delete_contact(args: list[str], book: AddressBook):
    name = args[0]
    if book.find(name) is None:
        raise KeyError(name)
    book.delete(name)
    return f"[green]Contact '{name}' deleted.[/green]"


# --- Note Handlers ---


@input_error
def add_note(args: list[str], notebook: Notebook):
    if len(args) < 2:
        raise IndexError
    title = args[0]
    text = " ".join(args[1:])
    note = Note(title, text)
    notebook.add_note(note)
    return f"[green]Note '{title}' added.[/green]"


@input_error
def show_all_notes(notebook: Notebook):
    if not notebook.data:
        return "Notebook is empty."
    return _notes_table("Notebook", list(notebook.data.values()))


@input_error
def edit_note(args: list[str], notebook: Notebook):
    if len(args) < 2:
        raise IndexError
    title = args[0]
    new_text = " ".join(args[1:])
    note = notebook.find(title)
    if note is None:
        raise ValueError(f"Note '{title}' does not exist.")
    note.edit_text(new_text)
    return f"[green]Note '{title}' updated.[/green]"


@input_error
def delete_note(args: list[str], notebook: Notebook):
    title = args[0]
    notebook.delete(title)
    return f"[green]Note '{title}' deleted.[/green]"


@input_error
def search_notes(args: list[str], notebook: Notebook):
    query = " ".join(args)
    if not query:
        raise IndexError
    matches = notebook.search(query)
    if not matches:
        return f"No notes found matching '{query}'."
    return _notes_table(f"Notes Matching: '{query}'", matches)


@input_error
def add_tag(args: list[str], notebook: Notebook):
    title, tag, *_ = args
    note = notebook.find(title)
    if note is None:
        raise ValueError(f"Note '{title}' does not exist.")
    note.add_tag(tag)
    return f"[green]Tag '#{tag.lstrip('#').lower()}' added to '{title}'.[/green]"


@input_error
def remove_tag(args: list[str], notebook: Notebook):
    title, tag, *_ = args
    note = notebook.find(title)
    if note is None:
        raise ValueError(f"Note '{title}' does not exist.")
    note.remove_tag(tag)
    return f"[green]Tag removed from '{title}'.[/green]"


@input_error
def search_by_tag(args: list[str], notebook: Notebook):
    tag = args[0]
    matches = notebook.search_by_tag(tag)
    if not matches:
        return f"No notes found with tag '#{tag.lstrip('#').lower()}'."
    return _notes_table(f"Notes with Tag #{tag.lstrip('#').lower()}", matches)


@input_error
def sort_notes_by_tags(notebook: Notebook):
    sorted_notes = notebook.sort_by_tags()
    if not sorted_notes:
        return "Notebook is empty."
    return _notes_table("Notes Sorted by Tags", sorted_notes)


def show_help():
    rows = [
        ("Contacts", f"{Command.ADD.value} <name> <phone>", "Add contact or new phone"),
        ("Contacts", f"{Command.CHANGE.value} <name> <old> <new>", "Change contact's phone"),
        ("Contacts", f"{Command.REMOVE_PHONE.value} <name> <phone>", "Remove phone from contact"),
        ("Contacts", f"{Command.PHONE.value} <name>", "Show contact's phones"),
        ("Contacts", Command.ALL.value, "Show all contacts"),
        ("Contacts", f"{Command.SEARCH.value} <query>", "Search contacts by any field"),
        ("Contacts", f"{Command.ADD_EMAIL.value} <name> <email>", "Set contact's email"),
        ("Contacts", f"{Command.ADD_ADDRESS.value} <name> <address>", "Set contact's address"),
        ("Contacts", f"{Command.ADD_BIRTHDAY.value} <name> <DD.MM.YYYY>", "Set contact's birthday"),
        ("Contacts", f"{Command.SHOW_BIRTHDAY.value} <name>", "Show contact's birthday"),
        ("Contacts", f"{Command.BIRTHDAYS.value} [days]", "Upcoming birthdays (default: 7 days)"),
        ("Contacts", f"{Command.RENAME.value} <old_name> <new_name>", "Rename contact"),
        ("Contacts", f"{Command.DELETE.value} <name>", "Delete contact"),
        ("Notes", f"{Command.ADD_NOTE.value} <title> <text>", "Create a new note"),
        ("Notes", Command.ALL_NOTES.value, "Show all notes"),
        ("Notes", f"{Command.EDIT_NOTE.value} <title> <new_text>", "Edit note text"),
        ("Notes", f"{Command.DELETE_NOTE.value} <title>", "Delete a note"),
        ("Notes", f"{Command.SEARCH_NOTE.value} <query>", "Search notes by text/title/tag"),
        ("Notes", f"{Command.ADD_TAG.value} <title> <tag>", "Add tag to a note"),
        ("Notes", f"{Command.REMOVE_TAG.value} <title> <tag>", "Remove tag from a note"),
        ("Notes", f"{Command.SEARCH_TAG.value} <tag>", "Find notes by tag"),
        ("Notes", Command.SORT_TAGS.value, "Show notes sorted by tags"),
        ("General", Command.HELLO.value, "Greet the assistant"),
        ("General", Command.HELP.value, "Show this help table"),
        ("General", f"{Command.CLOSE.value} / {Command.EXIT.value}", "Save data and exit"),
    ]
    return build_table(
        title="Assistant Commands",
        columns=("Category", "Command", "Description"),
        rows=rows,
    )
