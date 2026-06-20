import time
from actions.open_app import open_app
from actions.computer_control import computer_control

import subprocess
import pyautogui

def get_front_window_bounds():
    script = 'tell application "System Events" to tell (first application process whose frontmost is true) to get {position, size} of window 1'
    try:
        res = subprocess.check_output(['osascript', '-e', script]).decode('utf-8').strip()
        parts = [int(p.strip()) for p in res.split(',')]
        if len(parts) == 4:
            return parts[0], parts[1], parts[2], parts[3]
    except Exception:
        pass
    return None

def cctv_control(parameters: dict, player=None) -> str:
    """
    Controls the Hik-Connect CCTV application.
    Supports opening the app and auto-logging in, and showing specific cameras.
    """
    action = parameters.get("action", "").lower()
    
    if action == "open":
        if player:
            player.write_log("[CCTV] Opening Hik-Connect...")
            
        # 1. Open Hik-Connect
        open_app_params = {"app_name": "Hik-Connect"}
        open_app(parameters=open_app_params, player=player)
        
        # 2. Wait for app to load and become frontmost
        time.sleep(3.0)
        
        # 3. Use geometric coordinates to click "Login/Register" and the password field
        bounds = get_front_window_bounds()
        if bounds:
            x, y, w, h = bounds
            
            # The red "Login/Register" button is located near the center of the window vertically (around 60% down)
            login_btn_x = x + (w // 2)
            login_btn_y = y + int(h * 0.60)-15
            
            if player:
                player.write_log(f"[CCTV] Relative click: Login/Register button ({login_btn_x}, {login_btn_y})")
            
            # Move mouse there first so user can see it, then click
            pyautogui.moveTo(login_btn_x, login_btn_y, duration=0.5)
            pyautogui.click()
            time.sleep(2.5)
            
            # After clicking Login/Register, the actual login form appears.
            # The password input is below the phone number field, around 50% of the window height.
            pass_x = x + (w // 2)
            pass_y = y + int(h * 0.50)
            
            if player:
                player.write_log(f"[CCTV] Relative click: Password field ({pass_x}, {pass_y})")
            pyautogui.moveTo(pass_x, pass_y, duration=0.5)
            pyautogui.click()
            time.sleep(1.0)
        else:
            # Fallback to AI vision if bounds calculation fails
            if player:
                player.write_log("[CCTV] Window bounds failed, using AI fallback...")
            computer_control({"action": "screen_click", "description": "Login by Password"}, player=player)
            time.sleep(2.5)
            computer_control({"action": "screen_click", "description": "password input field"}, player=player)
            time.sleep(1.0)

        # 4. Type the password
        if player:
            player.write_log("[CCTV] Typing password...")
            
        computer_control({"action": "type", "text": "Naimuddin@786"}, player=player)
        time.sleep(0.5)
        
        # 5. Click the Login button
        if bounds:
            x, y, w, h = bounds
            login_submit_x = x + (w // 2)
            login_submit_y = y + int(h * 0.63)
            
            if player:
                player.write_log(f"[CCTV] Clicking Login button ({login_submit_x}, {login_submit_y})")
            
            pyautogui.moveTo(login_submit_x, login_submit_y, duration=0.5)
            # First click
            pyautogui.click()
            # Wait 2 seconds
            time.sleep(2.0)
            # Second click
            pyautogui.click()
            
            # 6. Maximize to full screen
            if player:
                player.write_log("[CCTV] Maximizing to full screen...")
            time.sleep(2.0) # Wait for login to complete
            pyautogui.hotkey("ctrl", "command", "f")

        else:
            computer_control({"action": "press", "key": "enter"}, player=player)
        
        return "Opened Hik-Connect, logged in, and maximized window."
        
    elif action == "show_camera":
        camera_number = parameters.get("camera_number", "1")
        if player:
            player.write_log(f"[CCTV] Showing camera {camera_number}...")
            
        # Use AI vision to find the camera element on screen and double click it
        description = f"Camera {camera_number} or Video {camera_number}"
        
        # First, find the coordinates
        find_result = computer_control({"action": "screen_find", "description": description}, player=player)
        
        if find_result and find_result != "NOT_FOUND":
            try:
                # The result is expected to be "x,y"
                x_str, y_str = find_result.split(",")
                x, y = int(x_str.strip()), int(y_str.strip())
                
                # Double click the camera
                computer_control({
                    "action": "double_click", 
                    "x": x, 
                    "y": y
                }, player=player)
                return f"Found and selected Camera {camera_number}."
            except Exception as e:
                print(f"[CCTV] Failed to parse coordinates from '{find_result}': {e}")
                return f"Failed to select Camera {camera_number}: coordinate parsing error."
        else:
            return f"Could not locate Camera {camera_number} on the screen."
            
    else:
        return f"Unknown cctv_control action: {action}"
