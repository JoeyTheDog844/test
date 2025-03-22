import subprocess

# ✅ List of critical services
CRITICAL_SERVICES = {
    "Geolocation Service": "lfsvc",
    "Remote Access Auto Connection Manager": "RasAuto",
    "Remote Access Connection Manager": "RasMan",
    "Routing and Remote Access": "RemoteAccess",
    "Remote Registry": "RemoteRegistry",
    "Remote Desktop Services": "TermService",
    "Remote Desktop Configuration": "SessionEnv",
    "OpenSSH Authentication Agent": "sshd",
    "Problem Reports Control Panel Support": "wercplsupport",
    "Telnet Client": "TlntSvr"
}

def get_service_status(service_name):
    """ ✅ Check if a Windows service is running, stopped, or disabled. """
    try:
        command = f'sc query "{service_name}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if "RUNNING" in result.stdout:
            return "Running"
        elif "STOPPED" in result.stdout:
            return "Stopped"
        elif "DISABLED" in result.stdout:
            return "Disabled"
        else:
            return "Unknown"
    except Exception as e:
        return f"Error: {e}"

def check_all_services():
    """ ✅ Fetch all service statuses. """
    statuses = {}
    for service, service_code in CRITICAL_SERVICES.items():
        statuses[service] = get_service_status(service_code)
    return statuses

def stop_all_services():
    """ ✅ Stop all running services. """
    stopped_services = []
    failed_services = []

    for service_name, service_code in CRITICAL_SERVICES.items():
        if get_service_status(service_code) == "Running":
            try:
                stop_command = f'sc stop "{service_code}"'
                result = subprocess.run(stop_command, shell=True, capture_output=True, text=True)

                if "STOP_PENDING" in result.stdout or "STOPPED" in result.stdout:
                    stopped_services.append(service_name)
                else:
                    failed_services.append(service_name)
            except Exception:
                failed_services.append(service_name)

    return stopped_services, failed_services

def start_all_services():
    """ ✅ Start all stopped services. """
    started_services = []
    failed_services = []

    for service_name, service_code in CRITICAL_SERVICES.items():
        if get_service_status(service_code) == "Stopped":
            try:
                start_command = f'sc start "{service_code}"'
                result = subprocess.run(start_command, shell=True, capture_output=True, text=True)

                if "RUNNING" in result.stdout:
                    started_services.append(service_name)
                else:
                    failed_services.append(service_name)
            except Exception:
                failed_services.append(service_name)

    return started_services, failed_services

def disable_all_services():
    """ ✅ Disable all critical services. """
    disabled_services = []
    failed_services = []

    for service_name, service_code in CRITICAL_SERVICES.items():
        try:
            disable_command = f'sc config "{service_code}" start= disabled'
            result = subprocess.run(disable_command, shell=True, capture_output=True, text=True)

            if "SUCCESS" in result.stdout:
                disabled_services.append(service_name)
            else:
                failed_services.append(service_name)
        except Exception:
            failed_services.append(service_name)

    return disabled_services, failed_services