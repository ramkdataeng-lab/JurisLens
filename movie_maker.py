import asyncio
from playwright.async_api import async_playwright
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import os

async def record_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--start-maximized"], headless=False)
        context = await browser.new_context(
            record_video_dir=".",
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        print("Scene 1: Introduction (0:00 - 0:40) ---------------------")
        # 01_Intro (10.92), 02_TheProblem (22.87), 03_TheBlindSpot (13.8) = ~47s
        await page.goto("https://jurislens.vercel.app/")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        
        # 01_Intro (10.92s) wait while speaking intro
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await page.wait_for_timeout(9000)

        # 02_TheProblem (22.87s) - Switch to ChatGPT screenshot
        chat_page = await context.new_page()
        chat_img_path = "file:///" + os.path.abspath("images/Chaygpt_screenshot/chat_screenshot.jpg").replace('\\', '/')
        await chat_page.goto(chat_img_path)
        await chat_page.bring_to_front()
        print("  Showing ChatGPT Screen...")
        await chat_page.wait_for_timeout(23000)

        # 03_TheBlindSpot (13.8s) 
        await page.bring_to_front()
        await chat_page.close()
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        # Hover over JurisLens AI header
        header = page.locator("h1")
        if await header.count() > 0:
            await header.first.hover()
        await page.wait_for_timeout(13800)

        print("Scene 2: The Technology (0:40 - 1:10) -------------------")
        # 04_Solution (16.13s)
        hybrid_text = page.locator("text=Hybrid")
        if await hybrid_text.count() > 0:
            await hybrid_text.first.hover()
        await page.wait_for_timeout(8000)
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await page.wait_for_timeout(8100)

        print("Scene 3: Demo - Ingest (1:10 - 1:30) --------------------")
        # 05_Demo_Ingest (12.29s)
        file_input = page.locator("input[type='file']")
        if await file_input.count() > 0:
            await file_input.set_input_files("goliath_bank_internal_policy.pdf")
            await page.wait_for_timeout(2000)
            
            process_btn = page.locator("button:has-text('Process & Index')")
            if await process_btn.count() > 0:
                await process_btn.click()
                print("  Clicked Process & Index")
            
            await page.wait_for_timeout(10300)
        else:
            await page.wait_for_timeout(12300)

        print("Scene 4: THE KILLER MOMENT - ES|QL Audit (1:30 - 2:25) --")
        # 06_Demo_AskRule (12.26s)
        chat_input = page.locator("input[placeholder='Ask a compliance question...']").or_(page.locator("textarea"))
        if await chat_input.count() > 0:
            await chat_input.fill("What is the limit for Zylaria?")
            await chat_input.press("Enter")
        print("  Asked limited for Zylaria")
        await page.wait_for_timeout(12300)

        # 07_Demo_AskAction (11.26s)
        if await chat_input.count() > 0:
            await chat_input.fill("My client wants to send $4,000 to Zylaria. Is this allowed?")
            await chat_input.press("Enter")
        print("  Asked about sending $4,000")
        await page.wait_for_timeout(11300)
        
        # 08_Demo_Result (20.54s)
        await page.wait_for_timeout(6000)
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await page.wait_for_timeout(14500)

        print("Scene 5: Multi-Step Orchestration (2:25 - 2:45) ---------")
        # 09_Scenario2_Sanctions (10.03s)
        if await chat_input.count() > 0:
            await chat_input.fill("Can we onboard Ivan Drago?")
            await chat_input.press("Enter")
        print("  Asked about onboarding Ivan Drago")
        await page.wait_for_timeout(10000)
        
        # 10_Scenario2_Result (10.75s)
        await page.wait_for_timeout(10800)

        print("Scene 6: The Big Finish (2:45 - 3:00) -------------------")
        # 11_Closing (8.71s)
        arch_btn = page.locator("button:has-text('Architecture Diagram')")
        if await arch_btn.count() > 0:
            await arch_btn.click()
        print("  Clicked Architecture Diagram")
        await page.wait_for_timeout(8700)

        # 12_Adoption (23.98s)
        close_btn = page.locator("button[aria-label='Close']")
        if await close_btn.count() > 0:
            await close_btn.first.click()
            
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await page.wait_for_timeout(24000)

        print("Done interacting, saving video... (This might take a moment)")
        await context.close()
        await browser.close()
        
        video_files = [f for f in os.listdir(".") if f.endswith(".webm")]
        if not video_files:
            raise Exception("Video not successfully recorded!")
        video_path = video_files[-1] # the newest one
        
        os.rename(video_path, "recorded_browser_new.webm")
        return "recorded_browser_new.webm"

def mix_video_audio(video_path):
    print("Beginning audio mix...")
    clips_names = [
        "01_Intro.mp3", "02_TheProblem.mp3", "03_TheBlindSpot.mp3", "04_Solution.mp3",
        "05_Demo_Ingest.mp3", "06_Demo_AskRule.mp3", "07_Demo_AskAction.mp3", "08_Demo_Result.mp3",
        "09_Scenario2_Sanctions.mp3", "10_Scenario2_Result.mp3", "11_Closing.mp3", "12_Adoption.mp3"
    ]
    clips = [AudioFileClip(f"voiceovers/{name}") for name in clips_names]
    
    final_audio = concatenate_audioclips(clips)

    video = VideoFileClip(video_path)
    
    print(f"Video duration measured: {video.duration}s")
    print(f"Audio duration measured: {final_audio.duration}s")
    
    # Trim to shortest to avoid out of bounds, but ideally they match close to (~174s)
    final_duration = min(video.duration, final_audio.duration)
    
    video = video.subclip(0, final_duration)
    final_audio = final_audio.subclip(0, final_duration)
    
    video = video.set_audio(final_audio)

    video.write_videofile("demo_video.mp4", codec="libx264", audio_codec="aac", fps=24)

    if os.path.exists(video_path):
        os.remove(video_path)

if __name__ == "__main__":
    for f in os.listdir():
        if f.endswith('.webm'):
            os.remove(f)
            
    vp = asyncio.run(record_browser())
    mix_video_audio(vp)
    print("Done! demo_video.mp4 is ready (full 3 minutes).")
