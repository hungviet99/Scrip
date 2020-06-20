# Hướng dẫn sử dụng Tools để bench Web site 

Có thể chọn 1 trong 2 hệ điều hành là CentOS 7 hoặc hệ điều hành Ubunntu. 

## CentOS 7 

### Cài đặt Python3 và các modul liên quan 

```
yum update -y
yum install -y python3
yum install -y python3-requests
```


### Tải về tools 

```
yum install -y wget
```

```
cd 
wget https://raw.githubusercontent.com/hungviet99/thuc_tap/master/Ghi_chep_python/Tools/Tool_bench_website/niemthread.py
```

Sau đó tiến hành chạy lệnh và nhập vào trang web cần becnh : 

```
python3 niemthread.py
```

## Ubuntu 

### Cài đặt python3 trên ubuntu 

```
apt update -y
apt-get -y python3 
```

### Tải về Tools 

```
apt install -y wget
```
```
cd 
wget https://raw.githubusercontent.com/hungviet99/thuc_tap/master/Ghi_chep_python/Tools/Tool_bench_website/niemthread.py
```

Sau đó chạy lệnh để bench 

```
python3 niemthread.py
```


