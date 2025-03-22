import subprocess

# List of services to re-enable
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

def enable_service(service_name, display_name):
    try:
        # Set startup type to 'Automatic'
        subprocess.run(f'powershell -Command "Set-Service -Name {service_name} -StartupType Automatic"', shell=True, check=True)

        # Start the service
        subprocess.run(f'powershell -Command "Start-Service -Name {service_name}"', shell=True, check=True)

        print(f"✅ Successfully re-enabled {display_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to enable {display_name}. (Requires Admin Privileges)")

# Enable each service
for service, display_name in services.items():
    enable_service(service, display_name)

print("\n🔄 Done! The selected services have been re-enabled.")