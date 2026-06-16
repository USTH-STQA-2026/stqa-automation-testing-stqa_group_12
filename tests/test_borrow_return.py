"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - "Mượn / Trả" tab: role="tab", aria-label="Mượn / Trả"
    - Available books have "Có sẵn" in aria-label, borrowed books have "Đang mượn"
      (*Sách "Có sẵn" có aria-label chứa "Có sẵn", sách "Đang mượn" chứa "Đang mượn"*)
    - Borrow button: 'flt-semantics[role="button"]:has-text("Mượn sách này")'
      (*Nút mượn*)
    - After clicking "Mượn sách này", a confirmation dialog appears — click "Mượn" again
      (*Sau khi click "Mượn sách này" sẽ hiện dialog xác nhận — cần click nút "Mượn" lần nữa*)
    - Return button: 'flt-semantics[role="button"]:has-text("Trả sách")'
      (*Nút trả*)
"""
import os
import re
from playwright.sync_api import expect
from conftest import (
    enable_flutter_semantics, wait_for_flutter,
    login, SCREENSHOT_DIR,
)

BORROW_TAB = 'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'
ACTIVE_LOAN = 'flt-semantics[role="group"][aria-label*="Đang mượn"]'


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → find an "Available" book → click "Mượn sách này" → confirm dialog
        → verify book status changes to "Borrowed".
        (*Đăng nhập → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog
        → kiểm tra sách chuyển sang trạng thái "Đang mượn".*)

    Suggested steps (*Gợi ý các bước*):
        1. login(page, test_config)
        2. Find available book: page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
           (*Tìm sách Có sẵn*)
        3. Click "Mượn sách này" button inside that book card
           (*Click nút "Mượn sách này" trong sách đó*)
        4. Wait for confirmation dialog, re-enable semantics
           (*Đợi dialog xác nhận, bật lại semantics*)
        5. Click "Mượn" button (confirm button in dialog)
           (*Click nút "Mượn" — nút xác nhận trong dialog*)
        6. Assert: "Đang mượn" or "thành công" appears
           (*Assert: "Đang mượn" hoặc "thành công" xuất hiện*)

    ⚠️ Lưu ý: test này cần tài khoản .env đang HOẠT ĐỘNG và chưa đạt giới hạn
        3 sách (theo SRS REQ-04). Khuyến nghị ba.nguyen / dam.tran (docs/test-accounts.md).
    """
    # Arrange — đăng nhập
    login(page, test_config)

    # Act — tìm 1 cuốn sách "Có sẵn", lấy TÊN sách (dòng đầu của aria-label) để theo dõi
    available = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available.wait_for(state="attached", timeout=10000)
    label = available.get_attribute("aria-label") or ""
    book_title = label.split("\n")[0].strip()
    assert book_title, f"Không lấy được tên sách từ card 'Có sẵn': {label!r}"

    # Click nút "Mượn sách này" trong card sách đó
    available.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first.click()

    # Dialog xác nhận -> click nút "Mượn" (khớp CHÍNH XÁC, không khớp "Mượn sách này")
    enable_flutter_semantics(page)
    confirm = page.locator('flt-semantics[role="button"]').filter(
        has_text=re.compile(r"^\s*Mượn\s*$")
    )
    confirm.first.wait_for(state="attached", timeout=8000)
    confirm.first.click()

    # Sang tab "Mượn / Trả" để kiểm chứng phiếu mượn mới (oracle tin cậy qua aria-label)
    enable_flutter_semantics(page)
    page.locator(BORROW_TAB).first.click()
    wait_for_flutter(page, text=book_title, timeout=8000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book.png"))

    # Assert — Strong Oracle (SRS REQ-04): mượn thành công => có phiếu "Đang mượn" cho đúng cuốn vừa mượn
    active = page.locator(ACTIVE_LOAN)
    labels = [active.nth(i).get_attribute("aria-label") or "" for i in range(active.count())]
    assert any(book_title in l for l in labels), \
        f"SRS REQ-04: kỳ vọng có phiếu 'Đang mượn' cho {book_title!r}. Thực tế các phiếu: {labels}"


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
        (*Đăng nhập → chuyển sang tab "Mượn / Trả" → kiểm tra có sách đang mượn.*)

    Hints (*Gợi ý*):
        - Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
        - Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists
          (*Kiểm tra: có sách với aria-label chứa "Đang mượn" hoặc có nút "Trả sách"*)

    ⚠️ Lưu ý: dùng tài khoản đang có sách mượn. Theo Seed Data, ba.nguyen (MEM002)
        đang mượn BOOK003 "Kiểm thử phần mềm nhập môn".
    """
    # Arrange — đăng nhập
    login(page, test_config)

    # Act — chuyển sang tab "Mượn / Trả"
    tab = page.locator(BORROW_TAB).first
    tab.wait_for(state="attached", timeout=10000)
    tab.click()
    wait_for_flutter(page, text="Đang mượn", timeout=8000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrowed_books.png"))

    # Assert — Strong Oracle (SRS REQ-08: thành viên xem phiếu mượn CỦA MÌNH)
    # Thông tin phiếu nằm trong aria-label của group "Đang mượn"
    active = page.locator(ACTIVE_LOAN)
    assert active.count() > 0, \
        "Kỳ vọng có ít nhất 1 phiếu đang mượn. Kiểm tra tài khoản .env có đang mượn sách không."
    label0 = active.first.get_attribute("aria-label") or ""
    # 1) Đúng cuốn sách đang mượn theo Seed Data (ba.nguyen -> BR001 "Kiểm thử phần mềm nhập môn")
    assert "Kiểm thử phần mềm nhập môn" in label0, \
        f"SRS REQ-08: kỳ vọng thấy phiếu BR001 của chính mình. Thực tế: {label0!r}"
    # 2) Phiếu đủ thông tin (REQ-08) và đúng là phiếu CỦA MÌNH (tên thành viên trùng)
    assert "Mã phiếu" in label0 and test_config["display_name"] in label0, \
        f"SRS REQ-08: phiếu thiếu thông tin hoặc không phải của mình: {label0!r}"


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
        (*Đăng nhập → tab "Mượn / Trả" → click "Trả sách" → kiểm tra sách được trả.*)

    Hints (*Gợi ý*):
        - Switch to "Mượn / Trả" tab (*Chuyển tab "Mượn / Trả"*)
        - Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
          (*Tìm nút "Trả sách"*)
        - Click and verify status change or success message
          (*Click và kiểm tra sách chuyển trạng thái hoặc có thông báo thành công*)

    ⚠️ Lưu ý: cần tài khoản đang có sách mượn (vd ba.nguyen — BOOK003 theo Seed Data).
    """
    # Arrange — đăng nhập + vào tab "Mượn / Trả"
    login(page, test_config)
    tab = page.locator(BORROW_TAB).first
    tab.wait_for(state="attached", timeout=10000)
    tab.click()
    wait_for_flutter(page, text="Đang mượn", timeout=8000)
    enable_flutter_semantics(page)

    # Đếm số phiếu "Đang mượn" TRƯỚC khi trả (điều kiện tiên quyết)
    active_loans = page.locator(ACTIVE_LOAN)
    before = active_loans.count()
    assert before > 0, "Cần có ít nhất 1 phiếu 'Đang mượn' để kiểm thử trả sách"

    # Act — click nút "Trả sách" đầu tiên (hệ thống trả ngay, không có dialog xác nhận)
    page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first.click()
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book.png"))

    # Assert — Strong Oracle (SRS REQ-05): trả thành công => số phiếu "Đang mượn" giảm đúng 1
    # (expect tự động chờ tới khi Semantics Tree cập nhật — Smart Wait, không dùng time.sleep)
    expect(active_loans).to_have_count(before - 1, timeout=8000)
