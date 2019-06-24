# パスワード変更
## Linux
* Ansible調査中
* chpasswdで変更する
    ```bash
    scp new_passwds user01:passwd01@$target_erver_ip
    ssh user01:passwd01@$target_erver_ip "sudo chpasswd < new_passwds"
    ...
    ```
    new_passwds
    ```
    user01:$new_passwd01
    user02:$new_passwd02
    ...
    user06:$new_passwd06
    ```
## MySQL
*  rootパスワード変更:
    ```bash
    mysqladmin -u root -p orignal_passwd password new_passwd
    ```
* 一般ユーザーパスワードと権限変更
    ```SQL
    1. rootでmysqlにログイン：
    mysql -u root -p

    2. 一般ユーザーの確認：
    SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS query FROM mysql.user;

    3. パスワード変更：
    SET PASSWORD FOR 'username'@'host' = PASSWORD('newpassword')；

    4. 権限確認：
    SHOW GRANTS FOR $username;

    5. 権限撤回：
    REVOKE privileges ON database.tablename FROM 'username'@'host';

    6. 実行
    flush privileges;
    ```

* 補足：登録機を限定する
    ```SQL
    use mysql;
    UPDATE user SET host = "$ip_address" WHERE user = "$user_name" AND host = "%";
    flush privileges;
    ```
* ログ確認

## 
# 権限変更
* Webコンテンツと設定ファイルにreadonly属性を設定する
    ```bash
    chattr -R +i /var/www
    lsattr
    ```
* rootをSSHでログインできないようにする
    ```bash
    sudo vim /etc/ssh/sshd_config
    PermitRootLogin no
    PermitEmptyPasswords no
    or comment
    service sshd restart
    ```
* Userのsu権限を限定する
    ```bash
    usermod -G wheel User01 User02 User03 User04 User05 User06
    echo “SU_WHEEL_ONLY yes” >> /etc/login.defs
    vim /etc/pam.d/su
    auth sufficient /lib/security/pam_rootok.so debug
    auth required /lib/security/$ISA/pam_wheel.so group=wheel
    ```
* Userのsudo権限を限定する
    ```bash
    sudo vim /etc/group   -> sudoを整理
    OR
    gpasswd -d $user_name sudo

    sudo visudo
    %sudo ALL=(ALL:ALL) ALL
    ```
* 不要なuserを削除するまたnologinにする
    ```
    userdel –r user_name
    ```
    ```
    sudo vim /etc/passwd
    /bin/bash -> /usr/sbin/nologin or /bin/fasle
    ```
* SSHのポートを変える
    ```
    vim /etc/ssh/ssh_config
    #Port: 22  -> Port : 65535
    service sshd restart
    ```
    firewall setting
    ```
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT
    service iptables save
    ```
* 不要なssh認証情報を確認
    ```
    ls -a /home/User0[1:6]/.ssh/authorized_keys
    ```
* ansible
参考資料：https://ansible-tran.readthedocs.io/en/latest/docs/intro_installation.html
    * install
        ```
        $ sudo yum install ansible
        ```
    * host fileを入れ替え
    * SSH keyを生成する
        ```
        ssh-keygen -t rsa -C KING -P ''
        ssh-copy-id -i ~/.ssh/id_rsa.pub username@[ip,hostname]
        ```
    * playbook depoly_ssh_key.yamlでSSH key.pub を全てのサーバーにに入れる
        ```
        ansible-palybook depoly_ssh_key.yaml
        ```
    * 
