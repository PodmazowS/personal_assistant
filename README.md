# personal_assistant

PROJECT STRUCTURE

main.py — entry point, main application loop, and command routing
README.md — setup instructions, usage guide, and list of available commands
.gitignore — exclusion of virtual environments, cache, and local data files from Git

models/fields.py — base Field class inherited by all data fields
models/contacts.py — Name, Phone, Email, Address, Birthday, Record, and AddressBook classes (CRUD, search, validation, upcoming birthdays)
models/notes.py — Tag, Note, and Notebook classes (CRUD, search, and tag sorting)

cli/parser.py — user input parser splitting raw text into a command and arguments
cli/handlers.py — CLI command handler functions and console output formatting
cli/matcher.py — command suggestion logic for mistyped commands

services/storage.py — data persistence (saving and loading data to/from disk)

utils/exceptions.py — custom exceptions and @input_error decorator for CLI error handling
