import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow for resizing images
import disable_services_gui
from tkinter import messagebox
import automate_rdp_services
import password_policy

def on_enter(e, button):
    button.config(bg='#d9d9d9', relief='raised')  # Lighten the button and add raised effect

def on_leave(e, button):
    button.config(bg='#c3c3c3', relief='flat')  # Restore original color and flat style

# Load and Resize Image
image_path = r"C:\Users\amaan\Desktop\Coding\doggy.jpg"  # Ensure this is the correct path

root = tk.Tk()
root.geometry('700x500')
root.title('CyberSecurity Audit Application')

def show_automate_services():
    """ ✅ Display service statuses in the GUI """
    for widget in automateservices_frame.winfo_children():
        widget.destroy()  # ✅ Clear old labels

    service_statuses = disable_services_gui.check_all_services()  # ✅ Fetch service statuses

    # ✅ Display service names & statuses
    for i, (service, status) in enumerate(service_statuses.items()):
        tk.Label(automateservices_frame, text=service, font=("Arial", 10), anchor="w").grid(row=i, column=0, sticky="w", padx=5, pady=2)
        tk.Label(automateservices_frame, text=status, font=("Arial", 10), fg="green" if status == "Running" else "red").grid(row=i, column=1, padx=5, pady=2)

    # ✅ Buttons for stopping, starting, and disabling services
    stop_button = tk.Button(automateservices_frame, text="STOP ALL SERVICES", font=("Bold", 12), bg="red", fg="white", command=stop_automate_services)
    stop_button.grid(row=len(service_statuses) + 1, column=0, padx=5, pady=10)

    start_button = tk.Button(automateservices_frame, text="START ALL SERVICES", font=("Bold", 12), bg="green", fg="white", command=start_automate_services)
    start_button.grid(row=len(service_statuses) + 1, column=1, padx=5, pady=10)

    disable_button = tk.Button(automateservices_frame, text="DISABLE ALL SERVICES", font=("Bold", 12), bg="gray", fg="white", command=disable_automate_services)
    disable_button.grid(row=len(service_statuses) + 2, column=0, columnspan=2, padx=5, pady=10)

def stop_automate_services():
    """ ✅ Stop all running services """
    stopped_services, failed_services = disable_services_gui.stop_all_services()

    if stopped_services:
        messagebox.showinfo("Services Stopped", f"Successfully stopped:\n" + "\n".join(stopped_services))
    if failed_services:
        messagebox.showwarning("Failed to Stop", f"Could not stop:\n" + "\n".join(failed_services))

    show_automate_services()

def start_automate_services():
    """ ✅ Start all stopped services """
    started_services, failed_services = disable_services_gui.start_all_services()

    if started_services:
        messagebox.showinfo("Services Started", f"Successfully started:\n" + "\n".join(started_services))
    if failed_services:
        messagebox.showwarning("Failed to Start", f"Could not start:\n" + "\n".join(failed_services))

    show_automate_services()

def disable_automate_services():
    """ ✅ Disable all critical services """
    disabled_services, failed_services = disable_services_gui.disable_all_services()

    if disabled_services:
        messagebox.showinfo("Services Disabled", f"Successfully disabled:\n" + "\n".join(disabled_services))
    if failed_services:
        messagebox.showwarning("Failed to Disable", f"Could not disable:\n" + "\n".join(failed_services))

    show_automate_services()

def automateservices_page():
    """ ✅ Show the automate services page """
    delete_pages()
    
    global automateservices_frame
    automateservices_frame = tk.Frame(main_frame)
    automateservices_frame.pack(pady=10, fill="both", expand=True)

    show_automate_services()

