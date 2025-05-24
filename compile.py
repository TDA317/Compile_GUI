// created using ChatGPT by TDA317
// https://github.com/TDA317/Compile_GUI/

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import subprocess
import os

class QuakeMapCompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quake Map Compiler")

        # Load previous settings if they exist
        self.settings = self.load_settings()

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10)

        # Create tabs
        self.create_qbsp_tab()
        self.create_vis_tab()
        self.create_light_tab()
        
        # Compile button
        self.compile_button = tk.Button(self.root, text="Compile", command=self.compile_maps)
        self.compile_button.pack(pady=20)

        # Save settings button
        self.save_button = tk.Button(self.root, text="Save Settings", command=self.save_settings)
        self.save_button.pack(pady=5)

        # Load settings button
        self.load_button = tk.Button(self.root, text="Load Settings", command=self.load_settings_dialog)
        self.load_button.pack(pady=5)

    def create_qbsp_tab(self):
        self.qbsp_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.qbsp_tab, text="QBSP")

        # Path for QBSP
        self.qbsp_path_var = tk.StringVar(value=self.settings.get('qbsp_path', ''))
        self.qbsp_path_label = tk.Label(self.qbsp_tab, text="QBSP Path:")
        self.qbsp_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.qbsp_path_entry = tk.Entry(self.qbsp_tab, textvariable=self.qbsp_path_var, width=50)
        self.qbsp_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.qbsp_path_button = tk.Button(self.qbsp_tab, text="Browse", command=self.browse_qbsp)
        self.qbsp_path_button.grid(row=0, column=2, padx=5, pady=5)

        # Input and Output files
        self.input_file_var = tk.StringVar(value=self.settings.get('input_file', ''))
        self.input_file_label = tk.Label(self.qbsp_tab, text="Input File:")
        self.input_file_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.input_file_entry = tk.Entry(self.qbsp_tab, textvariable=self.input_file_var, width=50)
        self.input_file_entry.grid(row=1, column=1, padx=5, pady=5)
        self.input_file_button = tk.Button(self.qbsp_tab, text="Browse", command=self.browse_input)
        self.input_file_button.grid(row=1, column=2, padx=5, pady=5)

        # Output Path
        self.output_path_var = tk.StringVar(value=self.settings.get('output_path', ''))
        self.output_path_label = tk.Label(self.qbsp_tab, text="Output Directory:")
        self.output_path_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.output_path_entry = tk.Entry(self.qbsp_tab, textvariable=self.output_path_var, width=50)
        self.output_path_entry.grid(row=2, column=1, padx=5, pady=5)
        self.output_path_button = tk.Button(self.qbsp_tab, text="Browse", command=self.browse_output)
        self.output_path_button.grid(row=2, column=2, padx=5, pady=5)

        # QBSP Flags
        self.qbsp_flags = {
            "-nofill": tk.BooleanVar(),
            "-noclip": tk.BooleanVar(),
            "-noskip": tk.BooleanVar(),
            "-onlyents": tk.BooleanVar(),
            "-verbose": tk.BooleanVar(),
            "-noverbose": tk.BooleanVar(),
            "-splitspecial": tk.BooleanVar(),
            "-transwater": tk.BooleanVar(),
            "-notranswater": tk.BooleanVar(),
            "-transsky": tk.BooleanVar(),
            "-nooldaxis": tk.BooleanVar(),
            "-forcegoodtree": tk.BooleanVar(),
            "-bspleak": tk.BooleanVar(),
            "-oldleak": tk.BooleanVar(),
            "-leaktest": tk.BooleanVar(),
            "-nopercent": tk.BooleanVar(),
            "-bsp2": tk.BooleanVar(),
            "-2psb": tk.BooleanVar(),
            "-wadpath": tk.StringVar(value=self.settings.get('wadpath', '')),
        }

        # Create flag checkboxes and input fields
        self.create_flag_checkboxes(self.qbsp_tab, self.qbsp_flags, 4)

        # Wadpath field
        self.wadpath_label = tk.Label(self.qbsp_tab, text="-wadpath:")
        self.wadpath_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.wadpath_entry = tk.Entry(self.qbsp_tab, textvariable=self.qbsp_flags['-wadpath'], width=50)
        self.wadpath_entry.grid(row=3, column=1, padx=5, pady=5)
        self.wadpath_button = tk.Button(self.qbsp_tab, text="Browse", command=self.browse_wadpath)
        self.wadpath_button.grid(row=3, column=2, padx=5, pady=5)

    def create_vis_tab(self):
        self.vis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.vis_tab, text="VIS")

        # Path for VIS
        self.vis_path_var = tk.StringVar(value=self.settings.get('vis_path', ''))
        self.vis_path_label = tk.Label(self.vis_tab, text="VIS Path:")
        self.vis_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.vis_path_entry = tk.Entry(self.vis_tab, textvariable=self.vis_path_var, width=50)
        self.vis_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.vis_path_button = tk.Button(self.vis_tab, text="Browse", command=self.browse_vis)
        self.vis_path_button.grid(row=0, column=2, padx=5, pady=5)

        # VIS Flags
        self.vis_flags = {
            "-threads": tk.IntVar(),
            "-fast": tk.BooleanVar(),
            "-level": tk.IntVar(),
            "-v": tk.BooleanVar(),
            "-vv": tk.BooleanVar(),
            "-noambientsky": tk.BooleanVar(),
            "-noambientwater": tk.BooleanVar(),
            "-noambientslime": tk.BooleanVar(),
            "-noambientlava": tk.BooleanVar(),
            "-noambient": tk.BooleanVar(),
        }

        # Create flag checkboxes
        self.create_flag_checkboxes(self.vis_tab, self.vis_flags, 1)

    def create_light_tab(self):
        self.light_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.light_tab, text="LIGHT")

        # Path for LIGHT
        self.light_path_var = tk.StringVar(value=self.settings.get('light_path', ''))
        self.light_path_label = tk.Label(self.light_tab, text="LIGHT Path:")
        self.light_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.light_path_entry = tk.Entry(self.light_tab, textvariable=self.light_path_var, width=50)
        self.light_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.light_path_button = tk.Button(self.light_tab, text="Browse", command=self.browse_light)
        self.light_path_button.grid(row=0, column=2, padx=5, pady=5)

        # LIGHT Flags
        self.light_flags = {
            "-threads": tk.IntVar(),
            "-extra": tk.BooleanVar(),
            "-extra4": tk.BooleanVar(),
            "-gate": tk.DoubleVar(),
            "-sunsamples": tk.IntVar(),
            "-surflight_subdivide": tk.IntVar(),
            "-lit": tk.BooleanVar(),
            "-onlyents": tk.BooleanVar(),
            "-soft": tk.IntVar(),
            "-dirtdebug": tk.BooleanVar(),
            "-phongdebug": tk.BooleanVar(),
            "-bouncedebug": tk.BooleanVar(),
            "-surflight_dump": tk.BooleanVar(),
            "-novisapprox": tk.BooleanVar(),
            "-addmin": tk.BooleanVar(),
            "-lit2": tk.BooleanVar(),
            "-lux": tk.BooleanVar(),
            "-lmscale": tk.DoubleVar(),
            "-bspxlit": tk.BooleanVar(),
            "-bspx": tk.BooleanVar(),
            "-novanilla": tk.BooleanVar(),
        }

        # Create flag checkboxes
        self.create_flag_checkboxes(self.light_tab, self.light_flags, 1)

    def create_flag_checkboxes(self, parent, flags, start_row):
        col_count = 3
        row = start_row
        col = 0

        for flag, var in flags.items():
            checkbox = tk.Checkbutton(parent, text=flag, variable=var)
            checkbox.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            if isinstance(var, (tk.IntVar, tk.DoubleVar)):
                entry = tk.Entry(parent, textvariable=var, width=5)
                entry.grid(row=row, column=col + 1, padx=5, pady=5)
            if col == col_count - 1:
                col = 0
                row += 1
            else:
                col += 1

    def browse_qbsp(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.qbsp_path_var.set(file_path)

    def browse_vis(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.vis_path_var.set(file_path)

    def browse_light(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.light_path_var.set(file_path)

    def browse_wadpath(self):
        directory = filedialog.askdirectory()
        if directory:
            self.qbsp_flags['-wadpath'].set(directory)

    def browse_input(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_file_var.set(file_path)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path_var.set(directory)

    def compile_maps(self):
        input_map = self.input_file_var.get()  # Get the actual file path for input
        output_path = self.output_path_var.get()  # Get the directory for output

        # Compile QBSP
        qbsp_cmd = [self.qbsp_path_var.get(), input_map, os.path.join(output_path, os.path.basename(input_map))]
        self.run_command(qbsp_cmd)

        # Compile VIS
        vis_cmd = [self.vis_path_var.get(), os.path.join(output_path, os.path.basename(input_map))]
        self.run_command(vis_cmd)

        # Compile LIGHT
        light_cmd = [self.light_path_var.get(), os.path.join(output_path, os.path.basename(input_map))]
        self.run_command(light_cmd)

        messagebox.showinfo("Success", "Compilation completed successfully.")

    def run_command(self, command):
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Command failed: {e}")

    def save_settings(self):
        settings = {
            'qbsp_path': self.qbsp_path_var.get(),
            'vis_path': self.vis_path_var.get(),
            'light_path': self.light_path_var.get(),
            'input_file': self.input_file_var.get(),
            'output_path': self.output_path_var.get(),
            'wadpath': self.qbsp_flags['-wadpath'].get(),
        }
        settings_file = "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", 'r') as f:
                return json.load(f)
        return {}

    def load_settings_dialog(self):
        settings = self.load_settings()
        if settings:
            self.qbsp_path_var.set(settings.get('qbsp_path', ''))
            self.vis_path_var.set(settings.get('vis_path', ''))
            self.light_path_var.set(settings.get('light_path', ''))
            self.input_file_var.set(settings.get('input_file', ''))
            self.output_path_var.set(settings.get('output_path', ''))
            self.qbsp_flags['-wadpath'].set(settings.get('wadpath', ''))

if __name__ == "__main__":
    root = tk.Tk()
    app = QuakeMapCompilerApp(root)
    root.mainloop()
