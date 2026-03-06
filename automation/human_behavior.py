# Human behavior simulation helpers for Playwright automations.
#
# These helpers add natural timing, typing, scrolling, and mouse movement
# to make browser actions look less robotic.

import random
import time


# Sleep for a random amount of time between min_seconds and max_seconds.
def random_delay(min_seconds, max_seconds):
    print("Simulating human delay...")
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


# Type text into a field one character at a time with small random pauses.
def human_type(page, selector, text):
    print("Typing text naturally...")

    if text is None:
        return False

    try:
        # Locate the target field and ensure it exists.
        field = page.locator(selector).first
        if field.count() == 0:
            return False

        # Scroll into view and focus the field.
        field.scroll_into_view_if_needed()
        field.click()

        # Clear current text first so we type from a clean state.
        field.fill("")

        # Type each character with 50-150ms delay.
        for char in str(text):
            field.type(char, delay=random.randint(50, 150))

        return True
    except Exception as exc:
        print(f"Warning: human_type failed for selector '{selector}' ({exc}).")
        return False


# Scroll page gradually in several steps with random short pauses.
def human_scroll(page):
    print("Scrolling page...")

    try:
        steps = random.randint(4, 7)
        for _ in range(steps):
            distance = random.randint(300, 900)
            page.mouse.wheel(0, distance)
            random_delay(0.2, 0.8)
    except Exception as exc:
        print(f"Warning: human_scroll failed ({exc}).")


# Move mouse cursor to random positions to mimic human browsing.
def random_mouse_movement(page):
    try:
        viewport = page.viewport_size or {"width": 1280, "height": 720}
        width = viewport.get("width", 1280)
        height = viewport.get("height", 720)

        # Move cursor through a few random points.
        moves = random.randint(4, 8)
        for _ in range(moves):
            x = random.randint(0, max(width - 1, 1))
            y = random.randint(0, max(height - 1, 1))
            page.mouse.move(x, y, steps=random.randint(5, 20))
            random_delay(0.05, 0.2)
    except Exception as exc:
        print(f"Warning: random_mouse_movement failed ({exc}).")
