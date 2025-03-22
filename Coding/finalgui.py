import tkinter as tk
from system_information2 import generate_system_report, get_system_info, get_network_details, get_last_windows_update, get_desktop_files, get_system_identity
from pdf_generator import generate_pdf_report
from cache_manager import clear_all_caches, clear_recycle_bin, clear_temp_files, clear_dns_cache, clear_windows_update_cache
from disable_services import disable_service, disable_all_services
from disable_services_with_caution import disable_all_caution_services

# Create main application window
root = tk.Tk()
root.title("IT Audit Tool")
root.geometry("600x500")  # Adjust size as needed
root.configure(bg="#3d3d3d")  # ✅ Set background color (Dark Gray)

# ✅ Create a heading label
heading_label = tk.Label(
    root, 
    text="CyberSecurity Audit Tool", 
    font=("Arial", 20,"bold"),  # ✅ Large font size
    fg="white",  # ✅ White text color
    bg="#3d3d3d"  # ✅ Match background color
)
heading_label.pack(pady=20)  # ✅ Add spacing

# Create Buttons with large size
button_font = ("Arial", 14, "bold")

btn_export = tk.Button(root, text="Export Report to PDF", font=button_font, bg="black", fg="white", height=2, width=20, command=generate_pdf_report)
btn_export.pack(pady=10)

# Frame for cache buttons (initially hidden)
cache_frame = tk.Frame(root, bg="#2C2C2C")  # ✅ Background color for frame
cache_frame.pack_propagate(False)  # Prevent resizing based on content

#btn_logs = tk.Button(root, text="Generate Logs", font=button_font, bg="green", fg="white", height=2, width=20, command=generate_logs)
#btn_logs.pack(pady=10)

# Frame for cache buttons (initially hidden)
cache_frame = tk.Frame(root)

# Function to toggle visibility of cache options
def toggle_cache_options():
    if cache_frame.winfo_ismapped():  # Check if frame is visible
        cache_frame.pack_forget()  # Hide if already visible
    else:
        cache_frame.pack(pady=5, before=btn_disable)  # Show above "Disable Services" button

# Function to clear all caches
def clear_all():
    clear_all_caches()
    clear_recycle_bin()
    clear_temp_files()
    clear_dns_cache()
    clear_windows_update_cache()

# Button to show/hide cache options
btn_toggle_cache = tk.Button(root, text="Clear Cache", font=button_font, bg="lightblue", fg="black", height=2, width=20, command=toggle_cache_options)
btn_toggle_cache.pack(pady=5)

# Create Individual Clear Cache Buttons inside cache_frame (Two-column layout)
btn_clear_all = tk.Button(cache_frame, text="Clear All Cache", font=button_font, bg="darkblue", fg="white", height=2, width=20, command=clear_all)
btn_clear_cache = tk.Button(cache_frame, text="Clear App Caches", font=button_font, bg="darkblue", fg="white", height=2, width=20, command=clear_all_caches)

btn_clear_recycle_bin = tk.Button(cache_frame, text="Clear Recycle Bin", font=button_font, bg="darkblue", fg="white", height=2, width=20, command=clear_recycle_bin)
btn_clear_temp = tk.Button(cache_frame, text="Clear Temp Files", font=button_font, bg="darkblue", fg="white", height=2, width=20, command=clear_temp_files)

btn_clear_dns = tk.Button(cache_frame, text="Clear DNS Cache", font=button_font, bg="darkblue", fg="white", height=2, width=20, command=clear_dns_cache)
btn_clear_update_cache = tk.Button(cache_frame, text="Clear Windows\nUpdate Cache", font=button_font, bg="darkblue", fg="white", height=2, width=20, command=clear_windows_update_cache)

# Positioning buttons in a two-column layout
btn_clear_all.grid(row=0, column=0, padx=5, pady=2)  
btn_clear_cache.grid(row=0, column=1, padx=5, pady=2)  

btn_clear_recycle_bin.grid(row=1, column=0, padx=5, pady=2)  
btn_clear_temp.grid(row=1, column=1, padx=5, pady=2)  

btn_clear_dns.grid(row=2, column=0, padx=5, pady=2)  
btn_clear_update_cache.grid(row=2, column=1, padx=5, pady=2)  

btn_disable = tk.Button(root, text="Disable Services", font=button_font, bg="red", fg="white", height=2, width=20, command=disable_all_services)
btn_disable.pack(pady=10)

btn_disable_caution = tk.Button(
    root, text="Disable Services with Caution", font=button_font,
    bg="red", fg="white", height=2, width=25,
    command=disable_all_caution_services
)
btn_disable_caution.pack(pady=10)

# Run the Tkinter loop
root.mainloop()