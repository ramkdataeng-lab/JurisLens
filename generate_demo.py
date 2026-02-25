import asyncio
from playwright.async_api import async_playwright
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import os
import base64
import sys
import time
import shutil

# Base durations for our minimum sleeps
# Sum = 173.54s (~2m 53s)
DURATIONS = {
    "01_Intro": 10.92,
    "02_TheProblem": 22.87,
    "03_TheBlindSpot": 13.80,
    "04_Solution": 16.13,
    "05_Demo_Ingest": 12.29,
    "06_Demo_AskRule": 12.26,
    "07_Demo_AskAction": 11.26,
    "08_Demo_Result": 20.54,
    "09_Scenario2_Sanctions": 10.03,
    "10_Scenario2_Result": 10.75,
    "11_Closing": 8.71,
    "12_Adoption": 23.98
}

async def wait_for_ai_response(page, max_wait=10):
    print(f"DEBUG: Quick wait for AI (max {max_wait}s)...", flush=True)
    try:
        # Just wait for the progress bar to show up and then vanish quickly
        await page.wait_for_selector("div[class*='bg-gradient-to-r from-teal-400']", state="visible", timeout=3000)
        await page.wait_for_selector("div[class*='bg-gradient-to-r from-teal-400']", state="hidden", timeout=max_wait * 1000)
    except:
        pass

