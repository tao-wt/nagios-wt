#!/usr/bin/env bash
# writer walle

IFS=$' \t\n'

if test $# -lt 6
then
	echo syntax error! ip+partition+username+warning+critical+unit.
	exit 3
fi

if [ "X$2" = "Xroot" ];then
	password='333222'
	/usr/bin/expect <<-EOF >>/dev/null
set timeout 90

spawn scp /usr/local/nagios/libexec/check_disk $2\@$1:~
# spawn ssh "$2\@$1"
expect {
	"assword:" {send "$password\r"}
	"yes/no" {
		send "yes\r"
		expect "assword:"
		send "$password\r"
	}
}
expect eof
#interact
EOF

elif [ "X$2" = "Xca_hzcbtsscm" ];then
	password='hzcbtsscm123'
else
	echo user is error
	exit 1
fi

/usr/bin/expect <<-EOF | awk  '$0~/^[D,d][i,I][S,s][K,k]/' | tee check_$$
set timeout 90

spawn ssh "$2\@$1"
expect {
	"assword:" {send "$password\r"}
	"yes/no" {
		send "yes\r"
		expect "assword:"
		send "$password\r"
	}
}
expect "*]*"
send "./check_disk -w $4 -c $5 -u $6 -p $3 \r";
#interact
expect "*]*"
send "exit\r";
expect eof
EOF

if grep -i 'warning' check_$$ >>/dev/null
then
	rm -rf check_$$
	exit 1
elif grep -i 'critical' check_$$ >>/dev/null
then
	rm -rf check_$$
	exit 2
else
	rm -rf check_$$
fi
