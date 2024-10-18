   import subprocess
   from gpiozero import Button
   from signal import pause

   # GPIO pin assignment for toggle switch
   TOGGLE_SWITCH_PIN = 21

   # Initialize toggle switch
   toggle_switch = Button(TOGGLE_SWITCH_PIN, pull_up=False, bounce_time=0.5)

   # Define Network Manager connection names
   AP_MODE = "qfnet"
   CLIENT_MODE = "Your_Main_WiFi"

   def switch_to_ap_mode():
       print("Switching to AP Mode")
       try:
           # Disconnect from any current Wi-Fi
           subprocess.run(["sudo", "nmcli", "connection", "down", CLIENT_MODE], check=True)
           # Activate AP Mode
           subprocess.run(["sudo", "nmcli", "connection", "up", AP_MODE], check=True)
           print("Switched to AP Mode successfully.")
       except subprocess.CalledProcessError as e:
           print(f"Failed to switch to AP Mode: {e}")

   def switch_to_client_mode():
       print("Switching to Client Mode")
       try:
           # Disconnect from AP Mode
           subprocess.run(["sudo", "nmcli", "connection", "down", AP_MODE], check=True)
           # Activate Client Mode
           subprocess.run(["sudo", "nmcli", "connection", "up", CLIENT_MODE], check=True)
           print("Switched to Client Mode successfully.")
       except subprocess.CalledProcessError as e:
           print(f"Failed to switch to Client Mode: {e}")

   def toggle_network():
       if toggle_switch.is_pressed:
           switch_to_ap_mode()
       else:
           switch_to_client_mode()

   # Assign toggle switch event
   toggle_switch.when_pressed = toggle_network
   toggle_switch.when_released = toggle_network

   print("Network switcher is running...")
   pause()