async def record_browser():
    print("DEBUG: record_browser (Fast Mode) started", flush=True)
    screenshot_path = r"images/Chaygpt_screenshot/chat_screenshot.jpg"
    b64_img = ""
    if os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as image_file:
            b64_img = f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"
    
    async with async_playwright() as p:
        print("DEBUG: Launching optimized Fullscreen Demo...", flush=True)
        browser = await p.chromium.launch(
            args=["--start-fullscreen", "--app=https://jurislens.vercel.app/"], 
            headless=False
        )

        context = await browser.new_context(
            record_video_dir=".",
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        
        page = await context.new_page()

        print("DEBUG: Scene 1: Intro", flush=True)
        await page.goto("https://jurislens.vercel.app/")
        await page.wait_for_load_state("networkidle")
        
        # Keep things moving with a heartbeat
        await page.evaluate("""() => {
            const div = document.createElement('div');
            div.style.position = 'fixed';
            div.style.bottom = '0';
            div.style.right = '0';
            div.style.width = '1px';
            div.style.height = '1px';
            div.style.background = 'transparent';
            div.id = 'v-heartbeat';
            document.body.appendChild(div);
            let frame = 0;
            function animate() {
                frame++;
                div.style.opacity = (frame % 2 === 0) ? 0.98 : 1.0;
                requestAnimationFrame(animate);
            }
            animate();
        }""")
        
        start_time = time.time()
        
        # SCENE 1
        await page.wait_for_timeout(DURATIONS["01_Intro"] * 1000)

        # SCENE 2
        print("DEBUG: Scene 2: The Problem", flush=True)
        if b64_img:
            await page.evaluate(f"""() => {{
                let div = document.createElement('div');
                div.id = 'chatgpt-overlay';
                div.style.position = 'fixed';
                div.style.top = '0';
                div.style.left = '0';
                div.style.width = '100vw';
                div.style.height = '100vh';
                div.style.zIndex = '999999';
                div.style.backgroundColor = 'black';
                div.style.backgroundImage = 'url("{b64_img}")';
                div.style.backgroundSize = 'contain';
                div.style.backgroundRepeat = 'no-repeat';
                div.style.backgroundPosition = 'center';
                document.body.appendChild(div);
            }}""")
        await page.wait_for_timeout(DURATIONS["02_TheProblem"] * 1000)

        # SCENE 3
        print("DEBUG: Scene 3: The Blind Spot", flush=True)
        await page.evaluate("""() => {
            let el = document.getElementById('chatgpt-overlay');
            if(el) el.remove();
        }""")
        await page.wait_for_timeout(DURATIONS["03_TheBlindSpot"] * 1000)

        # SCENE 4
        print("DEBUG: Scene 4: The Solution", flush=True)
        await page.evaluate("window.scrollTo({top: 400, behavior: 'smooth'})")
        await page.wait_for_timeout(2000)
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await page.wait_for_timeout((DURATIONS["04_Solution"] - 2) * 1000)

        # SCENE 5
        print("DEBUG: Scene 5: Demo Ingest", flush=True)
        file_input = page.locator("input[type='file']")
        if await file_input.count() > 0:
            await file_input.set_input_files("goliath_bank_internal_policy.pdf")
            await page.wait_for_timeout(1500)
            await page.locator("button:has-text('Sync to Elastic')").click()
        await page.wait_for_timeout((DURATIONS["05_Demo_Ingest"] - 1.5) * 1000)

        # SCENE 6
        print("DEBUG: Scene 6: Ask Rule", flush=True)
        chat_input = page.get_by_placeholder("Analyze compliance risk for client...")
        if await chat_input.count() > 0:
            await chat_input.type("What is the limit for Zylaria?", delay=50) 
            await chat_input.press("Enter")
            await wait_for_ai_response(page, max_wait=6)
        # We don't wait extra here, we want it to move to next audio clip fast
        # But we must ensure the total time for this scene matches the audio DURATIONS["06_Demo_AskRule"] approx
        # Playwright wait_for_timeout accounts for absolute time passed in this scene
        
        # SCENE 7
        print("DEBUG: Scene 7: Ask Action", flush=True)
        await chat_input.type("My client wants to send $4,000 to Zylaria. Is this allowed?", delay=50)
        await chat_input.press("Enter")
        await wait_for_ai_response(page, max_wait=8)

        # SCENE 8
        print("DEBUG: Scene 8: Demo Result", flush=True)
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await page.wait_for_timeout(DURATIONS["08_Demo_Result"] * 1000)

        # SCENE 9
        print("DEBUG: Scene 9: Scenario 2 Sanctions", flush=True)
        await chat_input.type("Can we onboard Ivan Drago?", delay=50)
        await chat_input.press("Enter")
        await wait_for_ai_response(page, max_wait=6)

        # SCENE 10
        print("DEBUG: Scene 10: Scenario 2 Result", flush=True)
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await page.wait_for_timeout(DURATIONS["10_Scenario2_Result"] * 1000)

        # SCENE 11
        print("DEBUG: Scene 11: Closing", flush=True)
        arch_btn = page.locator("button:has-text('Architecture Diagram')")
        if await arch_btn.count() > 0:
            await arch_btn.click()
        await page.wait_for_timeout(DURATIONS["11_Closing"] * 1000)

        # SCENE 12
        print("DEBUG: Scene 12: Adoption", flush=True)
        close_btn = page.locator("button[aria-label='Close']")
        if await close_btn.count() > 0:
            await close_btn.first.click()
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await page.wait_for_timeout(DURATIONS["12_Adoption"] * 1000)

        print("DEBUG: Closing contexts", flush=True)
        video_path_obj = await page.video.path()
        await context.close()
        await browser.close()
        
        if os.path.exists("recorded_browser_new.webm"):
            try: os.remove("recorded_browser_new.webm")
            except: pass
        shutil.copy(video_path_obj, "recorded_browser_new.webm")
        return "recorded_browser_new.webm"

def mix_video_audio(video_path):
    print("DEBUG: mix_video_audio (Standard back-to-back) started", flush=True)
    audio_files = [
        "01_Intro.mp3", "02_TheProblem.mp3", "03_TheBlindSpot.mp3", "04_Solution.mp3",
        "05_Demo_Ingest.mp3", "06_Demo_AskRule.mp3", "07_Demo_AskAction.mp3", "08_Demo_Result.mp3",
        "09_Scenario2_Sanctions.mp3", "10_Scenario2_Result.mp3", "11_Closing.mp3", "12_Adoption.mp3"
    ]
    
    audio_clips = [AudioFileClip(f"voiceovers/{f}") for f in audio_files]
    final_audio = concatenate_audioclips(audio_clips)
    video = VideoFileClip(video_path)
    
    print(f"DEBUG: Audio Duration: {final_audio.duration}s", flush=True)
    print(f"DEBUG: Recorded Video Duration: {video.duration}s", flush=True)
    
    # We force the video to match the audio length. If video is longer, we cut.
    # If video is shorter, the audio will just trail off or we cut both.
    final_duration = min(video.duration, final_audio.duration)
    
    video = video.subclip(0, final_duration)
    final_audio = final_audio.subclip(0, final_duration)
    
    video = video.set_audio(final_audio)
    video.write_videofile("JurisLens_Final_Demo.mp4", codec="libx264", audio_codec="aac", fps=24)
    print("DEBUG: Final MP4 generated.", flush=True)

if __name__ == "__main__":
    for f in os.listdir():
        if f.endswith('.webm'):
            try: os.remove(f)
            except: pass
    try:
        vp = asyncio.run(record_browser())
        mix_video_audio(vp)
        print("DEBUG: FINAL SUCCESS", flush=True)
    except Exception as e:
        print(f"DEBUG: CRITICAL ERROR: {e}", flush=True)
        sys.exit(1)
