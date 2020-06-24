#!/bin/bash 

TODAY=$(date +"%Y-%m-%d")
FOLDER=backupwp-$TODAY
FOLDERSQL=backupsql-$TODAY

# File config là đường dẫn của thư mục chứa code của wordpress. Thường là /var/www/html hoặc cũng có thể là /var/www/public_html, tùy vào từng trang web hoặc cách cấu hình của người quản trị
# Nếu sử dụng web hosting control panel thì đường dẫn có thể lầ /home/user/public_html
#FILE_CONFIG=

# User sử dụng truy cập vào máy chủ từ xa để đẩy file backup lên đó
# VD: root
#USER_SCP=

# Địa chỉ IP của máy đích, nơi file backup sẽ được gửi đến
# VD: 10.10.10.10
#IP_SCP=

# Là nơi lưu file backup trên máy đích. Chỉ rõ đường dẫn đến thư mục đó
# VD: /root/
#FILE_SCP=

#Token là mã token của bot telegram
#TOKEN=

#ID là ID telegram của bạn hoặc có thể là ID của 1 nhóm
#ID=

# Message
URL="https://api.telegram.org/bot$TOKEN/sendMessage"
SUCCESS_DRV=`echo -e "Back up code và DB WordPress lên google driver thành công. \nDate : $TODAY"`
SUCCESS_SCP=`echo -e "Back up code và DB WordPress đến $IP_SCP thành công. \nDate : $TODAY"`
NOSUC_SCP=`echo -e "Không thể backup đến $IP_SCP. \nDate : $TODAY"`
NOSUC_DRV=`echo -e "Không thể backup lên google driver. \nDate : $TODAY"`

# Lay ra DB, User, Pass
DB_NAME=`grep "DB_NAME" $FILE_CONFIG/wp-config.php 2>>/var/log/wpbackup.log| awk '{print $3}' |  tr -d "'"`
DB_USER=`grep "DB_USER" $FILE_CONFIG/wp-config.php 2>>/var/log/wpbackup.log| awk '{print $3}' |  tr -d "'"`
DB_PASSWORD=`grep "DB_PASSWORD" $FILE_CONFIG/wp-config.php 2>>/var/log/wpbackup.log| awk '{print $3}' |  tr -d "'"`

# Tao thu muc backup 
mkdir -p /opt/$FOLDER/backupcode 
cp -r $FILE_CONFIG/* /opt/$FOLDER/backupcode 2>>/var/log/wpbackup.log
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME > /opt/$FOLDER/$FOLDERSQL.sql 2>>/var/log/wpbackup.log

# Nen thu muc backup 
tar -zcf /opt/$FOLDER.tar.gz /opt/$FOLDER   2>>/var/log/wpbackup.log
rm -rf /opt/$FOLDER  2>>/var/log/wpbackup.log

# Backup ve 1 may chu
ping -q -c5 $IP_SCP > /dev/null
if [ $? -eq 0 ]
then
	scp -q -r /opt/$FOLDER.tar.gz $USER_SCP@$IP_SCP:$FILE_SCP  2>>/var/log/wpbackup.log

    curl -s -X POST $URL -d chat_id=$ID -d text="$SUCCESS_SCP" 2>>/var/log/wpbackup.log
else 
    curl -s -X POST $URL -d chat_id=$ID -d text="$NOSUC_SCP" 2>>/var/log/wpbackup.log
fi

# Backup ve driver
rclone mkdir backupwp:/$FOLDER 2>>/var/log/wpbackup.log
rclone move /opt/$FOLDER.tar.gz backupwp:$FOLDER 2>>/var/log/wpbackup.log
if [ $? -eq 0 ]
then
    curl -s -X POST $URL -d chat_id=$ID -d text="$SUCCESS_DRV" 2>>/var/log/wpbackup.log
else 
    curl -s -X POST $URL -d chat_id=$ID -d text="$NOSUC_DRV" 2>>/var/log/wpbackup.log
fi