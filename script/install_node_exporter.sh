#!/bin/bash

set -e; OS=""

f_check_os(){
    echo "Checking your OS..."
    if cat /etc/*release | grep CentOS > /dev/null 2>&1; then {
        if [ $(rpm --eval '%{centos_ver}') == 7 ]; then {
            OS="CentOS_7";
            echo $OS
            return 0
        } else {
            return 1
        } fi
    } else {
        return 1
    } fi
}

f_setup_exporter_centos(){
    if [ $(id -u) -eq 0 ]; then
        if f_check_os; then 
            echo "############## ENABLE PORT 9100 AND DISABLE SELINUX ##############"
            sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
            sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
            setenforce 0 || echo "selinux is disable"
            firewall-cmd --zone=public --add-port=9100/tcp --permanent
            firewall-cmd --reload
            yum install -y wget
        else
            echo "############## ENABLE PORT 9100 ##############"
            apt install -y wget
            ufw allow 9100/tcp
            ufw reload
        fi
        echo "############## DOWNLOAD SOURCE CODE NODE EXPORTER ##############"
        useradd --no-create-home --shell /bin/false node_exporter
        cd /opt
        wget https://github.com/prometheus/node_exporter/releases/download/v0.18.1/node_exporter-0.18.1.linux-amd64.tar.gz
        tar xvf node_exporter-0.18.1.linux-amd64.tar.gz
        cp /opt/node_exporter-0.18.1.linux-amd64/node_exporter /usr/local/bin
        chown node_exporter:node_exporter /usr/local/bin/node_exporter
        rm -rf node_exporter-0.18.1.linux-amd64*

echo "############## CREATE SERVICE NODE EXPORTER ##############"
cat <<EOF >  /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

        systemctl daemon-reload
        systemctl start node_exporter
        systemctl enable node_exporter
    else
        echo "Can dang nhap bang tai khoan root de thuc hien!!!"
    fi
}
f_main(){
    f_setup_exporter_centos
    echo "       ################################"
    echo "       ###### CAI DAT THANH CONG ######"
    echo "       ################################"
}
f_main
exit
