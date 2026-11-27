from pathlib import Path
import pickle

from models.contacts import AddressBook
from models.notes import Notebook

DEFAULT_STORAGE_PATH = Path("assistant_data.pkl")


def save_data(book: AddressBook, notebook: Notebook, filepath: Path | str = DEFAULT_STORAGE_PATH):
    #Persist AddressBook and Notebook to disk.
    path = Path(filepath)
    with path.open("wb") as file:
        pickle.dump((book, notebook), file)


def load_data(filepath: Path | str = DEFAULT_STORAGE_PATH):
    #Load AddressBook and Notebook from disk
    path = Path(filepath)
    if not path.exists():
        return AddressBook(), Notebook()

    try:
        with path.open("rb") as file:
            data = pickle.load(file)
            if isinstance(data, tuple) and len(data) == 2:
                book, notebook = data
                if isinstance(book, AddressBook) and isinstance(notebook, Notebook):
                    return book, notebook
    except (OSError, pickle.PickleError, EOFError):
        pass

    return AddressBook(), Notebook()
