"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
      (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
      (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
      (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
"""
import os
from conftest import (
    enable_flutter_semantics, flutter_fill, wait_for_flutter,
    login, SCREENSHOT_DIR,
)

SEARCH_BOX = "Tìm kiếm theo tên sách hoặc tác giả..."
CATEGORY_BOX = "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
BOOK_CARD = 'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
        (*Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.*)

    Hints (*Gợi ý*):
        - login(page, test_config)
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
        - Verify: page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0
    """
    # Arrange — đăng nhập
    login(page, test_config)

    # Act — tìm theo tên "Flutter"
    flutter_fill(page, SEARCH_BOX, "Flutter")
    # Smart Wait: chờ cuốn sách có "Flutter" (BOOK001 — Seed Data) xuất hiện
    wait_for_flutter(page, text="Lập trình Flutter cơ bản", timeout=8000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_name.png"))

    # Assert — Strong Oracle (SRS REQ-03)
    # Lưu ý: tên sách nằm trong aria-label của card (không có trong text content),
    # nên oracle đọc trực tiếp aria-label của từng card.
    cards = page.locator(BOOK_CARD)
    count = cards.count()
    assert count > 0, "Kỳ vọng có ít nhất 1 kết quả cho 'Flutter'"
    labels = [cards.nth(i).get_attribute("aria-label") or "" for i in range(count)]
    # 1) Đúng cuốn sách chứa "Flutter" theo Seed Data phải xuất hiện
    assert any("Lập trình Flutter cơ bản" in l for l in labels), \
        f"Kỳ vọng tìm thấy 'Lập trình Flutter cơ bản'. Thực tế: {labels}"
    # 2) MỌI card sách hiển thị đều khớp từ khóa (case-insensitive theo REQ-03)
    for l in labels:
        assert "flutter" in l.lower(), \
            f"Kết quả không khớp 'Flutter' (vi phạm REQ-03): {l!r}"


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
        (*Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.*)

    Hints (*Gợi ý*):
        - Verify: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count() == 0
    """
    # Arrange — đăng nhập
    login(page, test_config)

    # Act — tìm từ khóa không tồn tại
    flutter_fill(page, SEARCH_BOX, "xyz_khong_ton_tai_12345")
    # Smart Wait: chờ thông báo "Không tìm thấy sách" (SRS REQ-03)
    try:
        wait_for_flutter(page, text="Không tìm thấy sách", timeout=8000)
    except Exception:
        pass  # nếu không thấy -> assert bên dưới sẽ FAIL và lộ bug
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_no_result.png"))

    # Assert — Strong Oracle (SRS REQ-03)
    # 1) Không có card sách nào hiển thị
    cards = page.locator(BOOK_CARD)
    assert cards.count() == 0, \
        f"Kỳ vọng 0 kết quả, thực tế có {cards.count()} sách"
    # 2) Hiển thị đúng thông báo theo SRS
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Không tìm thấy sách" in sem_text, \
        f"SRS REQ-03: kỳ vọng thông báo 'Không tìm thấy sách'. Thực tế: {sem_text[:200]}"


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → enter "Công nghệ" in the category filter → verify all displayed books
        belong to the "Công nghệ" category.
        (*Đăng nhập → nhập "Công nghệ" vào ô lọc thể loại → kiểm tra tất cả sách
        hiển thị đều thuộc thể loại Công nghệ.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
        - Get book list: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
          (*Lấy danh sách sách*)
        - Loop through each book, verify aria-label contains "Công nghệ"
          (*Lặp qua từng sách, kiểm tra aria-label chứa "Công nghệ"*)
    """
    # Arrange — đăng nhập
    login(page, test_config)

    # Act — lọc theo thể loại "Công nghệ"
    flutter_fill(page, CATEGORY_BOX, "Công nghệ")
    # Smart Wait: chờ list cập nhật — neo bằng 1 sách Công nghệ trong Seed Data (BOOK001)
    wait_for_flutter(page, text="Lập trình Flutter cơ bản", timeout=8000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "filter_by_category.png"))

    # Assert — Strong Oracle (SRS REQ-03): MỌI sách hiển thị đều thuộc "Công nghệ"
    cards = page.locator(BOOK_CARD)
    count = cards.count()
    assert count > 0, "Kỳ vọng có sách thuộc thể loại 'Công nghệ'"
    for i in range(count):
        label = cards.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in label, \
            f"Sách không thuộc thể loại 'Công nghệ' (vi phạm REQ-03): {label}"


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
        (*Đăng nhập → tìm kiếm tên tác giả → kiểm tra có kết quả.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
        - Verify: page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0
    """
    # Arrange — đăng nhập
    login(page, test_config)
    author = "Nguyễn Minh Đức"  # Seed Data: tác giả của BOOK001 và BOOK009

    # Act — tìm theo tên tác giả
    flutter_fill(page, SEARCH_BOX, author)
    # Smart Wait: chờ 1 cuốn của tác giả này xuất hiện (BOOK009 — Seed Data)
    wait_for_flutter(page, text="Nhập môn lập trình Python", timeout=8000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author.png"))

    # Assert — Strong Oracle (SRS REQ-03) — đọc qua aria-label của card
    cards = page.locator(BOOK_CARD)
    count = cards.count()
    assert count > 0, f"Kỳ vọng có kết quả cho tác giả '{author}'"
    labels = [cards.nth(i).get_attribute("aria-label") or "" for i in range(count)]
    # 1) Sách của tác giả theo Seed Data phải xuất hiện (BOOK009)
    assert any("Nhập môn lập trình Python" in l for l in labels), \
        f"Kỳ vọng tìm thấy sách của '{author}'. Thực tế: {labels}"
    # 2) MỌI card sách hiển thị đều thuộc tác giả đã tìm
    for l in labels:
        assert author in l, \
            f"Kết quả không phải của tác giả '{author}' (vi phạm REQ-03): {l!r}"
