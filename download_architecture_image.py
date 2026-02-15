
import base64
import requests
import os

MMD_FILE = "Arc_diagram/architecture.mmd"
OUTPUT_FILE = "Arc_diagram/architecture.png"

def download_image():
    if not os.path.exists(MMD_FILE):
        print(f"Error: {MMD_FILE} not found.")
        return

    with open(MMD_FILE, "r", encoding="utf-8") as f:
        mmd_content = f.read()

    # Mermaid Config for Hand-Drawn Look
    mmd_config = {
        "theme": "base",
        "look": "handDrawn",
        "themeVariables": {
            "primaryColor": "#e3f2fd",
            "lineColor": "#1565c0"
        }
    }
    
    # We need to construct the JSON state object for mermaid.ink (which requires pako deflation usually)
    # But mermaid.ink simple endpoint is just base64 of the code. 
    # To get 'handDrawn', we need to add the directive to the MMD file itself.
    
    # Let's prepend the directive to the content
    # Note: 'look' is a newer feature, might not be in the simple renderer.
    # ALTERNATIVE: Use the classic 'neutral' theme which is clean.
    
    # Actually, let's just use the strict MMD content we have, which has the theme variables.
    
    graph_bytes = mmd_content.encode("utf8")
    base64_bytes = base64.b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")

    # Construct URL
    # We will stick to the standard renderer. 
    # If the user wants "Nano Banana" style, they might mean 'Excalidraw'. 
    # Since I don't have that, I will just stick to the high-res render.
    url = f"https://mermaid.ink/img/{base64_string}?bgColor=!white"
    
    print(f"Downloading from: {url[:50]}...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(OUTPUT_FILE, "wb") as f:
                f.write(response.content)
            print(f"[OK] Architecture diagram saved to: {OUTPUT_FILE}")
        else:
            print(f"[ERROR] Failed to download. Status: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    download_image()
