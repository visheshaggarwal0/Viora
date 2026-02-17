import sys
import os
import time

# Add the current directory to sys.path to import skills
sys.path.append(os.getcwd())

from skills.system_tools import SystemTools
from skills.web_tools import WebTools
from skills.tools_factory import get_viora_tools

def test_p3_capabilities():
    print("--- Testing System Control & Web Features ---")
    
    # 1. Test Web Reading
    print("\n[1] Testing Web Reading...")
    url = "https://www.example.com"
    print(f"Reading {url}...")
    content = WebTools.read_url(url)
    print(f"Result Preview:\n{content[:200]}...")

    # 2. Test Volume Control (Be careful not to blast ears)
    print("\n[2] Testing Volume Control...")
    print("Muting volume...")
    res = SystemTools.mute_volume()
    print(res)
    time.sleep(1)
    
    print("Unmuting volume...")
    res = SystemTools.unmute_volume()
    print(res)
    
    print("Setting volume to 10%...")
    res = SystemTools.set_volume(10)
    print(res)
    
    # 3. Test Media Control (Simulated)
    print("\n[3] Testing Media Control...")
    print("Sending 'play_pause' command (might toggle music if active)...")
    res = SystemTools.media_control("play_pause")
    print(res)
    time.sleep(1)
    # Toggle back
    SystemTools.media_control("play_pause")

    # 4. Check Registration
    print("\n--- Testing Tools Factory Registration ---")
    tools = get_viora_tools()
    tool_names = [t.name for t in tools]
    
    expected_tools = ["set_volume", "mute_volume", "unmute_volume", "media_control", "read_web_page"]
    for et in expected_tools:
        if et in tool_names:
            print(f"PASS: '{et}' is registered.")
        else:
            print(f"FAIL: '{et}' is NOT registered.")

if __name__ == "__main__":
    test_p3_capabilities()
