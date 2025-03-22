import subprocess

# List of services to disable (Safe ones)
services = {
    "LanmanServer": "Server",
    "lfsvc": "Geolocation Service",
    "MSDTC": "Distributed Transaction Coordinator",
    "RasAuto": "Remote Access Auto Connection Manager",
    "RasMan": "Remote Access Connection Manager",
    "RemoteAccess": "Routing and Remote Access",
    "RemoteRegistry": "Remote Registry",
    "SessionEnv": "Remote Desktop Configuration",
    "TermService": "Remote Desktop Services",
    "wercplsupport": "Problem Reports Control Panel Support",
}

def disable_service(service_name, display_name):
    try:
        # Change startup type to 'Disabled'
        subprocess.run(f'powershell -Command "Set-Service -Name {service_name} -StartupType Disabled"', shell=True, check=True)

        # Stop the service if it's running
        subprocess.run(f'powershell -Command "Stop-Service -Name {service_name} -Force"', shell=True, check=True)

        print(f"✅ Successfully disabled {display_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to disable {display_name}. (Requires Admin Privileges)")

# ✅ New function to disable all services only when explicitly called
def disable_all_services():
    for service, display_name in services.items():
        disable_service(service, display_name)

    print("\n🚀 Done! The selected services have been disabled.")

# Prevents automatic execution when imported
if __name__ == "__main__":
    disable_all_services()