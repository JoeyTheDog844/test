import system_audit
import logs_analysis
import cache_cleaner

if __name__ == "__main__":
    print("🔍 Running IT Audit Tool...\n")

    # Get system info
    system_info = system_audit.get_system_info()
    print("📌 System Info:", system_info)

    # Get security logs
    logs = logs_analysis.get_security_logs()
    print("\n📌 Security Logs:\n", logs)

    # Clear cache
    cache_status = cache_cleaner.clear_temp_files()
    print("\n📌 Cache Cleanup Status:", cache_status)
