import subprocess
import datetime
import socket
import re

def get_antivirus_status():
    try:
        # ✅ Get installed antivirus from Windows Security Center
        cmd = 'powershell -Command "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object -ExpandProperty displayName"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if not output:
            return "No antivirus detected (Windows Defender may be inactive or another AV is in use)"

        antivirus_list = [av.strip() for av in output.split("\n") if av.strip()]
        return f"Antivirus Installed: {', '.join(antivirus_list)}"

    except Exception as e:
        return f"Error retrieving antivirus status: {e}"

def get_last_scan_time():
    try:
        # ✅ First, check if Windows Defender is running
        cmd1 = 'powershell -Command "(Get-MpComputerStatus).AMRunningMode"'
        defender_mode = subprocess.check_output(cmd1, shell=True).decode('utf-8').strip()

        if "Passive" in defender_mode:
            return "Windows Defender is in Passive Mode (Another antivirus is active)"

        # ✅ Check Last Scan Time (First Try Standard Method)
        cmd2 = 'powershell -Command "(Get-MpComputerStatus).ScanTime"'
        output = subprocess.check_output(cmd2, shell=True).decode('utf-8').strip()

        if output:
            return f"{output}"

        # ✅ If Standard Method Fails, Check Event Logs
        cmd3 = 'powershell -Command "Get-WinEvent -LogName \'Microsoft-Windows-Windows Defender/Operational\' | Where-Object Id -eq 1001 | Select-Object -First 1 -ExpandProperty TimeCreated"'
        output = subprocess.check_output(cmd3, shell=True).decode('utf-8').strip()

        if output:
            return f"{output}"

        return "No scan data available (Windows Defender inactive or not scanning)"

    except Exception as e:
        return f"Error retrieving scan time: {e}"

def get_usb_device_control_status():
    try:
        cmd = 'powershell -Command "(Get-MpComputerStatus).DeviceControlState"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if output == "Disabled":
            return "USB Access: Allowed"
        elif output == "Enabled":
            return "USB Access: Blocked"
        else:
            return f"USB Access Status: {output}"

    except Exception as e:
        return f"Error retrieving USB storage access status: {e}"

def get_autoplay_status():
    try:
        cmd = 'powershell -Command "Get-ItemProperty -Path HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\AutoplayHandlers | Select -ExpandProperty DisableAutoplay"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        # If output is "1", AutoPlay is disabled
        if output == "1":
            return "AutoPlay is Disabled"
        elif output == "0":
            return "AutoPlay is Enabled"
        else:
            return f"AutoPlay status unknown: {output}"

    except Exception as e:
        return f"Error retrieving AutoPlay status: {e}"

def get_rdp_status():
    try:
        cmd = 'powershell -Command "(Get-ItemProperty -Path \'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server\').fDenyTSConnections"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if output == "1":
            return "Disabled (RDP is OFF)"
        elif output == "0":
            return "Enabled (RDP is ON)"
        else:
            return f"RDP status unknown: {output}"

    except Exception as e:
        return f"Error retrieving RDP status: {e}"

def get_telnet_status():
    try:
        cmd = 'powershell -Command "Get-Service -Name Telnet | Select-Object -ExpandProperty Status"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if output.lower() == "stopped":
            return "Disabled"
        elif output.lower() == "running":
            return "Enabled (Insecure)"
        else:
            return f"Telnet status unknown: {output}"

    except subprocess.CalledProcessError:
        return "Not Installed"

def get_default_share_status():
    try:
        cmd = 'powershell -Command "Get-SmbShare | Where-Object {$_.Name -match \'^\w+\$$\'} | Select-Object -ExpandProperty Name"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if output:
            return "Enabled (Security Risk)"
        else:
            return "Disabled (Safe)"

    except subprocess.CalledProcessError:
        return "Error retrieving Default Share status"

def get_shared_folder_status():
    try:
        cmd = 'powershell -Command "Get-SmbShare | Where-Object {$_.Name -notmatch \'^\w+\$$\'} | Select-Object -ExpandProperty Name"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if output:
            return f"Configured (Security Risk) - {output}"
        else:
            return "Not Configured (Safe)"

    except subprocess.CalledProcessError:
        return "Error retrieving Shared Folder status"

