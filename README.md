Hướng dẫn chạy chương trình Python với Pygame

Đây là một trò chơi mô phỏng sử dụng thư viện Pygame, trong đó có hai hình tròn (Đỏ và Xanh) di chuyển trên lưới với các chướng ngại vật.

Yêu cầu hệ thống

· Python 3.x
· Thư viện Pygame

Cài đặt

Bước 1: Cài đặt Python

Nếu chưa có Python, tải và cài đặt từ trang chủ Python.

Bước 2: Cài đặt Pygame

Mở terminal/command prompt và chạy lệnh:

```bash
pip install pygame
```

Bước 3: Tạo file Python

Tạo một file mới với tên game.py và sao chép toàn bộ code đã cho vào file.

Chạy chương trình

Cách 1: Chạy trực tiếp

```bash
python game.py
```

Cách 2: Chạy trong IDE

Mở file game.py trong IDE hỗ trợ Python (như VS Code, PyCharm, IDLE) và nhấn Run.

Hướng dẫn sử dụng

Cách chơi

· Mục tiêu: Hình tròn Đỏ phải bắt được hình tròn Xanh và kéo nó về ô màu Nâu
· Chướng ngại vật: Các ô màu đen là vật cản không thể đi qua
· Di chuyển tự động: Cả hai hình tròn sẽ tự động di chuyển theo thuật toán

Điều khiển

· Nhấn G: Thoát khỏi chương trình
· Click chuột trái:
  · Click vào hình tròn Xanh: Bật/tắt di chuyển của Xanh
  · Click vào hình tròn Đỏ: Bật/tắt di chuyển của Đỏ

Tính năng

· Hệ thống tự động tạo màn chơi ngẫu nhiên với chướng ngại vật
· Thuật toán tìm đường BFS để tìm đường đi ngắn nhất
· Khi Đỏ bắt được Xanh, nó sẽ kéo Xanh về ô Nâu
· Tự động chuyển màn mới khi hoàn thành

Lưu ý

· Chương trình sẽ chạy ở chế độ toàn màn hình
· Để thoát, nhấn phím G
· Nếu gặp lỗi, đảm bảo đã cài đặt đúng phiên bản Pygame và Python

Gỡ lỗi

Nếu gặp lỗi ModuleNotFoundError: No module named 'pygame', hãy chắc chắn rằng:

1. Pygame đã được cài đặt đúng cách
2. Bạn đang sử dụng môi trường Python phù hợp (nếu dùng virtual environment)

Chúc bạn chơi game vui vẻ!
