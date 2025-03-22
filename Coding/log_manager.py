import subprocess

def get_security_logs():
    """Fetch last 5 security logs from Windows Event Viewer."""
    command = 'wevtutil qe Security /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_system_logs():
    """Fetch last 5 system logs."""
    command = 'wevtutil qe System /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_application_logs():
    """Fetch last 5 application logs."""
    command = 'wevtutil qe Application /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_dns_logs():
    """Fetch last 5 DNS logs (if available)."""
    command = 'wevtutil qe "Microsoft-Windows-DNS-Client/Operational" /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_usb_logs():
    """Fetch last 5 USB-related logs (Device Setup Logs)."""
    command = 'wevtutil qe "Microsoft-Windows-DriverFrameworks-UserMode/Operational" /c:5 /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()
