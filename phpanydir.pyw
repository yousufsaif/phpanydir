import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterweb import HtmlFrame  # Import HtmlFrame
import os
import webbrowser
import subprocess
import json


def find_php_exe():
    try:
        result = subprocess.check_output('where php.exe', shell=True).decode('utf-8').strip()
        return result
    except subprocess.CalledProcessError:
        return None


class phpanydir(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('phpanydir (1.0.0)')
        self.geometry('450x190')  # Original window size

        self.settings_file = 'settings.json'
        self.load_settings()

        self.process = None

        tk.Label(self, text='Locate PHP interpreter').grid(row=0, column=0, padx=10, pady=10)
        self.php_path_entry = tk.Entry(self, textvariable=self.php_path_var, width=30)
        self.php_path_entry.grid(row=0, column=1, padx=10, pady=10)
        self.browse_btn = tk.Button(self, text='Browse', command=self.browse_php)
        self.browse_btn.grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self, text='Port Number').grid(row=1, column=0, padx=10, pady=10)
        self.port_entry = tk.Entry(self, textvariable=self.port_var, width=30)
        self.port_entry.grid(row=1, column=1, padx=10, pady=10)

        self.all_ports_check = tk.Checkbutton(self, text='Listen to traffic from all ports', variable=self.all_ports_var)
        self.all_ports_check.grid(row=2, column=1, padx=10, pady=10)

        self.start_btn = tk.Button(self, text='Start', command=self.toggle_server)
        self.start_btn.grid(row=4, column=1, padx=10, pady=20)

        self.status_label = tk.Label(self, text='Status: Stopped', fg='red')
        self.status_label.grid(row=4, column=2, padx=10, pady=20)

        self.about_link = tk.Label(self, text='About', fg='blue', cursor='hand2')
        self.about_link.grid(row=4, column=0, padx=10, pady=10)
        self.about_link.bind('<Button-1>', self.open_about_link)

        # Adjust window position
        self.center_window()

        # Create a separate window for the web view
        self.create_web_view_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_web_view_window(self):
        web_view_window = tk.Toplevel(self)
        web_view_window.title("phpanydir")
        web_view_window.geometry("200x190")  # Adjust size as needed

        # Position the web view window next to the main window
        x = self.winfo_x() + self.winfo_width()
        y = self.winfo_y()
        web_view_window.geometry(f"+{x}+{y}")

        # Create a web view (HtmlFrame) in the new window
        web_view = HtmlFrame(web_view_window, horizontal_scrollbar="auto")
        web_view.pack(expand=True, fill="both")
        web_view.load_website("https://yousufsaif.github.io/blog/more.html")

    def browse_php(self):
        file_path = filedialog.askopenfilename()
        self.php_path_var.set(file_path)

    def toggle_server(self):
        if self.start_btn['text'] == 'Start':
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        php_path = self.php_path_var.get()
        port = self.port_var.get()

        if not php_path or not port:
            messagebox.showerror('Error', 'Please fill all mandatory fields')
            return

        command = [php_path, '-S']
        if self.all_ports_var.get():
            command.append('0.0.0.0:' + port)
        else:
            command.append('localhost:' + port)

        try:
            self.process = subprocess.Popen(command)
            webbrowser.open('http://localhost:' + port)
            self.save_settings()
            self.start_btn.config(text='Stop')
            self.status_label.config(text='Status: Running', fg='green')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def stop_server(self):
        if self.process:
            self.process.terminate()
            self.process = None
        self.start_btn.config(text='Start')
        self.status_label.config(text='Status: Stopped', fg='red')
        self.destroy()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
            self.php_path_var = tk.StringVar(value=settings.get('php_path', 'C:/xampp/php/php.exe'))
            self.port_var = tk.StringVar(value=settings.get('port', '4000'))
            self.all_ports_var = tk.BooleanVar(value=settings.get('all_ports', False))

        else:
            self.php_path_var = tk.StringVar(value='C:/xampp/php/php.exe')
            self.port_var = tk.StringVar(value='4000')
            self.all_ports_var = tk.BooleanVar()

    def save_settings(self):
        settings = {
            'php_path': self.php_path_var.get(),
            'port': self.port_var.get(),
            'all_ports': self.all_ports_var.get(),
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def open_about_link(self, event):
        webbrowser.open('https://github.com/yousufsaif/phpanydir')


if __name__ == '__main__':
    app = phpanydir()
    app.mainloop()
