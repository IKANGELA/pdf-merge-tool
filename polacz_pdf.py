from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pypdf import PdfWriter


def get_default_folders():
    base_dir = Path.home() / "Documents" / "PDF Merge Tool"
    source_dir = base_dir / "Input"
    target_dir = base_dir / "Output"
    source_dir.mkdir(parents=True, exist_ok=True)
    target_dir.mkdir(parents=True, exist_ok=True)
    return source_dir, target_dir


def find_pdf_files(folder: Path, sort_by_name: bool = True):
    if not folder.exists() or not folder.is_dir():
        return []
    pdf_files = list(folder.glob("*.pdf"))
    if sort_by_name:
        pdf_files.sort(key=lambda p: p.name.lower())
    return pdf_files


def normalize_output_name(output_name: str):
    output_name = output_name.strip()
    if not output_name:
        output_name = "polaczone.pdf"
    if not output_name.lower().endswith(".pdf"):
        output_name += ".pdf"
    return output_name


def merge_pdfs(source_dir: Path, target_dir: Path, output_name: str, selected_files=None, sort_by_name: bool = True):
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)

    if not source_dir.exists() or not source_dir.is_dir():
        return False, "Nie wybrano poprawnego folderu źródłowego."

    if not target_dir.exists() or not target_dir.is_dir():
        return False, "Nie wybrano poprawnego folderu docelowego."

    if selected_files:
        pdf_files = []
        for file_path in selected_files:
            file_path = Path(file_path)
            if file_path.exists() and file_path.is_file() and file_path.suffix.lower() == ".pdf":
                pdf_files.append(file_path)
        if sort_by_name:
            pdf_files.sort(key=lambda p: p.name.lower())
    else:
        pdf_files = find_pdf_files(source_dir, sort_by_name=sort_by_name)

    if not pdf_files:
        return False, "Nie znaleziono żadnych plików PDF do połączenia."

    output_name = normalize_output_name(output_name)
    output_path = target_dir / output_name
    writer = PdfWriter()

    try:
        for pdf_file in pdf_files:
            writer.append(str(pdf_file))
    except Exception as exc:
        return False, f"Błąd podczas dodawania pliku PDF: {exc}"

    try:
        with output_path.open("wb") as file_out:
            writer.write(file_out)
    except Exception as exc:
        return False, f"Błąd podczas zapisu pliku wynikowego: {exc}"

    return True, f"Gotowe. Połączono {len(pdf_files)} plików do: {output_path.name}"


def choose_directory(title: str, initial_dir: Path | None = None):
    if initial_dir is None:
        initial_dir = Path.cwd()
    return Path(filedialog.askdirectory(title=title, initialdir=str(initial_dir))) or None


def choose_pdf_files(initial_dir: Path | None = None):
    if initial_dir is None:
        initial_dir = Path.cwd()
    files = filedialog.askopenfilenames(
        title="Wybierz pliki PDF",
        initialdir=str(initial_dir),
        filetypes=[("Pliki PDF", "*.pdf")]
    )
    return list(files)


