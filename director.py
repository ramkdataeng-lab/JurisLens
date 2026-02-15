
import os
import pygame
import time

AUDIO_DIR = "voiceovers"

def run_director():
    # Initialize Pygame Mixer
    pygame.mixer.init()
    
    # Get sorted audio files
    files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")])
    
    if not files:
        print(f"❌ No audio files found in '{AUDIO_DIR}'. Did you run generate_voiceover.py?")
        return

    print("\n🎬 **DIRECTOR MODE ACTIVATED** 🎬")
    print("-----------------------------------")
    print("INSTRUCTIONS:")
    print("1. Start your Screen Recording software (OBS, Loom, etc.).")
    print("2. Focus on your Browser window with JurisLens open.")
    print("3. Keep this terminal visible on a second screen (or minimized).")
    print("4. Press [ENTER] to play the next audio clip when you are ready.")
    print("-----------------------------------")
    
    current_index = 0
    total_clips = len(files)
    
    while current_index < total_clips:
        filename = files[current_index]
        clip_name = os.path.splitext(filename)[0]
        
        # Wait for user trigger
        input(f"\n👉 Press [ENTER] to play Clip {current_index + 1}/{total_clips}: '{clip_name}'...")
        
        # Load and Play
        filepath = os.path.join(AUDIO_DIR, filename)
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        
        print(f"🔊 Playing: {clip_name}...")
        
        # Wait for playing to finish (optional blocking, or non-blocking)
        # We'll monitor is_busy() to show a "Playing..." indicator
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        print("✅ Finished.")
        current_index += 1
        
    print("\n🎉 PERFORMANCE COMPLETE. Stop your recording now!")

if __name__ == "__main__":
    run_director()
