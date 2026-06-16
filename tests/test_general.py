"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - Logout button: 'flt-semantics[role="button"]:has-text("Đăng xuất")'
      (*Nút Đăng xuất*)
    - Language switch EN button: 'flt-semantics[role="button"]:has-text("EN")'
      (*Nút chuyển ngôn ngữ EN*)
    - After logout: page returns to login (has "Đăng nhập" button and "Email" input)
      (*Sau đăng xuất: trang quay về login*)
    - After switching to EN: text "Logout", "Borrow", "Search", "Library" may appear
      (*Sau chuyển EN: text tiếng Anh có thể xuất hiện*)
"""
import os
from conftest import (
    enable_flutter_semantics, flutter_click_button, wait_for_flutter,
    login, SCREENSHOT_DIR,
)


def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → click Logout → verify page returns to login screen.
        (*Đăng nhập → click Đăng xuất → kiểm tra quay về trang đăng nhập.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "Đăng xuất" button and click (*Tìm nút "Đăng xuất" và click*)
        3. Wait 3s, re-enable semantics (*Đợi 3s, bật lại semantics*)
        4. Assert: "Đăng nhập" button or Email input exists
           (*Assert: có nút "Đăng nhập" hoặc ô input Email*)
    """
    # Arrange — đăng nhập
    login(page, test_config)

    # Act — click nút "Đăng xuất"
    flutter_click_button(page, "Đăng xuất")
    # Smart Wait: chờ quay về trang đăng nhập (nút "Đăng nhập" xuất hiện lại)
    wait_for_flutter(page, text="Đăng nhập", timeout=8000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "logout.png"))

    # Assert — Strong Oracle (SRS REQ-01): sau đăng xuất phải về màn hình đăng nhập
    login_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng nhập")')
    email_input = page.locator('input[aria-label="Email"]')
    assert login_btn.count() > 0 or email_input.count() > 0, \
        "Sau đăng xuất phải quay về trang đăng nhập (có nút 'Đăng nhập' hoặc ô Email)"
    # ...và không còn ở trạng thái đã đăng nhập
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng xuất" not in sem_text, \
        "Vẫn còn ở trạng thái đã đăng nhập sau khi bấm Đăng xuất"


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → click "EN" button → verify UI switches to English.
        (*Đăng nhập → click nút "EN" → kiểm tra giao diện chuyển sang tiếng Anh.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "EN" button and click (*Tìm nút "EN" và click*)
        3. Wait 2s, re-enable semantics (*Đợi 2s, bật lại semantics*)
        4. Get sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
        5. Assert: "Logout" or "Borrow" or "Library" in sem_text
    """
    # Arrange — đăng nhập (UI mặc định Tiếng Việt theo SRS)
    login(page, test_config)

    # Act — click nút chuyển ngôn ngữ "EN"
    en_btn = page.locator('flt-semantics[role="button"]:has-text("EN")').first
    en_btn.wait_for(state="attached", timeout=8000)
    en_btn.click()
    # Smart Wait: chờ UI đổi sang tiếng Anh (nút đăng xuất đổi thành "Sign out")
    wait_for_flutter(page, text="Sign out", timeout=8000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "switch_language_en.png"))

    # Assert — Strong Oracle: UI thực sự chuyển sang tiếng Anh
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    # 1) Xuất hiện các nhãn UI tiếng Anh cụ thể ("Sign out", "Library — Book Management")
    assert "Sign out" in sem_text, \
        f"Kỳ vọng UI tiếng Anh có 'Sign out'. Thực tế: {sem_text[:200]}"
    assert "Library" in sem_text, \
        f"Kỳ vọng UI tiếng Anh có 'Library'. Thực tế: {sem_text[:200]}"
    # 2) Không còn nhãn tiếng Việt "Đăng xuất" (xác nhận đã đổi, không phải trùng từ)
    assert "Đăng xuất" not in sem_text, \
        "UI vẫn còn tiếng Việt sau khi bấm 'EN'"
