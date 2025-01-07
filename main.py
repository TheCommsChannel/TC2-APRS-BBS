import database
import aprs_comm
import threading
import time


def scheduled_cleanup():
    """Periodically run cleanup of expired bulletins."""
    while True:
        try:
            print("Running periodic cleanup of expired bulletins...")
            database.delete_expired_bulletins()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        time.sleep(24 * 60 * 60)  # Run cleanup every 24 hours

def main():
    banner = """
\033[96m
████████╗ ██████╗██████╗       ██████╗ ██████╗ ███████╗
╚══██╔══╝██╔════╝╚════██╗      ██╔══██╗██╔══██╗██╔════╝
   ██║   ██║      █████╔╝█████╗██████╔╝██████╔╝███████╗
   ██║   ██║     ██╔═══╝ ╚════╝██╔══██╗██╔══██╗╚════██║
   ██║   ╚██████╗███████╗      ██████╔╝██████╔╝███████║
   ╚═╝    ╚═════╝╚══════╝      ╚═════╝ ╚═════╝ ╚══════╝
\033[93mAPRS Version\033[0m
    """
    print(banner)

    print("Initializing database...")
    database.init_db()

    # Start periodic bulletin cleanup in a separate thread
    cleanup_thread = threading.Thread(target=scheduled_cleanup, daemon=True)
    cleanup_thread.start()

    print("Starting APRS communications...")
    aprs_comm.start()

if __name__ == "__main__":
    main()
