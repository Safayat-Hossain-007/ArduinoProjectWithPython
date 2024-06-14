import serial
import time
import vlc

# Function to play video using VLC
def play_video(video_path):
    player = vlc.MediaPlayer(video_path)
    player.play()
    return player

# Function to pause video
def pause_video(player):
    if player:
        player.set_pause(1)  # Set pause to 1 to pause the video

# Function to resume video
def resume_video(player):
    if player:
        player.set_pause(0)  # Set pause to 0 to resume the video

# Function to stop video
def stop_video(player):
    if player:
        player.stop()

# Setup serial communication with Arduino
arduino_port = '/dev/ttyACM0'  # Replace with your actual serial port
baud_rate = 9600
arduino = None
sad_played = False  # Flag to track if sad video has been played
sad_paused = False  # Flag to track if sad video is paused

try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Allow time for the serial connection to establish

    print(f"Connected to Arduino on {arduino_port}")

    # Paths to video files
    happy_video_path = "/home/safayat/media/happy_video.mp4"
    sad_video_path = "/home/safayat/media/sad_video.mp4"

    # Start playing happy video
    happy_player = play_video(happy_video_path)
    sad_player = None

    while True:
        if arduino.in_waiting > 0:
            message = arduino.readline().decode('utf-8').strip()
            print(f"Received from Arduino: {message}")

            if message == "MOTION_DETECTED":
                # Pause happy video
                pause_video(happy_player)

                # Check if sad video needs to be resumed or started
                if sad_played and sad_paused:
                    resume_video(sad_player)
                    sad_paused = False  # Reset pause flag
                else:
                    sad_player = play_video(sad_video_path)
                    sad_played = True  # Set flag to indicate sad video has been played

                # Wait for sad video to play for its duration
                time.sleep(10)  # Adjust this time according to your sad video length

                # Pause sad video
                pause_video(sad_player)
                sad_paused = True  # Set flag to indicate sad video is paused

                # Resume happy video
                resume_video(happy_player)

        time.sleep(0.1)  # Small delay to prevent busy-waiting

except serial.SerialException as e:
    print(f"Error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    if arduino and arduino.is_open:
        arduino.close()
    print("Script finished.")
