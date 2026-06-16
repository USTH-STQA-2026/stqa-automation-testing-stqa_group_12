# REPORT — Báo cáo Kiểm thử Tự động (A2)

**Nhóm**: Group 12 — Lớp 52ICT2012.L1 — HK2 2025-2026
**Hệ thống test**: Quản lý mượn sách Thư viện ABC — https://stqa.rbc.vn (Flutter Web / CanvasKit)
**Công cụ**: Python + Playwright + pytest
**Tài khoản test (.env)**: `ba.nguyen@email.com` (MEM002 — Hoạt động, đang mượn BOOK003 theo Seed Data)
**Link Github**: https://github.com/USTH-STQA-2026/stqa-automation-testing-stqa_group_12

---

## 1. Cách chạy

```bash
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt
playwright install chromium
pytest -v -s
```

Screenshot minh chứng được lưu tự động vào thư mục `screenshots/`.

---

## 2. Triết lý kiểm thử — Strong Oracle theo SRS

Theo mô hình **RIPR**, một bug chỉ bộc lộ (Revealability) khi **Test Oracle đủ mạnh**. Vì vậy mỗi `assert` trong dự án này **không** chỉ kiểm tra "trang còn sống" (Null Oracle) mà đối chiếu **kết quả mong đợi cụ thể trích từ SRS / Seed Data**:

- Thông báo lỗi đăng nhập lấy đúng câu chữ trong **SRS REQ-01**.
- Kết quả tìm kiếm/lọc được kiểm tra trên **toàn bộ** danh sách card (mọi card phải khớp tiêu chí — REQ-03).
- Mượn/Trả kiểm tra **đổi trạng thái thật** của đúng cuốn sách (REQ-04, REQ-05), không chỉ check không crash.
- Dùng `wait_for_flutter()` (Smart Wait) thay cho `time.sleep()` để test ổn định, không flaky.

---

## 3. Mô tả từng Test Case

### Nhóm 1 — Đăng nhập (`tests/test_login.py`) — SRS REQ-01

| TC | Mô tả | Oracle (kết quả mong đợi) |
|----|-------|----------------------------|
| TC-01 | Đăng nhập thành công (mẫu) | Hiện tên người dùng / nút "Đăng xuất" |
| TC-02 | Sai mật khẩu | Hiện đúng thông báo **"Mật khẩu không đúng"** + KHÔNG đăng nhập |
| TC-03 | Bỏ trống email & mật khẩu | Hiện đúng **"Vui lòng nhập email và mật khẩu"** + vẫn ở trang login |

### Nhóm 2 — Tìm kiếm & Lọc (`tests/test_search.py`) — SRS REQ-03

| TC | Mô tả | Oracle |
|----|-------|--------|
| TC-04 | Tìm theo tên "Flutter" | Thấy "Lập trình Flutter cơ bản" + **mọi** card kết quả chứa "flutter" (case-insensitive) |
| TC-05 | Tìm từ khóa không tồn tại | **0 card sách** + thông báo **"Không tìm thấy sách"** |
| TC-06 | Lọc thể loại "Công nghệ" | **Mọi** card hiển thị đều thuộc thể loại "Công nghệ" |
| TC-07 | Tìm theo tác giả "Nguyễn Minh Đức" | Thấy "Nhập môn lập trình Python" + **mọi** card đúng tác giả |

### Nhóm 3 — Mượn & Trả (`tests/test_borrow_return.py`) — SRS REQ-04, REQ-05, REQ-08

| TC | Mô tả | Oracle |
|----|-------|--------|
| TC-08 | Mượn sách "Có sẵn" | Lấy mã `BOOKxxx` của sách → mượn → **đúng cuốn đó** chuyển sang "Đang mượn" |
| TC-09 | Xem sách đang mượn | Có nút "Trả sách" + thấy đúng phiếu của mình "Kiểm thử phần mềm nhập môn" (BOOK003) |
| TC-10 | Trả sách | Phiếu chuyển sang trạng thái "Đã trả" |

### Nhóm 4 — Chức năng chung (`tests/test_general.py`) — SRS REQ-01

| TC | Mô tả | Oracle |
|----|-------|--------|
| TC-11 | Đăng xuất | Về trang đăng nhập (có nút "Đăng nhập"/ô Email) + "Đăng xuất" biến mất |
| TC-12 | Chuyển ngôn ngữ EN | Xuất hiện "Logout" **VÀ** "Đăng xuất" tiếng Việt biến mất |

---

## 4. Kết quả chạy test

Môi trường: Windows 10, Python 3.12.10, pytest 8.3.4, Playwright 0.6.2 (Chromium).
Lệnh: `pytest -v` → **12 passed in ~2 phút**.

| TC | Kết quả | Ghi chú |
|----|---------|---------|
| TC-01 | ✅ PASS | Đăng nhập thành công (mẫu) |
| TC-02 | ✅ PASS | Hiện đúng "Mật khẩu không đúng" |
| TC-03 | ✅ PASS | Hiện đúng "Vui lòng nhập email và mật khẩu" |
| TC-04 | ✅ PASS | 1 kết quả "Lập trình Flutter cơ bản", mọi card khớp |
| TC-05 | ✅ PASS | 0 card + "Không tìm thấy sách" |
| TC-06 | ✅ PASS | Mọi card thuộc "Công nghệ" |
| TC-07 | ✅ PASS | 2 sách của "Nguyễn Minh Đức" |
| TC-08 | ✅ PASS | Mượn xong → phiếu "Đang mượn" xuất hiện ở tab Mượn/Trả |
| TC-09 | ✅ PASS | Thấy phiếu BR001 của chính mình, đủ thông tin (REQ-08) |
| TC-10 | ✅ PASS | Trả xong → số phiếu "Đang mượn" giảm đúng 1 |
| TC-11 | ✅ PASS | Đăng xuất → về trang đăng nhập |
| TC-12 | ✅ PASS | UI chuyển EN: "Sign out", "Library — Book Management" |

### Ghi chú phát hiện trong quá trình kiểm thử (tinh thần QA)

Việc viết Strong Oracle giúp lộ ra vài đặc điểm thực tế của hệ thống (khác với mô tả gợi ý ban đầu) — đã điều chỉnh oracle cho khớp **hành vi thật**:

1. **Tên/thông tin sách nằm trong `aria-label`** của `flt-semantics[role="group"]`, **không** có trong text content (`all_text_contents()`) một cách ổn định → oracle tìm kiếm/lọc đọc trực tiếp `aria-label`.
2. **Mượn sách**: sau khi xác nhận, card sách trên tab "Sách" mất `aria-label` group → kiểm chứng tin cậy hơn bằng cách sang tab "Mượn / Trả" xác nhận có phiếu "Đang mượn" mới.
3. **Trả sách**: hệ thống trả **ngay**, không có dialog xác nhận → oracle dựa trên việc số phiếu "Đang mượn" giảm đúng 1 (REQ-05).
4. **Chuyển ngôn ngữ**: nhãn đăng xuất tiếng Anh là **"Sign out"** (không phải "Logout" như gợi ý trong file mẫu).

---

## 5. Khai báo sử dụng AI

Nhóm có sử dụng công cụ AI (Claude Code) để sinh khung test code Playwright, sau đó **tự đối chiếu lại với SRS** để bảo đảm mỗi assertion là Strong Oracle (kiểm tra đúng thông báo lỗi / trạng thái / dữ liệu theo SRS và Seed Data), tránh Weak Oracle, dùng đúng helper Flutter CanvasKit và `wait_for_flutter()` thay cho `time.sleep()`.
