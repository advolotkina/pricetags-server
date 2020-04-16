#!/usr/bin/expect
set address [lindex $argv 0]
set password "12345678"
spawn ssh-copy-id root@$address

expect "Are you sure you want to continue connecting (yes/no)?"
send -- "yes\r"
expect "*"
expect "root@$address\'s password:*"
send -- "$password\r"
expect eof