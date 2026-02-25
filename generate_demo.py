
import asyncio
from playwright.async_api import async_playwright
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import os
import base64
import sys
import time

# Audio durations for sync
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

async def record_browser():
    print("DEBUG: record_browser started", flush=True)
    screenshot_path = r"images/Chaygpt_screenshot/chat_screenshot.jpg"
    b64_img = ""
    if os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            b64_img = f"data:image/jpeg;base64,{encoded_string}"
    
    async with async_playwright() as p:
        print("DEBUG: Launching browser", flush=True)
        browser = await p.chromium.launch(args=["--start-maximized"], headless=True)
        context = await browser.new_context(
            record_video_dir=".",
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        
        page = await context.new_page()

        print("DEBUG: Scene 1: Intro", flush=True)
        await page.goto("https://jurislens.vercel.app/")
        await page.wait_for_load_state("networkidle")
        
        # Inject constant animation to force Playwright to record idle frames
        await page.evaluate("""() => {
            const div = document.createElement('div');
            div.style.position = 'fixed';
            div.style.bottom = '0';
            div.style.right = '0';
            div.style.width = '1px';
            div.style.height = '1px';
            div.style.background = 'transparent';
            document.body.appendChild(div);
            let frame = 0;
            function animate() {
                frame++;
                div.style.opacity = (frame % 2 === 0) ? 0.99 : 1.0;
                requestAnimationFrame(animate);
            }
            animate();
        }""")
        
        await asyncio.sleep(DURATIONS["01_Intro"])

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
        await asyncio.sleep(DURATIONS["02_TheProblem"])

        print("DEBUG: Scene 3: The Blind Spot", flush=True)
        await page.evaluate("""() => {
            let el = document.getElementById('chatgpt-overlay');
            if(el) el.remove();
        }""")
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(DURATIONS["03_TheBlindSpot"])

        print("DEBUG: Scene 4: The Solution", flush=True)
        await page.evaluate("window.scrollTo({top: 300, behavior: 'smooth'})")
        await asyncio.sleep(3)
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(DURATIONS["04_Solution"] - 3)

        print("DEBUG: Scene 5: Demo Ingest", flush=True)
        file_input = page.locator("input[type='file']")
        if await file_input.count() > 0:
            await file_input.set_input_files("goliath_bank_internal_policy.pdf")
            await asyncio.sleep(2)
            process_btn = page.locator("button:has-text('Sync to Elastic')")
            if await process_btn.count() > 0:
                await process_btn.click()
                print("DEBUG: Clicked Sync to Elastic", flush=True)
            await asyncio.sleep(DURATIONS["05_Demo_Ingest"] - 2)
        else:
            print("DEBUG: File input not found", flush=True)
            await asyncio.sleep(DURATIONS["05_Demo_Ingest"])

        print("DEBUG: Scene 6: Ask Rule", flush=True)
        # 05_Demo_Ingest naturally overflows a little due to playwright execution time, wait slightly less.
        # We also need to let it type. Typing takes 2-3 seconds at 100ms per char. 
        # Zylaria is ~30 chars => 3 seconds.
        chat_input = page.get_by_placeholder("Analyze compliance risk for client...")
        if await chat_input.count() > 0:
            question = "What is the limit for Zylaria?"
            await chat_input.type(question, delay=80) 
            await chat_input.press("Enter")
        # 06_Demo_AskRule duration is 12.26. Subtract typing time ~2.4s.
        await asyncio.sleep(DURATIONS["06_Demo_AskRule"] - 2.5)

        print("DEBUG: Scene 7: Ask Action", flush=True)
        if await chat_input.count() > 0:
            question = "My client wants to send $4,000 to Zylaria. Is this allowed?"
            await chat_input.type(question, delay=80)
            await chat_input.press("Enter")
        # 07_Demo_AskAction duration is 11.26. ~58 chars => 4.6s typing.
        await asyncio.sleep(DURATIONS["07_Demo_AskAction"] - 4.6)
        
        print("DEBUG: Scene 8: Demo Result", flush=True)
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        # API loads take a second maybe
        await asyncio.sleep(DURATIONS["08_Demo_Result"])

        print("DEBUG: Scene 9: Scenario 2 Sanctions", flush=True)
        if await chat_input.count() > 0:
            question = "Can we onboard Ivan Drago?"
            await chat_input.type(question, delay=80)
            await chat_input.press("Enter")
        # 09_Scenario2_Sanctions is 10.03. ~26 chars => 2.0s typing.
        await asyncio.sleep(DURATIONS["09_Scenario2_Sanctions"] - 2.0)
        
        print("DEBUG: Scene 10: Scenario 2 Result", flush=True)
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await asyncio.sleep(DURATIONS["10_Scenario2_Result"])

        print("DEBUG: Scene 11: Closing", flush=True)
        arch_btn = page.locator("button:has-text('Architecture Diagram')")
        if await arch_btn.count() > 0:
            await arch_btn.click()
        await asyncio.sleep(DURATIONS["11_Closing"])

        print("DEBUG: Scene 12: Adoption", flush=True)
        close_btn = page.locator("button[aria-label='Close']")
        if await close_btn.count() > 0:
            await close_btn.first.click()
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(DURATIONS["12_Adoption"])

        print("DEBUG: Closing contexts", flush=True)
        await context.close()
        await browser.close()
        
        video_files = [f for f in os.listdir(".") if f.endswith(".webm")]
        new_video_path = sorted(video_files, key=os.path.getmtime)[-1]
        print(f"DEBUG: Selected webm: {new_video_path}", flush=True)
        if os.path.exists("recorded_browser_new.webm"):
            os.remove("recorded_browser_new.webm")
        os.rename(new_video_path, "recorded_browser_new.webm")
        return "recorded_browser_new.webm"

def mix_video_audio(video_path):
    print("DEBUG: mix_video_audio started", flush=True)
    clips_names = [
        "01_Intro.mp3", "02_TheProblem.mp3", "03_TheBlindSpot.mp3", "04_Solution.mp3",
        "05_Demo_Ingest.mp3", "06_Demo_AskRule.mp3", "07_Demo_AskAction.mp3", "08_Demo_Result.mp3",
        "09_Scenario2_Sanctions.mp3", "10_Scenario2_Result.mp3", "11_Closing.mp3", "12_Adoption.mp3"
    ]
    audio_clips = [AudioFileClip(f"voiceovers/{name}") for name in clips_names]
    final_audio = concatenate_audioclips(audio_clips)
    video = VideoFileClip(video_path)
    print(f"DEBUG: Durations - Video: {video.duration}, Audio: {final_audio.duration}", flush=True)
    final_duration = min(video.duration, final_audio.duration)
    video = video.subclip(0, final_duration)
    final_audio = final_audio.subclip(0, final_duration)
    video = video.set_audio(final_audio)
    video.write_videofile("JurisLens_Final_Demo.mp4", codec="libx264", audio_codec="aac", fps=24)
    print("DEBUG: mix_video_audio finished", flush=True)

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