def build_gui():
    root = tk.Tk()
    root.title("Łączenie PDF")
    root.geometry("820x450")
    root.resizable(False, False)
    root.configure(bg="#f2eadf")

    style = ttk.Style(root)
    style.theme_use("clam")

    STYLE_BG = "#f2eadf"
    STYLE_PANEL = "#f8f1e8"
    STYLE_TEXT = "#3a2d24"
    STYLE_MUTED = "#6d5548"
    STYLE_FIELD = "#fffaf3"
    STYLE_BORDER = "#d3bba5"
    STYLE_BUTTON = "#8a5d3b"
    STYLE_BUTTON_DARK = "#70472e"
    STYLE_BUTTON_HOVER = "#a56d45"
    STYLE_BUTTON_TEXT = "#ffffff"

    style.configure("TFrame", background=STYLE_BG)
    style.configure("TLabel", background=STYLE_BG, foreground=STYLE_TEXT, font=("Segoe UI", 10))
    style.configure("Header.TLabel", background=STYLE_BG, foreground=STYLE_TEXT, font=("Segoe UI", 17, "bold"))
    style.configure("TEntry", fieldbackground=STYLE_FIELD, foreground=STYLE_TEXT, insertcolor=STYLE_TEXT, borderwidth=1, relief="solid")
    style.map("TEntry", fieldbackground=[("readonly", STYLE_FIELD)])
    style.configure("TCheckbutton", background=STYLE_BG, foreground=STYLE_TEXT, font=("Segoe UI", 10))
    style.map("TCheckbutton", background=[("active", STYLE_BG)])

    style.configure("Brown.TButton", background=STYLE_BUTTON, foreground=STYLE_BUTTON_TEXT, padding=(12, 10), font=("Segoe UI", 10, "bold"))
    style.map("Brown.TButton", background=[("active", STYLE_BUTTON_HOVER), ("pressed", STYLE_BUTTON_DARK)], foreground=[("active", STYLE_BUTTON_TEXT), ("pressed", STYLE_BUTTON_TEXT)])
    style.configure("BrownSoft.TButton", background="#b38867", foreground="#ffffff", padding=(12, 10), font=("Segoe UI", 10))
    style.map("BrownSoft.TButton", background=[("active", "#c49b7a"), ("pressed", "#8a5b38")], foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

    main = ttk.Frame(root, padding=24)
    main.pack(fill="both", expand=True)
    main.configure(style="TFrame")

    header = ttk.Label(main, text="Łączenie PDF", style="Header.TLabel")
    header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 20))

    default_source_dir, default_target_dir = get_default_folders()
    source_var = tk.StringVar(value=str(default_source_dir))
    target_var = tk.StringVar(value=str(default_target_dir))
    output_var = tk.StringVar(value="polaczone.pdf")
    selected_files_var = tk.StringVar(value="Brak wybranych plików — zostaną użyte wszystkie PDF z folderu źródłowego.")
    status_var = tk.StringVar(value="Wybierz folder źródłowy i docelowy.")
    sort_var = tk.BooleanVar(value=True)
    selected_files = []

    def set_source_folder():
        selected = choose_directory("Wybierz folder źródłowy", Path(source_var.get()))
        if selected:
            source_var.set(str(selected))
            selected_files.clear()
            selected_files_var.set("Brak wybranych plików — zostaną użyte wszystkie PDF z folderu źródłowego.")

    def set_target_folder():
        selected = choose_directory("Wybierz folder docelowy", Path(target_var.get()))
        if selected:
            target_var.set(str(selected))

    def select_pdf_files():
        nonlocal selected_files
        files = choose_pdf_files(Path(source_var.get()))
        if files:
            selected_files = list(files)
            selected_files_var.set(f"Wybrano {len(selected_files)} plików PDF.")
        else:
            selected_files = []
            selected_files_var.set("Brak wybranych plików — zostaną użyte wszystkie PDF z folderu źródłowego.")

    def open_output_file():
        output_path = Path(target_var.get()) / normalize_output_name(output_var.get())
        if output_path.exists():
            try:
                output_path.open("rb")
                import os
                os.startfile(str(output_path))
            except Exception as exc:
                messagebox.showerror("Błąd", f"Nie udało się otworzyć pliku: {exc}")
        else:
            messagebox.showwarning("Ostrzeżenie", "Najpierw połącz pliki PDF, aby utworzyć wynikowy plik.")

    def open_target_folder():
        folder = Path(target_var.get())
        if folder.exists():
            import os
            os.startfile(str(folder))
        else:
            messagebox.showwarning("Ostrzeżenie", "Folder docelowy nie istnieje.")

    def on_merge():
        result, message = merge_pdfs(
            source_dir=source_var.get(),
            target_dir=target_var.get(),
            output_name=output_var.get(),
            selected_files=selected_files if selected_files else None,
            sort_by_name=sort_var.get(),
        )
        status_var.set(message)
        if result:
            messagebox.showinfo("Sukces", message)
        else:
            messagebox.showerror("Błąd", message)

    ttk.Label(main, text="Folder źródłowy:").grid(row=1, column=0, sticky="w", pady=(0, 10))
    ttk.Entry(main, textvariable=source_var, width=54).grid(row=1, column=1, padx=(12, 8), sticky="ew")
    ttk.Button(main, text="Wybierz", command=set_source_folder, style="BrownSoft.TButton").grid(row=1, column=2, sticky="ew")

    ttk.Label(main, text="Folder docelowy:").grid(row=2, column=0, sticky="w", pady=(0, 10))
    ttk.Entry(main, textvariable=target_var, width=54).grid(row=2, column=1, padx=(12, 8), sticky="ew")
    ttk.Button(main, text="Wybierz", command=set_target_folder, style="BrownSoft.TButton").grid(row=2, column=2, sticky="ew")

    ttk.Label(main, text="Nazwa pliku:").grid(row=3, column=0, sticky="w", pady=(0, 10))
    ttk.Entry(main, textvariable=output_var, width=54).grid(row=3, column=1, padx=(12, 8), sticky="ew")
    ttk.Checkbutton(main, text="Sortuj wg nazwy", variable=sort_var, onvalue=True, offvalue=False).grid(row=3, column=2, sticky="w")

    ttk.Button(main, text="Wybierz pliki PDF", command=select_pdf_files, style="BrownSoft.TButton").grid(row=4, column=0, columnspan=3, sticky="ew", pady=(12, 8))
    ttk.Label(main, textvariable=selected_files_var, wraplength=760, justify="left").grid(row=5, column=0, columnspan=3, sticky="w", pady=(0, 10))

    ttk.Button(main, text="Połącz PDF", command=on_merge, style="Brown.TButton").grid(row=6, column=0, columnspan=3, sticky="ew", pady=(4, 8))

    action_row = ttk.Frame(main)
    action_row.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(0, 14))
    action_row.columnconfigure(0, weight=1)
    action_row.columnconfigure(1, weight=1)
    ttk.Button(action_row, text="Otwórz wynik PDF", command=open_output_file, style="Brown.TButton").grid(row=0, column=0, sticky="ew", padx=(0, 6))
    ttk.Button(action_row, text="Otwórz folder docelowy", command=open_target_folder, style="Brown.TButton").grid(row=0, column=1, sticky="ew", padx=(6, 0))

    ttk.Button(main, text="Zamknij", command=root.destroy, style="BrownSoft.TButton").grid(row=8, column=0, columnspan=3, sticky="ew")

    ttk.Label(main, textvariable=status_var, wraplength=760, justify="left").grid(row=9, column=0, columnspan=3, sticky="w", pady=(10, 0))

    main.columnconfigure(1, weight=1)
    root.mainloop()


if __name__ == "__main__":
    get_default_folders()
    build_gui()
