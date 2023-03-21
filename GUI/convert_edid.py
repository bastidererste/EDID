import re
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class EDIDConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('EDID Converter')
        self.geometry('300x100')

        self.input_file = None
        self.output_file = None

        self.select_file_button = tk.Button(self, text='Select File', command=self.select_file)
        self.select_file_button.pack(pady=5)

        self.save_to_button = tk.Button(self, text='Save to', state='disabled', command=self.save_to)
        self.save_to_button.pack(pady=5)

        self.convert_button = tk.Button(self, text='Convert', state='disabled', command=self.convert_edid)
        self.convert_button.pack(pady=5)

    def select_file(self):
        self.input_file = filedialog.askopenfilename(title='Select the input file')
        if self.input_file:
            self.save_to_button.config(state='normal')

    def save_to(self):
        if self.input_file:
            input_base_name = os.path.splitext(os.path.basename(self.input_file))[0]
            self.output_file = filedialog.asksaveasfilename(defaultextension='.bin', initialfile=input_base_name + '.bin', filetypes=[('Binary files', '*.bin')], title='Save to')
            if self.output_file:
                self.convert_button.config(state='normal')

    def convert_edid(self):
        if self.input_file and self.output_file:
            pattern = re.compile(r'^([a-f0-9]{32}|[a-f0-9 ]{47})$')

            with open(self.input_file, 'r') as infile, open(self.output_file, 'wb') as outfile:
                for line in infile:
                    if pattern.match(line.strip()):
                        hex_string = line.replace(' ', '').strip()
                        binary_data = bytes.fromhex(hex_string)
                        outfile.write(binary_data)

            self.input_file = None
            self.output_file = None
            self.save_to_button.config(state='disabled')
            self.convert_button.config(state='disabled')
            
            messagebox.showinfo("Success", "Conversion complete!")

if __name__ == '__main__':
    app = EDIDConverterApp()
    app.mainloop()
