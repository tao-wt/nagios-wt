#!/usr/bin/env bash
#writer walle

IFS=$' \t\n'
OLDPATH=$PATH
PATH=/bin:/usr/bin
export PATH

if test $# -lt 3
then
	echo syntax error! partition+warning+critical.
	exit 3
fi

while getopts "W:C:P:" opt; do  
	case $opt in  
		W)
			#echo "this is -W the arg is : $OPTARG"
			warning=$OPTARG
			;;  
		C)
			#echo "this is -C the arg is : $OPTARG"  
			critical=$OPTARG
			;;  
		P)
			#echo "this is -P the arg is : $OPTARG"   
			part=$OPTARG
			;; 
	esac  
done

used=$(df -B 1G | egrep "${part}$" | awk '{print $(NF-1)}' | sed 's/%//')
canuseb=$((100-${used}))
canuse=$(df -B 1G | egrep " ${part}$" | awk '{print $(NF-2)}')
if echo $warning | grep '%' >>/dev/null
then
	owarning=$(echo $warning | sed 's/%//')
	ocritical=$(echo $critical | sed 's/%//')
	if [ $ocritical -ge $canuseb ];then
		status="CRITICAL"
		echo DISK CRITICAL - free space: $part is $canuse GB \(used ${used}%\)\| /=GB\;\;\;\;
		exit 2
	elif [ $owarning -ge $canuseb ];then
		status="WARNING"
		echo DISK WARNING - free space: $part is $canuse GB \(used ${used}%\)\| /=GB\;\;\;\;
		exit 1
	else
		stats="OK"
		echo DISK OK - free space: $part is $canuse GB \(used ${used}%\)\| /=GB\;\;\;\;
		exit 0
	fi
else
	if [ $critical -ge $canuse ];then
		status="CRITICAL"
		echo DISK CRITICAL - free space: $part is $canuse GB \(used ${used}%\)\| /=GB\;\;\;\;
		exit 2
	elif [ $warning -ge $canuse ];then
		status="WARNING"
		echo DISK WARNING - free space: $part is $canuse GB \(used ${used}%\)\| /=GB\;\;\;\;
		exit 1
	else
		stats="OK"
		echo DISK OK - free space: $part is $canuse GB \(used ${used}%\)\| /=GB\;\;\;\;
		exit 0
	fi
fi
	