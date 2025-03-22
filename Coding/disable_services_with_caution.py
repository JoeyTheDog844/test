import subprocess

# 🟡 Services That Can Be Disabled (But Consider Dependencies)
services = {
    "PlugPlay": "Plug and Play (Disabling may break device detection!)",
    "RpcEptMapper": "RPC Endpoint Mapper (Disabling may break Remote Procedure Call!)",
    "RpcLocator": "Remote Procedure Call (RPC) Locator (May affect network services!)",
    "Spaceport": "Microsoft Storage Spaces SMP (Disabling may break disk/RAID management!)",
    "ssh-agent": "OpenSSH Authentication Agent (Disabling breaks SSH authentication!)",
}

def disable_service_with_caution(service_name, display_name):
    try:
        # Change startup type to 'Disabled'
        subprocess.run(f'powershell -Command "Set-Service -Name {service_name} -StartupType Disabled"', shell=True, check=True)

        # Stop the service if it's running
        subprocess.run(f'powershell -Command "Stop-Service -Name {service_name} -Force"', shell=True, check=True)

        print(f"✅ Successfully disabled {display_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to disable {display_name}. (Requires Admin Privileges)")

# ✅ New function to disable all services only when explicitly called
def disable_all_caution_services():
    for service, display_name in services.items():
        disable_service_with_caution(service, display_name)

    print("\n🚀 Done! The selected services have been disabled.")

# Prevents automatic execution when imported
if __name__ == "__main__":
    disable_all_caution_services()