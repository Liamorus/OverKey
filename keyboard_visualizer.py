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
        # Remove window decorations so only the key overlay is visible
        self.overrideredirect(True)
        # Set transparent background and make the window topmost
        transparent_color = 'magenta'
        self.configure(bg=transparent_color)
        self.attributes('-transparentcolor', transparent_color)
        self.attributes('-topmost', True)

        self.title('Keyboard Visualizer')

        self.buttons = {}

        # Frame to hold all key labels so we can easily place the drag handle
        self.keys_frame = tk.Frame(self, bg=self['bg'])
        self.keys_frame.grid(row=0, column=0)

        self._create_keys()
        self.bind('<KeyPress>', self.on_key_press)
        self.bind('<KeyRelease>', self.on_key_release)
        self.bind('<Button-3>', self.show_context_menu)
        self.focus_set()

        # Create a small handle label to drag the overlay around
        self.drag_handle = tk.Label(self, text='☰', bg='gray', fg='white', width=2)
        self.drag_handle.grid(row=1, column=0, sticky='e', pady=(2, 0))
        self.drag_handle.bind('<ButtonPress-1>', self.start_move)
        self.drag_handle.bind('<B1-Motion>', self.do_move)

        # Button to toggle ability to move individual keys
        self.locked = True
        self.lock_button = tk.Label(self, text='🔒', bg='gray', fg='white', width=2)
        self.lock_button.grid(row=1, column=0, sticky='w', pady=(2, 0))
        self.lock_button.bind('<Button-1>', self.toggle_lock)

        # Track drag state for keys when unlocked
        self._active_key = None

        self._create_context_menu()

    def toggle_lock(self, event=None):
        """Toggle the ability to move individual key squares."""
        self.locked = not self.locked
        self.lock_button.config(text='🔒' if self.locked else '🔓')
        if self.locked:
            self._disable_key_drag()
        else:
            self._enable_key_drag()

    def _create_keys(self):
        for r, row_keys in enumerate(KEY_ROWS):
            for c, key in enumerate(row_keys):
                btn = tk.Label(
                    self.keys_frame,
                    text=key.upper(),
                    width=4,
                    height=2,
                    relief='raised',
                    bg='lightgray',
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[key] = btn

        # Keep track of layout size for placing keys later
        self.update_idletasks()

    def _create_context_menu(self):
        """Create a simple context menu with an option to close the app."""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label='Schließen', command=self.destroy)

    def start_move(self, event):
        """Record the start position for dragging."""
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def do_move(self, event):
        """Move the window based on pointer movement."""
        dx = event.x_root - self._drag_start_x
        dy = event.y_root - self._drag_start_y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.geometry(f'+{x}+{y}')
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def show_context_menu(self, event):
        """Display the context menu on right-click."""
        self.context_menu.tk_popup(event.x_root, event.y_root)
        self.context_menu.grab_release()

    def _enable_key_drag(self):
        """Allow dragging individual keys to reposition them."""
        for btn in self.buttons.values():
            # If using grid, convert to place at current position
            if btn.winfo_manager() == 'grid':
                x = btn.winfo_x()
                y = btn.winfo_y()
                btn.grid_forget()
                btn.place(in_=self.keys_frame, x=x, y=y)

            btn.bind('<ButtonPress-1>', self.start_key_move)
            btn.bind('<B1-Motion>', self.do_key_move)

    def _disable_key_drag(self):
        """Stop dragging of individual keys."""
        for btn in self.buttons.values():
            btn.unbind('<ButtonPress-1>')
            btn.unbind('<B1-Motion>')

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

    def start_key_move(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def do_key_move(self, event):
        widget = event.widget
        dx = event.x - widget._drag_start_x
        dy = event.y - widget._drag_start_y
        x = widget.winfo_x() + dx
        y = widget.winfo_y() + dy
        widget.place_configure(x=x, y=y)

if __name__ == '__main__':
    app = KeyboardVisualizer()
    app.mainloop()