import subprocess

def check_saved_passwords():
    try:
        cmd = 'powershell -Command "cmdkey /list"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if "Currently stored credentials" in output:
            return "Passwords Saved (See Credential Manager)"
        else:
            return "Passwords Not Saved (Safe)"

    except Exception as e:
        return f"Error checking saved passwords: {e}"

def get_bios_password_status():
    try:
        # ✅ Check if BIOS has security settings (BIOS version info)
        cmd = 'wmic bios get smbiosbiosversion'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if output:
            return "BIOS Password May Be Set (Check BIOS Manually)"
        else:
            return "No BIOS Password Detected"

    except:
        return "BIOS Password Status Unknown"

def get_login_password_status():
    try:
        # ✅ Get the current logged-in Windows user
        cmd_user = 'powershell -Command "$env:USERNAME"'
        username = subprocess.check_output(cmd_user, shell=True).decode('utf-8').strip()

        # ✅ Check if the user has a password set
        cmd_password = f'net user {username}'
        output = subprocess.check_output(cmd_password, shell=True).decode('utf-8')

        if "Password required" in output:
            if "Yes" in output:
                return f"Windows Login Password Set (User: {username})"
            else:
                return f"No Windows Login Password (User: {username})"

        return f"Windows Login Password Status Unknown (User: {username})"

    except:
        return "Error Retrieving Windows Login Password Status"

def get_password_policy_status():
    try:
        # ✅ Get Password Policy settings
        cmd = 'powershell -Command "net accounts | Select-String \'password\'"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        # Extract key values
        min_length = "Minimum password length:" in output and int(output.split("Minimum password length:")[1].split("\n")[0].strip()) or 0
        password_history = "Length of password history maintained:" in output and output.split("Length of password history maintained:")[1].split("\n")[0].strip() or "None"

        if min_length == 0:
            return f"Weak (Users can set empty passwords)\n{output}"
        elif password_history == "None":
            return f"Partial Password Policy (No password history enforced)\n{output}"
        else:
            return f"Password Policy is Configured \n{output}"

    except:
        return "Error Retrieving Password Policy"

def get_lockout_policy_status():
    try:
        # ✅ Fetch Lockout Policy settings
        cmd = 'powershell -Command "net accounts | Select-String \'Lockout\'"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        # Default values in case data is missing
        lockout_threshold = "Unknown"
        lockout_duration = "Unknown"
        lockout_window = "Unknown"

        # Extracting lockout values
        for line in output.split("\n"):
            if "Lockout threshold" in line:
                lockout_threshold = line.split(":")[-1].strip()
            elif "Lockout duration" in line:
                lockout_duration = line.split(":")[-1].strip()
            elif "Lockout observation window" in line:
                lockout_window = line.split(":")[-1].strip()

        # Determine final message
        if lockout_threshold == "Never":
            return (
                f"No System Lockout Policy (Accounts never lock)\n"
                f"Lockout Threshold: {lockout_threshold}\n"
                f"Lockout Duration (minutes): {lockout_duration}\n"
                f"Lockout Observation Window (minutes): {lockout_window}"
            )
        else:
            return (
                f"System Lockout Policy is Configured\n"
                f"Lockout Threshold: {lockout_threshold}\n"
                f"Lockout Duration (minutes): {lockout_duration}\n"
                f"Lockout Observation Window (minutes): {lockout_window}"
            )

    except Exception as e:
        return f"Error Retrieving Lockout Policy: {str(e)}"

# ✅ Define well-known ports to always show
COMMON_PORTS = {
    "21": "FTP",
    "22": "SSH",
    "23": "Telnet",
    "25": "SMTP",
    "53": "DNS",
    "80": "HTTP",
    "135": "RPC",
    "139": "NetBIOS",
    "443": "HTTPS",
    "445": "SMB",
    "3389": "RDP",
    "5353": "mDNS",
    "1900": "UPnP",
}

