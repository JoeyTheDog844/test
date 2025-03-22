from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from system_information2 import (
    get_system_info,
    get_network_details,
    get_last_windows_update,
    get_desktop_files,
    get_system_identity,
    get_all_user_accounts,
)
from log_manager import (
    get_security_logs,
    get_system_logs,
    get_application_logs,
    get_dns_logs,
    get_usb_logs,
)
from security_logs import (
    get_antivirus_status,
    get_last_scan_time,
    get_usb_device_control_status,
    get_autoplay_status,
    get_rdp_status,
    get_telnet_status,
    get_default_share_status,
    get_shared_folder_status,
    check_saved_passwords,
    get_bios_password_status,
    get_login_password_status,
    get_password_policy_status,
    get_lockout_policy_status,
)
import datetime

def add_header(canvas, doc):
    """ Adds Audit Date (top-left) and Audit Time (top-right) to each page. """
    audit_date = datetime.datetime.now().strftime("%Y-%m-%d")  # YYYY-MM-DD format
    audit_time = datetime.datetime.now().strftime("%H:%M:%S")  # HH:MM:SS format
    page_number = canvas.getPageNumber()  # Get current page number
    canvas.setFont("Helvetica", 10)
    
    # Top-left: Audit Date
    canvas.drawString(40, 750, f"AUDIT DATE: {audit_date}")
    
    # Top-right: Audit Time
    canvas.drawRightString(550, 750, f"AUDIT TIME: {audit_time}")

    # Bottom-center: Page Number
    canvas.drawCentredString(300, 30, f"{page_number}")  # X = 300 (Center), Y = 30 (Bottom)

