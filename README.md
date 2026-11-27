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

---

**all** command output:
<img width="1280" height="230" alt="telegram-cloud-photo-size-2-5208826746663280798-y" src="https://github.com/user-attachments/assets/8be01aa7-f475-48c4-9268-91aa08216e6b" />

**all-notes** command output:
<img width="1280" height="181" alt="telegram-cloud-photo-size-2-5208826746663280790-y" src="https://github.com/user-attachments/assets/723965f3-1c45-4121-8014-f1386a0e23a1" />

**help** command:
<img width="1280" height="760" alt="telegram-cloud-photo-size-2-5208826746663280791-y" src="https://github.com/user-attachments/assets/6d1f1eba-f61e-4be8-87d1-7cf1a2fdcf95" />

**matcher feature**:
<img width="1412" height="76" alt="telegram-cloud-document-2-5208826746203320558" src="https://github.com/user-attachments/assets/5f8cb3a6-6c0c-42e6-9b0e-aeb6c5da2c4c" />