def show_rdp_services():
    """ ✅ Display RDP & Remote Services statuses in the GUI """
    for widget in rdp_services_frame.winfo_children():
        widget.destroy()  # ✅ Clear old labels

    service_statuses = automate_rdp_services.check_services_status()  # ✅ Fetch service statuses

    # ✅ Display service names & statuses
    for i, (service, status) in enumerate(service_statuses.items()):
        tk.Label(rdp_services_frame, text=service, font=("Arial", 10), anchor="w").grid(row=i, column=0, sticky="w", padx=5, pady=2)
        tk.Label(rdp_services_frame, text=status, font=("Arial", 10), fg="green" if status == "Running" else "red").grid(row=i, column=1, padx=5, pady=2)

    # ✅ Buttons for stopping, starting, and disabling services
    stop_button = tk.Button(rdp_services_frame, text="STOP SERVICES", font=("Bold", 12), bg="red", fg="white", command=stop_rdp_services)
    stop_button.grid(row=len(service_statuses) + 1, column=0, padx=5, pady=10)

    start_button = tk.Button(rdp_services_frame, text="ENABLE SERVICES", font=("Bold", 12), bg="green", fg="white", command=enable_rdp_services)
    start_button.grid(row=len(service_statuses) + 1, column=1, padx=5, pady=10)

    disable_button = tk.Button(rdp_services_frame, text="DISABLE SERVICES", font=("Bold", 12), bg="gray", fg="white", command=disable_rdp_services)
    disable_button.grid(row=len(service_statuses) + 2, column=0, columnspan=2, padx=5, pady=10)

def stop_rdp_services():
    """ ✅ Stop all RDP & Remote Services """
    stopped_services, failed_services = automate_rdp_services.stop_services()

    if stopped_services:
        messagebox.showinfo("Services Stopped", f"Successfully stopped:\n" + "\n".join(stopped_services))
    if failed_services:
        messagebox.showwarning("Failed to Stop", f"Could not stop:\n" + "\n".join(failed_services))

    show_rdp_services()  # ✅ Refresh the GUI

def enable_rdp_services():
    """ ✅ Enable all RDP & Remote Services """
    enabled_services, failed_services = automate_rdp_services.enable_services()

    if enabled_services:
        messagebox.showinfo("Services Enabled", f"Successfully enabled:\n" + "\n".join(enabled_services))
    if failed_services:
        messagebox.showwarning("Failed to Enable", f"Could not enable:\n" + "\n".join(failed_services))

    show_rdp_services()  # ✅ Refresh the GUI

def disable_rdp_services():
    """ ✅ Disable all RDP & Remote Services """
    disabled_services, failed_services = automate_rdp_services.disable_services()

    if disabled_services:
        messagebox.showinfo("Services Disabled", f"Successfully disabled:\n" + "\n".join(disabled_services))
    if failed_services:
        messagebox.showwarning("Failed to Disable", f"Could not disable:\n" + "\n".join(failed_services))

    show_rdp_services()  # ✅ Refresh the GUI

def rdp_services_page():
    """ ✅ Show the RDP & Remote Services page """
    delete_pages()

    global rdp_services_frame
    rdp_services_frame = tk.Frame(main_frame)
    rdp_services_frame.pack(pady=10, fill="both", expand=True)

    show_rdp_services()

def show_password_policy():
    """ ✅ Display the current password policy in the GUI """
    delete_pages()

    global password_policy_frame
    password_policy_frame = tk.Frame(main_frame)
    password_policy_frame.pack(pady=10, fill="both", expand=True)

    # ✅ Fetch current password policy
    policy_text = password_policy.get_current_policy()

    # ✅ Display Policy in a Label
    policy_label = tk.Label(password_policy_frame, text="Current Password Policy:\n\n" + policy_text,
                            font=("Arial", 10), anchor="w", justify="left")
    policy_label.pack(padx=10, pady=10)

    # ✅ "Apply Password Policy" Button (Inside the Page)
    apply_button = tk.Button(password_policy_frame, text="APPLY PASSWORD POLICY", font=("Bold", 12),
                             bg="blue", fg="white", command=apply_password_policy)
    apply_button.pack(pady=10)

def apply_password_policy():
    """ ✅ Ask for confirmation before applying new password policy """
    confirm = messagebox.askyesno("Confirm Policy Change", "Are you sure you want to apply the new password policy?")
    
    if confirm:  # Only proceed if the user clicks "Yes"
        result = password_policy.set_password_policy()
        messagebox.showinfo("Password Policy Updated", result)

        # ✅ Refresh to show the updated policy
        show_password_policy()

def home_page():
    home_frame = tk.Frame(main_frame)
    lb = tk.Label(home_frame, text='CyberSecurity Audit Application\n\nPage: 1', font=('Bold', 30))
    lb.pack()
    home_frame.pack(pady=20)