def generate_pdf_report():
    filename = "System_Audit_Report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []  # Stores all content for the PDF

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    # ✅ Generate Timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Title
    elements.append(Paragraph("<b><u>CYBER SECURITY AUDIT REPORT</u></b>", title_style))
    elements.append(Spacer(1, 20))  # Space after title

    # ✅ Collect System Information in Table
    system_info = get_system_info()
    elements.append(Paragraph("<b><u>System Information</u></b>", heading_style))
    elements.append(Spacer(1, 5))  # Small space before table

    # Define header text color variable
    header_text_color = colors.black  # Change this to colors.white, colors.black, etc.
    
    # Define table data with bold headers
    data = [[
    Paragraph(f'<b><font color="{header_text_color}">S.No</font></b>', styles["Normal"]),
    Paragraph(f'<b><font color="{header_text_color}">Parameter</font></b>', styles["Normal"]),
    Paragraph(f'<b><font color="{header_text_color}">Value</font></b>', styles["Normal"])
    ]]

    # Add actual system information data
    for i, (key, value) in enumerate(system_info.items(), start=1):
        data.append([str(i), key, str(value)])

    # Create table
    system_table = Table(data, colWidths=[50, 200, 250])

    # Apply styles (header row formatting)
    system_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), header_text_color),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Makes header bold
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Ensures normal font for data
    ]))
    # Apply alternating row colors
    for row_idx in range(1, len(data)):
        bg_color = colors.lightgrey if row_idx % 2 == 0 else colors.white
        system_table.setStyle(TableStyle([
            ('BACKGROUND', (0, row_idx), (-1, row_idx), bg_color),
        ]))

    elements.append(system_table)
    elements.append(Spacer(1, 20))  # Space after table

    # ✅ Collect Network Details in Table
    network_details = get_network_details()
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("<b>Network Details</b>", heading_style))
    elements.append(Spacer(1, 10))  # Small space before table

    # Define header text color variable
    header_text_color = colors.black  # Change this to colors.white, colors.black, etc.

    data = [[
    Paragraph(f'<b><font color="{header_text_color}">S.No</font></b>', styles["Normal"]),
    Paragraph(f'<b><font color="{header_text_color}">Parameter</font></b>', styles["Normal"]),
    Paragraph(f'<b><font color="{header_text_color}">Value</font></b>', styles["Normal"])
    ]]

    for i, (key, value) in enumerate(network_details.items(), start=1):
        data.append([str(i), key, str(value)])

    network_table = Table(data, colWidths=[50, 200, 250])
    network_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), header_text_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Ensures normal font for data
    ]))
    # Apply alternating row colors
    for row_idx in range(1, len(data)):
        bg_color = colors.lightgrey if row_idx % 2 == 0 else colors.white
        network_table.setStyle(TableStyle([
            ('BACKGROUND', (0, row_idx), (-1, row_idx), bg_color),
        ]))

    elements.append(network_table)
    elements.append(Spacer(1, 20))  # Space after table

    # ✅ Security Information Table with Serial Number
    elements.append(Paragraph("<b>Security Information</b>", heading_style))
    elements.append(Spacer(1, 5))

    # ✅ Add Serial Number Column
    security_data = [
        ["S.No", "Parameter", "Value"]  # Updated header with "S.No"
    ]

    # ✅ Populate table with serial numbers
    security_entries = [
        ["Timestamp", timestamp],
        ["Antivirus Installed", get_antivirus_status()],
        ["Last Windows Defender Scan Time", get_last_scan_time()],
        ["USB Storage Device Access", get_usb_device_control_status()],
        ["AutoPlay Status", get_autoplay_status()],
        ["Remote Desktop Protocol (RDP)", get_rdp_status()],
        ["Telnet", get_telnet_status()],
        ["Default Share Status", get_default_share_status()],
        ["Shared Folder Status", get_shared_folder_status()],
        ["Passwords not saved in web/system", check_saved_passwords()],
        ["BIOS Password", get_bios_password_status()],
        ["Windows Login Password", get_login_password_status()],
        ["Password Policy", get_password_policy_status()],
        ["System Lockout Policy", get_lockout_policy_status()],
    ]

    # ✅ Add serial numbers dynamically
    for i, (parameter, value) in enumerate(security_entries, start=1):
        security_data.append([str(i), parameter, str(value)])

    # ✅ Define column widths (adjusted for Serial Number)
    security_table = Table(security_data, colWidths=[50, 200, 250])

    # ✅ Apply table styles
    security_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font bold
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Data font
    ]))

    # ✅ Apply alternating row colors for readability
    for row_idx in range(1, len(security_data)):
        bg_color = colors.lightgrey if row_idx % 2 == 0 else colors.white
        security_table.setStyle(TableStyle([
            ('BACKGROUND', (0, row_idx), (-1, row_idx), bg_color),
        ]))

    elements.append(security_table)
    elements.append(Spacer(1, 20))  # Space after table

    # ✅ Users Accounts
    elements.append(Paragraph("<b>Users Accounts</b>", heading_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(get_all_user_accounts(), body_style))
    elements.append(Spacer(1, 20))

    # ✅ Last Windows Update
    elements.append(Paragraph("<b>Last Windows Update</b>", heading_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(get_last_windows_update(), body_style))
    elements.append(Spacer(1, 20))

    # ✅ Desktop Files
    elements.append(Paragraph("<b>Desktop Files</b>", heading_style))
    elements.append(Spacer(1, 5))
    desktop_files = get_desktop_files()
    if isinstance(desktop_files, (tuple, list)):
        desktop_files = "\n".join(map(str, desktop_files))
    elements.append(Paragraph(desktop_files, body_style))
    elements.append(Spacer(1, 20))

    # ✅ Security Logs
    elements.append(Paragraph("<b>Security Logs</b>", heading_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(get_security_logs(), body_style))
    elements.append(Spacer(1, 20))

    # ✅ System Logs
    elements.append(Paragraph("<b>System Logs</b>", heading_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(get_system_logs(), body_style))
    elements.append(Spacer(1, 20))

    # ✅ Application Logs
    elements.append(Paragraph("<b>Application Logs</b>", heading_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(get_application_logs(), body_style))
    elements.append(Spacer(1, 20))

    # ✅ DNS Logs
    elements.append(Paragraph("<b>DNS Logs</b>", heading_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(get_dns_logs(), body_style))
    elements.append(Spacer(1, 20))

    # ✅ USB Logs
    elements.append(Paragraph("<b>USB Logs</b>", heading_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(get_usb_logs(), body_style))
    elements.append(Spacer(1, 20))

    # ✅ Save the PDF
    doc.build(elements, onFirstPage=add_header, onLaterPages=add_header)
    print(f"✅ PDF Report Generated: {filename}")

# ✅ Run the script
if __name__ == "__main__":
    generate_pdf_report()
