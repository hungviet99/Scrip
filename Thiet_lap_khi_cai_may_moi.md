# Thiết lập khi cài máy mới : 

## CentOS 7: 

Thực hiện với quyền sudo hoặc root

**Install wget**

```
yum install -y wget 
```

**Tải về các script disable ssh, user thuctap**

```
cd
wget https://raw.githubusercontent.com/danghai1996/thuctapsinh/master/HaiDD/Script/ssh/denyIPssh.sh
```

```
https://gist.githubusercontent.com/hungviet99/8884f8f6fdf4c033fac3f1cbae16114c/raw/2caec43a576de0fc2e9cf40fca14963e8c52c550/UserThucTap.sh
```

**Cấp quyền và thực thi**

```
chmod +x denyIPssh.sh
chmod +x UserThucTap.sh
./denyIPssh.sh
./UserThucTap.sh
```

## Ubuntu 

Thực hiện với quyền sudo hoặc root

**Install wget**

```
apt install -y wget 
```

**Tải về các script disable ssh, user thuctap**

```
cd
wget https://raw.githubusercontent.com/danghai1996/thuctapsinh/master/HaiDD/Script/ssh/denyIPssh.sh
```

**Cấp quyền và thực thi**

```
chmod +x denyIPssh.sh
./denyIPssh.sh
```