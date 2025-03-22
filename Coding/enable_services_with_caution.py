import subprocess

# 🟡 Services That Were Disabled (Restoring Them)
services = {
    "PlugPlay": "Plug and Play (Re-enabling allows device detection!)",
    "RpcEptMapper": "RPC Endpoint Mapper (Required for Remote Procedure Call!)",
    "RpcLocator": "Remote Procedure Call (RPC) Locator (May restore network services!)",
    "Spaceport": "Microsoft Storage Spaces SMP (Needed for disk/RAID management!)",
    "ssh-agent": "OpenSSH Authentication Agent (Restores SSH authentication!)",
}

def enable_service_with_caution(service_name, display_name):
    try:
        # Change startup type to 'Automatic'
        subprocess.run(f'powershell -Command "Set-Service -Name {service_name} -StartupType Automatic"', shell=True, check=True)

        # Start the service
        subprocess.run(f'powershell -Command "Start-Service -Name {service_name}"', shell=True, check=True)

        print(f"✅ Successfully enabled {display_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to enable {display_name}. (Requires Admin Privileges)")

# Enable each service
for service, display_name in services.items():
    enable_service_with_caution(service, display_name)

print("\n🚀 Done! The selected services have been restored.")
