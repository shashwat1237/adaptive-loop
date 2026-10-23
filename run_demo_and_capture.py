import os
import time
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARTIFACT_DIR = r"C:\Users\admin\.gemini\antigravity\brain\f31d380e-4922-4144-93ec-efbe752ebaf3\screenshots"
DOCS_DIR = r"c:\Users\admin\Downloads\broyo\docs\screenshots"

os.makedirs(ARTIFACT_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

def save_screenshot(page, filename, full_page=False):
    artifact_path = os.path.join(ARTIFACT_DIR, filename)
    docs_path = os.path.join(DOCS_DIR, filename)
    page.screenshot(path=artifact_path, full_page=full_page)
    page.screenshot(path=docs_path, full_page=full_page)
    print(f"Saved: {filename}")

def run_demo():
    print("Starting Playwright end-to-end interactive demo...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--window-size=1440,900", "--no-sandbox"]
        )
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Step 1: Open Dashboard
        print("Navigating to http://localhost:3000...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(2)

        # 01_dashboard_landing.png
        save_screenshot(page, "01_dashboard_landing.png")

        # Step 2: Marcus Vance Telemetry & Chart
        print("Capturing Marcus Vance baseline telemetry...")
        page.evaluate("window.scrollTo(0, 300)")
        time.sleep(1)
        save_screenshot(page, "02_marcus_telemetry_protocols.png")

        # Step 3: Trigger Live Analysis for Marcus Vance
        print("Clicking 'Run Adaptive Analysis' for Marcus Vance...")
        page.evaluate("window.scrollTo(0, 150)")
        time.sleep(0.5)
        # Click Run Adaptive Analysis button
        run_button = page.locator('button:has-text("Run Adaptive Analysis")').first
        run_button.click()
        time.sleep(1)

        # 03_marcus_analysis_executing.png
        page.evaluate("window.scrollTo(0, 600)")
        time.sleep(0.5)
        save_screenshot(page, "03_marcus_analysis_executing.png")

        # Wait for analysis to complete (usually 6-8 seconds)
        print("Waiting for Marcus analysis to complete...")
        page.wait_for_selector('text=Synthesized Clinical Recommendation', timeout=60000)
        time.sleep(2)

        # 04_marcus_analysis_completed.png
        page.evaluate("window.scrollTo(0, 850)")
        time.sleep(1)
        save_screenshot(page, "04_marcus_analysis_completed.png")

        # Cooldown to respect Groq TPM bucket
        print("Cooling down 7 seconds to respect Groq TPM rate limit...")
        time.sleep(7)

        # Step 4: Elena Rostova (Confounded Benchmark)
        print("Switching to Elena Rostova (MEM-1002)...")
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)
        page.locator('text=Elena Rostova').click()
        time.sleep(2)

        # 05_elena_confounder_timeline.png
        page.evaluate("window.scrollTo(0, 450)")
        time.sleep(1)
        save_screenshot(page, "05_elena_confounder_timeline.png")

        # Trigger analysis for Elena
        print("Running Adaptive Analysis for Elena Rostova...")
        page.evaluate("window.scrollTo(0, 150)")
        time.sleep(0.5)
        page.locator('button:has-text("Run Adaptive Analysis")').first.click()
        print("Waiting for Elena analysis to complete (up to 60s for Groq LLM)...")
        page.wait_for_selector('text=Synthesized Clinical Recommendation', timeout=60000)
        time.sleep(2)

        # 06_elena_analysis_critic_audit.png
        page.evaluate("window.scrollTo(0, 850)")
        time.sleep(1)
        save_screenshot(page, "06_elena_analysis_critic_audit.png")

        # Cooldown to respect Groq TPM bucket
        print("Cooling down 7 seconds to respect Groq TPM rate limit...")
        time.sleep(7)

        # Step 5: David Chen (Sparse Data / Abstention Guard)
        print("Switching to David Chen (MEM-1003)...")
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)
        page.locator('text=David Chen').click()
        time.sleep(2)

        # Trigger analysis for David
        print("Running Adaptive Analysis for David Chen (evaluating abstention guard)...")
        page.locator('button:has-text("Run Adaptive Analysis")').first.click()
        print("Waiting for David analysis to complete...")
        page.wait_for_selector('text=Principled Abstention Triggered', timeout=60000)
        time.sleep(2)

        # 07_david_abstention_guard.png
        page.evaluate("window.scrollTo(0, 700)")
        time.sleep(1)
        save_screenshot(page, "07_david_abstention_guard.png")

        # Step 6: Add Custom Test Case Member
        print("Opening '+ Add Test Case User' modal...")
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)
        page.locator('button:has-text("Add Test Case User")').click()
        time.sleep(1)

        # Fill in custom test member
        print("Filling custom patient form...")
        page.fill('input[placeholder="e.g. Dr. Julian Croft"]', "Dr. Julian Croft")
        page.fill('input[type="number"][min="18"]', "47")
        page.select_option('select >> nth=0', "MALE") # Biological sex
        # Target cohort
        page.select_option('select >> nth=1', "Cellular Longevity & NAD+ Recovery")
        page.fill('input[required] >> nth=1', "Optimize NAD+ synthesis & mitochondrial fatty acid oxidation")

        # Select Clean Responder
        time.sleep(1)
        # 08_add_member_modal.png
        save_screenshot(page, "08_add_member_modal.png")

        # Submit modal
        print("Submitting custom member form...")
        page.locator('button:has-text("Add Member to Database")').click()
        time.sleep(3)
        page.wait_for_selector('text=Dr. Julian Croft', timeout=15000)

        # 09_custom_member_created.png
        page.evaluate("window.scrollTo(0, 200)")
        time.sleep(1)
        save_screenshot(page, "09_custom_member_created.png")

        # Cooldown before custom member analysis
        print("Cooling down 7 seconds to respect Groq TPM rate limit...")
        time.sleep(7)

        # Step 7: Run Live Analysis for Custom Member
        print("Running Adaptive Analysis for Dr. Julian Croft...")
        page.locator('button:has-text("Run Adaptive Analysis")').first.click()
        print("Waiting for custom member live Groq analysis (up to 60s)...")
        page.wait_for_selector('text=Synthesized Clinical Recommendation', timeout=60000)
        time.sleep(2)

        # 10_custom_member_analysis_result.png
        page.evaluate("window.scrollTo(0, 850)")
        time.sleep(1)
        save_screenshot(page, "10_custom_member_analysis_result.png")

        browser.close()
        print("Demo run completed successfully! All 10 screenshots captured.")

if __name__ == "__main__":
    run_demo()
