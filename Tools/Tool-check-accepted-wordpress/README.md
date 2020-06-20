# Cấu hình 

Tool python sử dụng để gửi cảnh báo khi có thông tin đăng nhập thành công vào site quản trị của wordpress

Sử dụng trên 2 hệ điều hành là CentOS 7 và Ubuntu.

Thực hiện bằng user với quyền sudo hoặc người dùng root

## Kiểm tra version Python trên máy

Ta kiểm tra xem đã có version 3 của python được cài trong máy chưa. 
```
python3 --version
```

Nếu chưa có phiên bản python 3 trong máy, thực hiện cài đặt python3 

**Đối với CentOS:** 

```
yum install -y python3
```

Cài đặt Modul request

```
yum install -y python3-requests
```
**Đối với Ubuntu:**

```
apt install -y python3
```

Để sử dụng được chương trình này chạy như 1 tiến trình của hệ thống, ta làm như sau : 

## Bước 1: Tải về source code

```
cd /etc
mkdir AlertWP
cd /etc/AlertWP
```

### Tải về file `wpalert.py`: 

```
wget https://raw.githubusercontent.com/hungviet99/Tools_and_Script/master/Tools/Tool-check-accepted-wordpress/wpalert.py
```

### Chỉnh sửa file như sau : 

#### Nhập vào file `Token ID` của Bot Telegram

```
sed -i 's/#TOKEN =/TOKEN = "918364925:AAGbl5y7463f8DFFx4RhkeB3_eRhUUNfHHw"/' /etc/AlertWP/wpalert.py
```

**Lưu ý:** Thay giá trị `918364925:AAGbl5y7463f8DFFx4RhkeB3_eRhUUNfHHw` bằng token ID của bạn. 

#### Nhập vào message ID của Group trong telegram hoặc ID của bạn 

```
sed -i 's|#CHAT_ID =|CHAT_ID = -468923562|' /etc/AlertWP/wpalert.py
```
**Lưu ý:** Thay ID chat `-468923562` bằng ID chat của bạn. 

#### Nhập vào đường dẫn file log wordpress 

```
sed -i 's/#        poll_logfile("")/        poll_logfile("\/var\/log\/httpd\/access_log")/' /etc/AlertWP/wpalert.py
```

**Lưu ý** Thay `/var/log/httpd/access_log` bằng đường dẫn file log wordpress. Với mỗi ký tự / ta phải thêm 1 ký tự \

## Tải về file service

### Tải file 

#### Đối với CentOS

```
cd /usr/lib/systemd/system
```
```
wget https://raw.githubusercontent.com/hungviet99/Tools_and_Script/master/Tools/Tool-check-accepted-wordpress/wpalert.service
```

#### Đối với Ubuntu

```
cd /etc/systemd/system
```

```
wget https://raw.githubusercontent.com/hungviet99/Tools_and_Script/master/Tools/Tool-check-accepted-wordpress/wpalert.service
```

### Chỉnh sửa file `wpalert.service`

Hiển thị đường dẫn tới Python3
```
which python3
```
và sẽ có kết quả tương tự như sau : 

```
/bin/python3
```

Sau khi có được đường dẫn tới python3, ta tiến hành chỉnh sửa file `wpalert.service`

Chỉnh sửa `/bin/python3` và thay bằng đường dẫn hiển thị trên máy bạn

#### Trên CentOS: 
```
sed -i 's|ExecStart=|ExecStart=/bin/python3 /etc/AlertWP/wpalert.py|' /usr/lib/systemd/system/wpalert.service
```
#### Trên Ubuntu: 
```
sed -i 's|ExecStart=|ExecStart=/usr/bin/python3 /etc/AlertWP/wpalert.py|' /etc/systemd/system/wpalert.service
```

### Khởi động dich vụ wpalert 

```
systemctl start wpalert.service
systemctl status wpalert.service
systemctl enable wpalert.service
```

