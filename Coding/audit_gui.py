import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from system_audit import generate_system_report
from datetime import datetime

# Create the main application window
root = tb.Window(themename="darkly")
root.title("System Audit Report")
root.geometry("700x500")
root.resizable(False, False)

# Create a frame for layout
frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Create a Text widget with a scrollbar
text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12), bg="#2b2b2b", fg="white", padx=10, pady=10, relief=tk.FLAT)
scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
text_widget.config(yscrollcommand=scrollbar.set)

# Insert system report text into widget
def update_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get the system report
    raw_report = generate_system_report()

    # Ensure no duplicate title
    cleaned_report = "\n".join(line for line in raw_report.split("\n") if "🔍 System Audit Report" not in line).strip()

    # Format Windows Update section (align columns properly)
    cleaned_report = cleaned_report.replace("Description      InstalledOn", "Description         Installed On")
    
    # Format Desktop Files section with bullet points
    if "📌 Desktop Files:" in cleaned_report:
        before, files_section = cleaned_report.split("📌 Desktop Files:", 1)
        file_list = files_section.strip().split("\n")
        formatted_files = "\n".join([f"  • {file}" for file in file_list])
        cleaned_report = f"{before}📌 Desktop Files:\n{formatted_files}"

    # Construct the formatted report
    report_text = (
        f"🔍 **System Audit Report** (Generated: {timestamp})\n"
        "════════════════════════════════════════\n"
        f"{cleaned_report}\n"
        "════════════════════════════════════════"
    )

    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, report_text)
    text_widget.config(state=tk.DISABLED)

update_report()  # Initial load

# Create a button to refresh the report
refresh_button = tb.Button(root, text="🔄 Refresh Report", bootstyle="success", command=update_report)
refresh_button.pack(pady=10)

# Pack widgets
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Run the Tkinter main loop
root.mainloop()