def hide_indicators():
    home_indicate.config(bg='#c3c3c3')
    automateservices_indicate.config(bg='#c3c3c3')
    rdp_services_indicate.config(bg='#c3c3c3')
    password_policy_indicate.config(bg='#c3c3c3')

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

def indicate(lb, page):
    hide_indicators()
    lb.config(bg='#158aff')
    delete_pages()
    page()

# Sidebar container frame (Now it does NOT restrict options_frame)
sidebar_frame = tk.Frame(root, bg='#c3c3c3')

# Options Frame (Manually set its width again)
options_frame = tk.Frame(sidebar_frame, bg='#c3c3c3', width=140, height=600)
options_frame.configure(width=140, height=600)  # Explicitly set size

# Load and Resize Logo (Separate from options_frame)
try:
    original_image = Image.open(image_path)
    resized_image = original_image.resize((95, 95), Image.LANCZOS)  # Resize to fit
    logo_img = ImageTk.PhotoImage(resized_image)  # Convert to Tkinter-compatible format

    logo_label = tk.Label(sidebar_frame, image=logo_img, bg='#c3c3c3')
    logo_label.pack(pady=10)  # Align properly
except Exception as e:
    print(f"Error loading logo: {e}")

# Create indicators first before buttons to avoid NameError
home_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
home_indicate.grid(row=0, column=0, sticky="w", padx=5)

automateservices_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
automateservices_indicate.grid(row=1, column=0, sticky="w", padx=5)

rdp_services_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
rdp_services_indicate.grid(row=2, column=0, sticky="w", padx=5)

password_policy_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
password_policy_indicate.grid(row=3, column=0, sticky="w", padx=5)

# Configure the options_frame for perfect alignment
options_frame.grid_columnconfigure(1, weight=1)  # Ensure buttons expand evenly

# Home Button
home_btn = tk.Button(
    options_frame, text='HOME', font=('Bold', 15),
    fg='#158aff', bd=0, bg='#c3c3c3', relief='flat',
    command=lambda: indicate(home_indicate, home_page)
)
home_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
home_btn.bind('<Enter>', lambda e: on_enter(e, home_btn))
home_btn.bind('<Leave>', lambda e: on_leave(e, home_btn))

# DISABLE Services Button
automateservices_btn = tk.Button(
    options_frame, text='DISABLE\nSERVICES', font=('Bold', 15),
    fg='#158aff', bd=0, bg='#c3c3c3', relief='flat',
    command=lambda: indicate(automateservices_indicate, automateservices_page)
)
automateservices_btn.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
automateservices_btn.bind('<Enter>', lambda e: on_enter(e, automateservices_btn))
automateservices_btn.bind('<Leave>', lambda e: on_leave(e, automateservices_btn))

# Automate RDP Services Button
rdp_services_btn = tk.Button(
    options_frame, text='AUTOMATE\nRDP SERVICES', font=('Bold', 15),
    fg='#158aff', bd=0, bg='#c3c3c3', relief='flat',
    command=lambda: indicate(rdp_services_indicate, rdp_services_page)
)
rdp_services_btn.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
rdp_services_btn.bind('<Enter>', lambda e: on_enter(e, rdp_services_btn))
rdp_services_btn.bind('<Leave>', lambda e: on_leave(e, rdp_services_btn))

# Password Policy Button
password_policy_btn = tk.Button(
    options_frame, text="SET PASSWORD\nPOLICY", font=('Bold', 15),
    fg='#158aff', bd=0, bg='#c3c3c3', relief='flat',
    command=lambda: indicate(password_policy_indicate, show_password_policy)  # ✅ Opens policy page instead
)
password_policy_btn.grid(row=3, column=1, sticky="ew", padx=10, pady=10)
password_policy_btn.bind('<Enter>', lambda e: on_enter(e, password_policy_btn))
password_policy_btn.bind('<Leave>', lambda e: on_leave(e, password_policy_btn))

# Pack everything properly
options_frame.pack(fill="both", expand=False)  # Now it can be resized manually
sidebar_frame.pack(side=tk.LEFT, fill="y")  # Sidebar keeps full height

# Main content area
main_frame = tk.Frame(root, highlightbackground='black', highlightthickness=2)
main_frame.pack(side=tk.LEFT, fill="both", expand=True)

root.mainloop()
