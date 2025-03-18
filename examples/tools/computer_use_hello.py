from agents import Agent, Runner, function_tool
import os
from playwright.sync_api import sync_playwright
from agents import set_default_openai_key

api_key = os.environ.get("OPENAI_API_KEY")
print(f"OPENAI_API_KEY {api_key}")
set_default_openai_key(api_key)

@function_tool
def capture_screenshot(url: str) -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page_path = "webpage_screenshot.png"
        page.goto(url)
        page.screenshot(path=page_path, full_page=True)
        browser.close()

        return os.path.abspath(page_path)

@function_tool
def list_current_directory_files() -> list:
    return os.listdir('.')

agent = Agent(
      name="Computer Use Agent",
    tools=[capture_screenshot, list_current_directory_files],
)

import asyncio

async def main():
    result = await Runner.run(agent, input="Capture a screenshot of 'https://example.com' and list all files in the current directory.")
    print("Agent Output:", result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
