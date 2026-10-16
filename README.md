# YummyApp - Bài thực hành 7

Dự án thực hành kiểm thử mocking ứng dụng và thiết lập CI cho các chức năng
cơ bản của YummyApp.

## Nội dung đã thực hiện

- Tính tổng giỏ hàng và kiểm tra các tình huống cơ bản.
- Kiểm thử áp mã khuyến mãi: mã hợp lệ, mất mạng, mã không hợp lệ và phiên
  bản hệ điều hành không đáp ứng yêu cầu.
- Dùng `unittest.mock.patch` giả lập GPS để kiểm thử vị trí có nhà hàng, vị
  trí chưa có dữ liệu và tình huống mất tín hiệu GPS.
- Sửa định dạng khóa tọa độ để vị trí GPS `(10.0, 105.0)` trả về đúng danh
  sách nhà hàng.
- Ghim phiên bản các dependencies trong `requirements.txt`.
- Tạo GitHub Actions workflow tại
  `.github/workflows/yummyapp-ci.yml`. Workflow chạy trên Ubuntu với Python
  3.11, cài dependencies, chạy `flake8`, unittest và coverage với ngưỡng
  tối thiểu 80%; đồng thời tải báo cáo HTML coverage lên dưới dạng artifact.
- Lưu log kiểm thử cục bộ và lịch sử Git trong thư mục `logs/`.

## Cấu trúc chính

```text
.
├── .github/
│   └── workflows/
│       └── yummyapp-ci.yml
├── logs/
│   ├── git_history.log
│   └── local_test.log
├── gps_service.py
├── requirements.txt
├── test_yummy_app.py
└── yummy_app.py
```

## Cài đặt môi trường

Tạo virtual environment và cài dependencies đã ghim phiên bản.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Chạy kiểm thử

Các lệnh dưới đây chạy unittest, kiểm tra lint và đo coverage. Quality gate trả
về mã lỗi khác 0 nếu coverage thấp hơn 80%.

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s . -p "test_*.py"
.\.venv\Scripts\python.exe -m flake8 gps_service.py yummy_app.py test_yummy_app.py
.\.venv\Scripts\python.exe -m coverage run -m unittest discover -s . -p "test_*.py"
.\.venv\Scripts\python.exe -m coverage report -m --fail-under=80
.\.venv\Scripts\python.exe -m coverage html
```

### Linux/macOS

```bash
.venv/bin/python -m unittest discover -s . -p "test_*.py"
.venv/bin/python -m flake8 gps_service.py yummy_app.py test_yummy_app.py
.venv/bin/python -m coverage run -m unittest discover -s . -p "test_*.py"
.venv/bin/python -m coverage report -m --fail-under=80
.venv/bin/python -m coverage html
```

Sau lệnh `coverage html`, mở `htmlcov/index.html` để xem báo cáo. Khi chạy trên
GitHub Actions, báo cáo HTML được tải lên trong artifact
`yummyapp-coverage-report`.

Để tạo/cập nhật log kiểm thử cục bộ bằng Bash:

```bash
mkdir -p logs
coverage run -m unittest discover -s . -p "test_*.py" > logs/local_test.log 2>&1
coverage report -m >> logs/local_test.log 2>&1
```

Các nội dung yêu cầu viết tay và chữ ký trên minh chứng cần được người học tự
thực hiện theo hướng dẫn của bài thực hành.
