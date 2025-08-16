import os
import datetime

def main():
    # Get environment variables from ConfigMap / Secret
    app_env = os.getenv("APP_ENV", "development")
    db_password = os.getenv("DATABASE_PASSWORD", "not-set")

    # Simulate some periodic task
    now = datetime.datetime.now()
    print(f"[{now}] Running periodic task in {app_env} environment")
    print(f"[{now}] Using database password: {db_password[:3]}***")  # don't print full secret

    # Example: write to a log file inside container (optional)
    with open("/tmp/cronjob.log", "a") as f:
        f.write(f"[{now}] Task ran in {app_env} environment\n")

if __name__ == "__main__":
    main()
