import subprocess
import sys

def main():
    print("Starting Task Management Assistant Agent...")
    # This will invoke `adk web agents --port 8001` using subprocess
    try:
        subprocess.run(["adk", "web", "--port", "8001", "agents"], check=True)
    except KeyboardInterrupt:
        print("\nAgent stopped.")
    except Exception as e:
        print(f"Failed to start agent: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
