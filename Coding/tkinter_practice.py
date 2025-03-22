from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, ListItem, ListFlowable
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
    check_open_ports,
)
from datetime import datetime
import re

def add_header_footer(canvas, doc):
    """ Adds Audit Date (top-left), Audit Time (top-right), and Page Numbers (bottom-center). """
    audit_date = datetime.now().strftime("%Y-%m-%d")  # YYYY-MM-DD format
    audit_time = datetime.now().strftime("%H:%M:%S")  # HH:MM:SS format
    page_number = canvas.getPageNumber()  # Get current page number
    
    canvas.setFont("Helvetica", 10)

    # Top-left: Audit Date
    canvas.drawString(40, 750, f"AUDIT DATE: {audit_date}")
    
    # Top-right: Audit Time
    canvas.drawRightString(550, 750, f"AUDIT TIME: {audit_time}")

    # Bottom-center: Page Number
    canvas.drawCentredString(300, 30, f"{page_number}")  # X = 300 (Center), Y = 30 (Bottom)

def clean_text(text):
    """Removes non-printable characters and ensures proper line breaks for PDFs."""
    text = text.encode("ascii", "ignore").decode()  # ✅ Remove Unicode issues
    text = re.sub(r"[^\x20-\x7E\n]", "", text)  # ✅ Remove non-ASCII characters
    text = text.replace("\n", " ")  # ✅ Replace newlines with spaces for descriptions
    text = text.replace("?", "").strip()  # ✅ Remove unexpected `?`
    return text

def format_timestamp(timestamp):
    """Convert Windows Event timestamp to a readable format."""
    try:
        timestamp = timestamp.rstrip("Z")  # ✅ Remove trailing "Z"

        if "." in timestamp:
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

        return dt.strftime("%Y-%m-%d %H:%M:%S")  # ✅ Readable format
    except ValueError:
        return timestamp  # Return as is if parsing fails
    
def generate_pdf_report():
    filename = "System_Audit_Report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []  # Stores all content for the PDF

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    error_style = ParagraphStyle("ErrorStyle", parent=body_style, textColor=colors.red)
    warning_style = ParagraphStyle("WarningStyle", parent=body_style, textColor=colors.orange)
    info_style = ParagraphStyle("InfoStyle", parent=body_style, textColor=colors.green)

    # ✅ Generate Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    elements.append(Paragraph("<b><u>Network Details</u></b>", heading_style))
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
    elements.append(Paragraph("<b><u>Security Information</u></b>", heading_style))
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
        ["Open Ports", ", ".join(check_open_ports())],
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
    elements.append(Paragraph("<b><u>Users Accounts</u></b>", heading_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(get_all_user_accounts(), body_style))
    elements.append(Spacer(1, 20))

    # ✅ Last Windows Update
    elements.append(Paragraph("<b><u>Last Windows Update</u></b>", heading_style))
    elements.append(Spacer(1, 5))
    last_update_text = get_last_windows_update().replace("\n", "<br/>")

    elements.append(Paragraph(last_update_text, body_style))
    elements.append(Spacer(1, 20))

    # ✅ Desktop Files
    elements.append(Paragraph("<b><u>Desktop Files</u></b>", heading_style))
    elements.append(Spacer(1, 5))
    desktop_files = get_desktop_files()
    if isinstance(desktop_files, (tuple, list)):
        desktop_files = "\n".join(map(str, desktop_files))
    elements.append(Paragraph(desktop_files, body_style))
    elements.append(Spacer(1, 20))

    def format_timestamp(timestamp):
        """Convert Windows Event timestamp to a readable format."""
        try:
            timestamp = timestamp.rstrip("Z")  # ✅ Remove trailing "Z"
        
            if "." in timestamp:
                dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
            else:
                dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        
            return dt.strftime("%Y-%m-%d %H:%M:%S")  # ✅ Readable format
        except ValueError:
            return timestamp  # Return as is if parsing fails
    
    # ✅ Log Analysis with Color Coding
    def format_logs_for_pdf(logs):
        if not logs.strip():
            return [("<b>No logs found.</b>", info_style)]

        events = logs.strip().split("Event[")
        formatted_logs = []

        for event in events:
            event = event.strip()
            if event:
                event_lines = event.split("\n")
                event_id = next((line.split(":")[1].strip() for line in event_lines if "Event ID" in line), "Unknown")
                timestamp_raw = next((line.split(":", 1)[1].strip() if ":" in line else "Unknown" for line in event_lines if "Date" in line), "Unknown")
                timestamp = format_timestamp(timestamp_raw)  # ✅ Convert timestamp
                source = next((line.split(":")[1].strip() for line in event_lines if "Source" in line), "Unknown")
                description_lines = []
                capture_description = False

                for line in event_lines:
                    if "Description:" in line:
                        capture_description = True
                        description_lines.append(line.split("Description:", 1)[1].strip())
                    elif capture_description:
                        if line.strip() == "":
                            break  # Stop capturing on an empty line
                        description_lines.append(line.strip())

                description = " ".join(description_lines).strip() if description_lines else "No Description Found"
                
                description = clean_text(description)

                # ✅ Fix: Replace problematic characters for ReportLab
                description = " ".join(description_lines) if description_lines else "No Description Found"
                description = clean_text(description)

                level = next((line.split(":")[1].strip() for line in event_lines if "Level" in line), "Information")

                log_style = error_style if "Error" in level else warning_style if "Warning" in level else info_style
                formatted_logs.append((
                    f"<b>Event ID:</b> {event_id}<br/>"
                    f"<b>Timestamp:</b> {timestamp}<br/>"
                    f"<b>Source:</b> {source}<br/>"
                    f"<b>Description:</b> {description}<br/><br/>", 
                    log_style
                ))

        return formatted_logs

    def add_log_section(title, logs):
        elements.append(Paragraph(f"<b>{title}</b>", heading_style))
        elements.append(Spacer(1, 5))

        log_entries = format_logs_for_pdf(logs)
        list_items = [ListItem(Paragraph(log[0], log[1])) for log in log_entries]
        elements.append(ListFlowable(list_items, bulletType="bullet"))
        elements.append(Spacer(1, 20))

    add_log_section("<u>USB Logs</u>", get_usb_logs())
    add_log_section("<u>Security Logs</u>", get_security_logs())
    add_log_section("<u>System Logs</u>", get_system_logs())
    add_log_section("<u>Application Logs</u>", get_application_logs())
    add_log_section("<u>DNS Logs</u>", get_dns_logs())

    # ✅ Save the PDF
    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"✅ PDF Report Generated: {filename}")
    
# ✅ Run the script
if __name__ == "__main__":
    generate_pdf_report()
