from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
import json, os

class NoteApp(BoxLayout):
    editor = ObjectProperty(None)
    list_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_btn = None
        self.load_notes()

    def new_note(self):
        self.editor.text = ""
        self.selected_btn = None

    def save_note(self):
        text = self.editor.text.strip()
        if not text:
            return
        if self.selected_btn:
            self.selected_btn.text = text[:20] + ("..." if len(text) > 20 else "")
            self.selected_btn.full_text = text
        else:
            btn = Button(text=text[:20] + ("..." if len(text) > 20 else ""),
                         size_hint_y=None, height=50)
            btn.full_text = text
            btn.bind(on_press=self.select_note)
            self.list_layout.add_widget(btn)
        self.save_to_file()

    def select_note(self, btn):
        self.selected_btn = btn
        self.editor.text = btn.full_text

    def delete_note(self):
        if self.selected_btn:
            self.list_layout.remove_widget(self.selected_btn)
            self.selected_btn = None
            self.editor.text = ""
            self.save_to_file()

    def save_to_file(self):
        notes = [w.full_text for w in self.list_layout.children if hasattr(w, 'full_text')]
        with open("notes.json", "w") as f:
            json.dump(notes, f)

    def load_notes(self):
        if not os.path.exists("notes.json"):
            return
        with open("notes.json") as f:
            notes = json.load(f)
        for n in notes:
            btn = Button(text=n[:20] + ("..." if len(n) > 20 else ""),
                         size_hint_y=None, height=50)
            btn.full_text = n
            btn.bind(on_press=self.select_note)
            self.list_layout.add_widget(btn)

class NoteAppMain(App):
    def build(self):
        return NoteApp()

if __name__ == "__main__":
    NoteAppMain().run()