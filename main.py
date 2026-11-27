from cli.handlers import (
    ALL_COMMANDS,
    Command,
    EXIT_COMMANDS,
    add_contact,
    add_note,
    add_tag,
    birthdays,
    change_phone,
    delete_contact,
    delete_note,
    edit_note,
    remove_phone,
    remove_tag,
    rename_contact,
    search_by_tag,
    search_contacts,
    search_notes,
    set_address,
    set_birthday,
    set_email,
    show_all_contacts,
    show_all_notes,
    show_birthday,
    show_help,
    show_phone,
    sort_notes_by_tags,
)
from cli.matcher import suggest_commands
from cli.output import console, display
from cli.parser import parse_input
from services.storage import load_data, save_data


def main():
    book, notebook = load_data()

    commands = {
        Command.HELLO: lambda args: "How can I help you?",
        Command.HELP: lambda args: show_help(),
        Command.ADD: lambda args: add_contact(args, book),
        Command.CHANGE: lambda args: change_phone(args, book),
        Command.REMOVE_PHONE: lambda args: remove_phone(args, book),
        Command.PHONE: lambda args: show_phone(args, book),
        Command.ALL: lambda args: show_all_contacts(book),
        Command.SEARCH: lambda args: search_contacts(args, book),
        Command.ADD_EMAIL: lambda args: set_email(args, book),
        Command.ADD_ADDRESS: lambda args: set_address(args, book),
        Command.ADD_BIRTHDAY: lambda args: set_birthday(args, book),
        Command.SHOW_BIRTHDAY: lambda args: show_birthday(args, book),
        Command.BIRTHDAYS: lambda args: birthdays(args, book),
        Command.RENAME: lambda args: rename_contact(args, book),
        Command.DELETE: lambda args: delete_contact(args, book),
        Command.ADD_NOTE: lambda args: add_note(args, notebook),
        Command.ALL_NOTES: lambda args: show_all_notes(notebook),
        Command.EDIT_NOTE: lambda args: edit_note(args, notebook),
        Command.DELETE_NOTE: lambda args: delete_note(args, notebook),
        Command.SEARCH_NOTE: lambda args: search_notes(args, notebook),
        Command.ADD_TAG: lambda args: add_tag(args, notebook),
        Command.REMOVE_TAG: lambda args: remove_tag(args, notebook),
        Command.SEARCH_TAG: lambda args: search_by_tag(args, notebook),
        Command.SORT_TAGS: lambda args: sort_notes_by_tags(notebook),
    }

    
    display(
        f"[bold cyan]Welcome to the assistant bot![/bold cyan] "
        f"You can type '[bold]{Command.HELP.value}[/bold]' to see available commands."
    )

    try:
        while True:
            user_input = console.input("[bold green]Enter a command:[/bold green] ")
            command, *args = parse_input(user_input)

            if not command:
                continue

            if command in EXIT_COMMANDS:
                display("[bold cyan]Good bye![/bold cyan]")
                break

            handler = commands.get(command)
            if handler is not None:
                display(handler(args))
            else:
                suggestions = suggest_commands(command, ALL_COMMANDS)
                if suggestions:
                    display(
                        f"[yellow]Invalid command.[/yellow] Did you mean: "
                        f"[bold]{', '.join(suggestions)}[/bold]?"
                    )
                else:
                    display(
                        f"[yellow]Invalid command.[/yellow] Type "
                        f"'[bold]{Command.HELP.value}[/bold]' for a list of commands."
                    )
    except (KeyboardInterrupt, EOFError):
        display("\n[bold cyan]Good bye![/bold cyan]")
    finally:
        #In any case saves the data
        save_data(book, notebook)


if __name__ == "__main__":
    main()