# ✅ Known UDP Services (Well-Known Ports)
KNOWN_UDP_PORTS = {
    "123": "NTP (Network Time Protocol)",
    "500": "ISAKMP (VPN Key Exchange)",
    "3702": "WS-Discovery (Device Discovery)",
    "53": "DNS",
    "67": "DHCP Server",
    "68": "DHCP Client",
    "161": "SNMP",
    "162": "SNMP Trap",
    "137": "NetBIOS Name Service",
    "138": "NetBIOS Datagram Service",
    "1900": "UPnP",
    "5353": "mDNS (Multicast DNS)"
}

def get_open_ports():
    """Find open TCP and UDP ports and their associated processes, filtering unnecessary noise."""
    try:
        # ✅ Get TCP Connections
        tcp_result = subprocess.run(["powershell", "Get-NetTCPConnection | Select-Object LocalPort, State"], 
                                    capture_output=True, text=True, shell=True)

        tcp_ports = set()
        for line in tcp_result.stdout.strip().split("\n")[3:]:  # Skip headers
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1].lower() == "listen":
                port = parts[0]
                # ✅ Only keep well-known ports + max 5 random ports
                if port in COMMON_PORTS or len(tcp_ports) < 5:
                    tcp_ports.add(f"Port {port} (TCP) - {COMMON_PORTS.get(port, 'Unknown')}")

        # ✅ Get UDP Connections
        udp_result = subprocess.run(["powershell", "Get-NetUDPEndpoint | Select-Object LocalAddress, LocalPort, OwningProcess"], 
                                    capture_output=True, text=True, shell=True)

        udp_ports = {}
        for line in udp_result.stdout.strip().split("\n")[3:]:  # Skip headers
            parts = re.split(r"\s+", line.strip())  
            if len(parts) >= 3:
                local_address, local_port, process_id = parts[:3]
                if local_port in COMMON_PORTS or len(udp_ports) < 5:
                    udp_ports[local_port] = udp_ports.get(local_port, []) + [process_id]

        # ✅ Format UDP output (Summarized by Port, Not Every Process ID)
        udp_list = [f"Port {port} (UDP) - {COMMON_PORTS.get(port, 'Unknown')} - Process IDs: {', '.join(set(pids))}"
                    for port, pids in udp_ports.items()]

        return {
            "tcp": list(tcp_ports) if tcp_ports else ["No open TCP ports detected."],
            "udp": udp_list if udp_list else ["No active UDP services detected."]
        }

    except Exception as e:
        return {
            "tcp": [f"Error retrieving TCP ports: {e}"],
            "udp": [f"Error retrieving UDP services: {e}"]
        }

def generate_security_log():
    # Gather all required data
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    antivirus_status = get_antivirus_status()
    scan_time = get_last_scan_time()
    usb_status = get_usb_device_control_status()
    autoplay_status = get_autoplay_status()
    rdp_status = get_rdp_status()
    telnet_status = get_telnet_status()
    default_share_status = get_default_share_status()
    shared_folders_status = get_shared_folder_status()
    check_saved_passwords_status = check_saved_passwords()
    bios_password_status = get_bios_password_status()
    login_password_status = get_login_password_status()
    password_policy_status = get_password_policy_status()
    System_lockout_policy_status = get_lockout_policy_status()
    open_ports = get_open_ports()
    open_ports_status = open_ports["tcp"]
    udp_services_status = open_ports["udp"]

    open_ports_text = "\n".join(open_ports_status) if open_ports_status else "No open TCP ports detected."
    udp_services_text = "\n".join(udp_services_status) if udp_services_status else "No active UDP services detected."

    log_entry = f"""
📌 [Antivirus Security Log]
-------------------------------------
Timestamp: {timestamp}

{antivirus_status}

Last Windows Defender Scan Time: {scan_time}

{usb_status}

AutoPlay Status: {autoplay_status}

Remote Desktop Protocol (RDP): {rdp_status}

Telnet: {telnet_status}

Default Share: {default_share_status}

Shared Folders: {shared_folders_status}

Passwords not saved in web/system: {check_saved_passwords_status}

{bios_password_status}  

{login_password_status}

Password Policy: {password_policy_status}

System Lockout Policy: {System_lockout_policy_status}

Open Ports: {", ".join(open_ports_status)}

UDP Services: {udp_services_text}

-------------------------------------
"""

    # Save to log file
    with open("security_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")

    print(log_entry)

if __name__ == "__main__":
    generate_security_log()
