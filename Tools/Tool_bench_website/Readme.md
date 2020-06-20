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
wgethttps://raw.githubusercontent.com/hungviet99/Tools_and_Script/master/Tools/Tool_bench_website/Benmarkweb.py
```

Sau đó tiến hành chạy lệnh và nhập vào trang web cần becnh : 

```
python3 Benmarkweb.py
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
wget https://raw.githubusercontent.com/hungviet99/Tools_and_Script/master/Tools/Tool_bench_website/Benmarkweb.py
```

Sau đó chạy lệnh để bench 

```
python3 Benmarkweb.py
```


