import subprocess

def disable_services():
    """Disables selected services."""
    services = [
        "bthserv",  # Bluetooth Support Service
        "lfsvc",  # Geolocation Service
        "TermService",  # Remote Desktop Services
        "RemoteAccess",  # Routing and Remote Access
        "WFDSConMgrSvc",  # Wi-Fi Direct Services
        "xbgm",  # Xbox Game Monitoring
        "LanmanServer"  # Default Share Status
    ]
    
    disabled_services = []
    failed_services = []
    
    for service in services:
        result = subprocess.run(["sc", "config", service, "start= disabled"], capture_output=True, text=True)
        if "SUCCESS" in result.stdout:
            disabled_services.append(service)
        else:
            failed_services.append(service)
    
    return disabled_services, failed_services

def enable_services():
    """Enables selected services."""
    services = [
        "bthserv", "lfsvc", "TermService", "RemoteAccess", "WFDSConMgrSvc", "xbgm", "LanmanServer"]
    
    enabled_services = []
    failed_services = []
    
    for service in services:
        result = subprocess.run(["sc", "config", service, "start= auto"], capture_output=True, text=True)
        if "SUCCESS" in result.stdout:
            enabled_services.append(service)
        else:
            failed_services.append(service)
    
    return enabled_services, failed_services

def stop_services():
    """Stops selected services."""
    services = ["bthserv", "lfsvc", "TermService", "RemoteAccess", "WFDSConMgrSvc", "xbgm", "LanmanServer"]
    
    stopped_services = []
    failed_services = []
    
    for service in services:
        result = subprocess.run(["net", "stop", service], capture_output=True, text=True)
        if "successfully stopped" in result.stdout.lower():
            stopped_services.append(service)
        else:
            failed_services.append(service)
    
    return stopped_services, failed_services

def check_services_status():
    """ ✅ Retrieves the current status (Running, Stopped, or Disabled) of the selected services. """
    services = {
        "bthserv": "Bluetooth Support Service",
        "lfsvc": "Geolocation Service",
        "TermService": "Remote Desktop Services",
        "RemoteAccess": "Routing and Remote Access",
        "WFDSConMgrSvc": "Wi-Fi Direct Services",
        "xbgm": "Xbox Game Monitoring",
        "LanmanServer": "Default Share Status"
    }

    statuses = {}

    for service, service_name in services.items():
        result = subprocess.run(["sc", "query", service], capture_output=True, text=True)
        
        if "RUNNING" in result.stdout:
            statuses[service_name] = "Running"
        elif "STOPPED" in result.stdout:
            statuses[service_name] = "Stopped"
        else:
            statuses[service_name] = "Disabled or Not Found"

    return statuses
