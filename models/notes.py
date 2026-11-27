from collections import UserDict
from collections.abc import Iterable

from .fields import Field


class Tag(Field):
    #A normalized, non-empty note tag.

    def __init__(self, value: str):
        cleaned = str(value).strip().lstrip("#").casefold()
        if not cleaned:
            raise ValueError("Tag cannot be empty.")
        super().__init__(cleaned)


class Note:
    #A text note with a title, body text, and optional tags.

    def __init__(self, title: str, text: str, tags: Iterable[str] = ()):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Note title is required.")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Note text cannot be empty.")

        self.title = title.strip()
        self.text = text.strip()
        self.tags: list[Tag] = []
        for tag in tags:
            self.add_tag(tag)

    def edit_text(self, new_text: str):
        if not isinstance(new_text, str) or not new_text.strip():
            raise ValueError("Note text cannot be empty.")
        self.text = new_text.strip()

    def add_tag(self, tag: str):
        new_tag = Tag(tag)
        if any(existing.value == new_tag.value for existing in self.tags):
            return
        self.tags.append(new_tag)

    def remove_tag(self, tag: str):
        target = Tag(tag).value
        for existing in self.tags:
            if existing.value == target:
                self.tags.remove(existing)
                return
        raise ValueError(f"Tag '{target}' not found on this note.")

    def __str__(self):
        tags_str = ", ".join(f"#{t.value}" for t in self.tags) if self.tags else "no tags"
        return f"[{self.title}] ({tags_str})\n  {self.text}"


class Notebook(UserDict[str, Note]):
    #Store notes by their title.

    def add_note(self, note: Note):
        if note.title in self.data:
            raise ValueError(f"Note '{note.title}' already exists.")
        self.data[note.title] = note

    def find(self, title: str):
        return self.data.get(title.strip())

    def delete(self, title: str):
        key = title.strip()
        if key not in self.data:
            raise ValueError(f"Note '{key}' does not exist.")
        del self.data[key]

    def search(self, query: str):
        #Search notes by substring in title, text, or tags.
        q = query.strip().casefold()
        if not q:
            return []
        results: list[Note] = []
        for note in self.data.values():
            in_title = q in note.title.casefold()
            in_text = q in note.text.casefold()
            in_tags = any(q in tag.value for tag in note.tags)
            if in_title or in_text or in_tags:
                results.append(note)
        return results

    def search_by_tag(self, tag: str):
        target = Tag(tag).value
        return [
            note
            for note in self.data.values()
            if any(existing.value == target for existing in note.tags)
        ]

    def sort_by_tags(self):
        #Return notes sorted alphabetically by their first tag (untagged last).
        return sorted(
            self.data.values(),
            key=lambda n: (len(n.tags) == 0, n.tags[0].value if n.tags else "", n.title.casefold()),
        )
