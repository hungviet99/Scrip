# Cài đặt và sử dụng Tool 

Tool viết bằng bash shell, được sử dụng để tự động backup code và database của 1 site wordpress. Sau khi backup sẽ được nén lại, sau đó gửi về 1 máy lưu trữ dữ liệu từ xa và gửi về google dirver. Để chạy tools, ta sẽ cài đặt các mục cần thiết và cấu hình như sau : 

### Bước 1 : Cài đặt các gói cần thiết 

```
yum install -y wget curl 
```

```
cd /root/
wget https://downloads.rclone.org/v1.41/rclone-v1.41-linux-amd64.zip
unzip rclone-v*.zip
\cp rclone-v*-linux-amd64/rclone /usr/sbin/
rm -rf rclone-*
```

### Bước 2: Tạo kết nối tới google driver 

```
rclone config
```

Nếu chưa tạo kết nối thì sẽ có 1 thông báo rằng `No remotes found - make a new one`  

Nhập `n` để tạo kết nối mới 

`name` > Nhập vào tên kết nối, hãy nhập vào `backupwp` 

`Storage` > Nhập vào `11` để kết nối tới `Google Drive`

`Client_id` và `Client_secret` để trống và ấn Enter

`Scope` > Nhập vào 1 

`root_folder_id` và `service_account_file` để trống và ấn Enter 

`Use auto config?` > nhập vào n

Sau đó sẽ có 1 đường link hiển thị đại loại như : 

```
https://accounts.google.com/o/oauth2/auth?access_type=offline&client_id=245693815694.apps.googleusercontent.com&redirect_uri=urn%37dgetf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=https%9A%5G%2Fwww.googleapis.com%2Fauth%2Fdrive&state=acec87cj8395hf94kd7k40c1c16e34
```
hãy copy link và dán vào trình duyệt, đăng nhập vào google driver và  cho phép rclone truy cập vào driver của bạn. 

Sau đó sẽ có 1 đoạn mã, hãy copy lại đoạn mã đó. 

![Imgur](https://i.imgur.com/m7e97cn.png)

Quay trở lại server và dán đoạn mã vào `Enter verification code`. 

Tiếp theo bạn sẽ được hỏi rằng `Configure this as a team drive?` 

Nhập `n`  và Enter. 

Nhập `y` và `Enter` để xác nhận. Sau đó nhập `q` và `Enter` để thoát. 

### Bước 3 : Tạo key để 2 máy kết nối với nhau khi backup với scp

Tạo ra 1 cặp khóa. 

Để trống và nhấn Enter tất cả các mục. 

```
ssh-keygen -t rsa
```

Sử dụng lệnh sau để sao chép khóa vào máy chủ từ xa. 

```
ssh-copy-id USER@SERVER
```

- USER và SERVER lần lượt nhập vào user đăng nhập và địa chỉ IP của máy ta sẽ SCP tới. Sau khi chạy, lệnh sẽ yêu cầu nhập vào mật khẩu đăng nhập của máy chủ. Sau khi nhập mật khẩu, 2 máy sẽ kết nối với nhau sử dụng cặp khóa đó. 


### Bước 4 : Tải về và cấu hình Script 

Tải về script 

```
cd /opt

wget https://raw.githubusercontent.com/hungviet99/Tools_and_Script/master/Tools/Tool_backup_code_and_db_wordpress/Backupwp.sh
``` 

Chỉnh sửa cấu hình Script 

**Nhập vào đường dẫn đến thư mục chứa code** 

```
sed -i 's/#FILE_CONFIG=/FILE_CONFIG=\/var\/www\/html/' /opt/Backupwp.sh
```
**Lưu ý:** Thay đường dẫn thư mục `/var/www/html/` bằng đường dẫn thư mục chứa code wordpress của bạn. Với thư mục sẽ đi kèm với dấu `/` thì đối với mỗi dấu `/` ta sẽ phải đặt trước nó dấu `\`. 

**Nhập vào User ssh để truy cập vào server**

```
sed -i 's/#USER_SCP=/USER_SCP=userbkwp/' /opt/Backupwp.sh
```

**Lưu ý:** Thay `userbkwp` bằng user bạn sử dụng để truy cập máy chủ của mình.

**Nhập vào IP của server** 

```
sed -i 's/#IP_SCP=/IP_SCP=10.10.10.10/' /opt/Backupwp.sh
```
**Lưu ý:** thay địa chỉ `10.10.10.10` bằng địa chỉ máy chủ của bạn. 


**Nhập vào đường dẫn thư mục chứa thư mục backup trên server** 

```
sed -i 's/#FILE_SCP=/FILE_SCP=\/home\/userbkwp/' /opt/Backupwp.sh
```

Tại đây mình sử dụng user `sudo` để đẩy file lên server nên đường dẫn file mình sẽ để là `/home/userbkwp`, chính là thư mục home của user. Nếu sử dụng user `root` với được phép đẩy vào thư mục `/root`. Lưu ý rằng thư mục sẽ đi kèm với dấu `/` thì đối với mỗi dấu `/` ta sẽ phải đặt trước nó dấu `\`. 

**Nhập vào token_ID** 

```
sed -i 's/#TOKEN=/TOKEN="918364925:AAGbl5y7463f8DFFx4RhkeB3_eRhUUNfHHw"/' /opt/Backupwp.sh
```
**Lưu ý:** Thay giá trị `918364925:AAGbl5y7463f8DFFx4RhkeB3_eRhUUNfHHw` bằng token ID của bạn.

**Nhập vào message ID** 

```
sed -i 's|#ID=|ID="-468923562"|' /opt/Backupwp.sh
```

**Lưu ý:** Thay ID chat `-468923562` bằng ID chat của bạn.


**Cấp quyền cho file thực thi** 

```
chmod +x /opt/Backupwp.sh
```

### Bước 5: Tạo crontab để tự động backup 

Tạo 1 crontab tự động chạy script để backup vào 0h30 chủ nhật hàng tuần : 

sử dụng lênh 

```
crontab -e
```
 
và ghi vào file những nội dung sau : 

```
30 0 * * 0 /opt/Backupwp.sh
```
sau đó lưu lại file và thoát. 

Như vậy ta đã cấu hình xong script để tự động backup code và DB của wordpress. Mỗi khi backup xong sẽ có 1 tin nhắn được gửi về telegram. 

