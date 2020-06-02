#!/bin/bash

# Variable
set -e; OS=""

USER="thuctap"
PASS="NhanHoa@2020"

# Check OS
f_check_os(){
    echo "Checking your OS..."
    if cat /etc/*release | grep CentOS > /dev/null 2>&1; then {
        OS="CentOS_"
        if [ $(rpm --eval '%{centos_ver}') == 7 ]; then {
            OS="${OS}7";
            echo $OS
            return 0
        } else {
            return 1
        } fi
    } else {
        return 1
    } fi
}


# Add user thuctap
f_adduser_thuctap(){
	if [ $(id -u) -eq 0 ]; then

		echo "\n____THEM USER thuctap VOI QUYEN SUDO____\n"
		adduser thuctap
		
		echo "\n____NHAP MAT KHAU CHO USER thuctap____\n"
		echo "$PASS" | passwd thuctap --stdin

		
		# Cap quyen sudo
		usermod -aG wheel thuctap

	else
		echo "Can dang nhap bang tai khoan root de thuc hien!!!"
	fi
}

f_main(){
	if f_check_os; then 
		f_adduser_thuctap
		
	else
		echo "\nKHONG PHAI CENTOS-7\n"
	fi

}

f_main

#Disable root

sed -i 's|#PermitRootLogin yes|PermitRootLogin no|' /etc/ssh/sshd_config

#Sudo no Pass

chmod +w /etc/sudoers
echo "%wheel        ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers
chmod -w /etc/sudoers
exit