import subprocess
import re

def get_usb_logs():
    """Fetch last 10 USB-related logs with deep details for cybersecurity auditing."""
    command = 'wevtutil qe "Microsoft-Windows-DriverFrameworks-UserMode/Operational" /c:10 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    logs = result.stdout.strip().split("\n\n")  # Split log entries

    parsed_logs = []
    for log in logs:
        if "Event ID:" in log:
            lines = log.split("\n")
            
            # Extract relevant details
            event_id = next((line.split(":")[1].strip() for line in lines if "Event ID" in line), "Unknown")
            timestamp = next((line.split(":")[1].strip() for line in lines if "Date" in line), "Unknown")
            device_id = next((line.split(":")[1].strip() for line in lines if "USB\\VID" in line), "Unknown")
            serial_number = next((line.split(":")[1].strip() for line in lines if "Serial Number" in line), "Unknown")
            user = next((line.split(":")[1].strip() for line in lines if "User" in line), "SYSTEM")
            driver_name = next((line.split(":")[1].strip() for line in lines if "Driver Name" in line), "Unknown")
            driver_version = next((line.split(":")[1].strip() for line in lines if "Driver Version" in line), "Unknown")
            port_used = next((line.split(":")[1].strip() for line in lines if "Port" in line), "Unknown")
            description = next((line.strip() for line in lines if "Description:" in line), "No Description")
            installation_status = "Success" if "Status: Success" in log else "Failure"
            error_code = next((match.group(1) if (match := re.search(r'Error Code: (\d+)', line)) else None for line in lines), "None")

            # Flag unknown devices
            flagged_device = "Suspicious Device" if "VID_0000" in device_id or "Unknown" in driver_name else "Known Device"

            parsed_logs.append(f"""
📌 **Event ID:** {event_id}
        **Timestamp:** {timestamp}
        **Device ID:** {device_id}
        **Serial Number:** {serial_number}
        **User:** {user}
        **USB Port Used:** {port_used}
        **Driver:** {driver_name} (Version: {driver_version})
        **Description:** {description}
        **Installation Status:** {installation_status}
        **Error Code:** {error_code}
        **Security Check:** {flagged_device}
            """.strip())

    usb_logs = "\n\n".join(parsed_logs) if parsed_logs else "No USB activity detected."
    return usb_logs.strip()


def get_security_logs():
    """Fetch last 5 security logs from Windows Event Viewer."""
    command = 'wevtutil qe Security /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() or "No Security Logs Found."

def get_system_logs():
    """Fetch last 5 system logs."""
    command = 'wevtutil qe System /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() or "No System Logs Found."

def get_application_logs():
    """Fetch last 5 application logs."""
    command = 'wevtutil qe Application /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() or "No Application Logs Found."

def get_dns_logs():
    """Fetch last 5 DNS logs (if available)."""
    command = 'wevtutil qe "Microsoft-Windows-DNS-Client/Operational" /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() or "No DNS Logs Found."

if __name__ == "__main__":
    print("\n🔍 Fetching USB Logs...\n", get_usb_logs())

    print("\n🔍 Fetching Security Logs...\n", get_security_logs())

    print("\n🔍 Fetching System Logs...\n", get_system_logs())

    print("\n🔍 Fetching Application Logs...\n", get_application_logs())

    print("\n🔍 Fetching DNS Logs...\n", get_dns_logs())



