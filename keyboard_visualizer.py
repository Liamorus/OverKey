import tkinter as tk

# Layout of keys in rows
KEY_ROWS = [
    list('qwertyuiop'),
    list('asdfghjkl'),
    list('zxcvbnm')
]

class KeyboardVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Keyboard Visualizer')
        self.buttons = {}
        self._create_keys()
        self.bind('<KeyPress>', self.on_key_press)
        self.bind('<KeyRelease>', self.on_key_release)
        self.focus_set()

    def _create_keys(self):
        for r, row_keys in enumerate(KEY_ROWS):
            for c, key in enumerate(row_keys):
                btn = tk.Label(self, text=key.upper(), width=4, height=2, relief='raised', bg='lightgray')
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[key] = btn

    def on_key_press(self, event):
        key = event.char.lower()
        btn = self.buttons.get(key)
        if btn:
            btn.config(bg='yellow')

    def on_key_release(self, event):
        key = event.char.lower()
        btn = self.buttons.get(key)
        if btn:
            btn.config(bg='lightgray')

if __name__ == '__main__':
    app = KeyboardVisualizer()
    app.mainloop()
