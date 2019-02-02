#!/usr/bin/env bash
#writer walle
#set -e
IFS=$' \t\n'
OLDPATH=$PATH
PATH=/bin:/usr/bin
export PATH

if test $# -lt 5
then
    echo syntax error! host+key+object+warning+critical.
    exit 4
fi

while getopts ":h:k:w:c:o:" opt; do  
    case $opt in  
        h)
            host=$OPTARG
            ;;
        w)
            #echo "this is -W the arg is : $OPTARG"
            warning=$OPTARG
            ;;  
        c)
            #echo "this is -C the arg is : $OPTARG"  
            critical=$OPTARG
            ;;  
        o)
            #echo "this is -P the arg is : $OPTARG"   
            object=$OPTARG
            ;;
        k)
            key=$OPTARG
            ;;
    esac  
done

pushd "/usr/local/nagios" >/dev/null
    if [ "$key" = "ca_hzcbtsscm" ];then
        user="ca_hzcbtsscm"
    else
        user="root"
        scp -r -i cloud_key/${key}.pem nagios root@${host}:~/ >/dev/null
    fi

    if [ "$object" = 'load' ];then
        stdout=$(ssh -i cloud_key/${key}.pem ${user}@${host} "~/nagios/check_load -w $warning,$((warning-2)),$((warning-3)) -c $critical,$((critical-2)),$((critical-3))")
        iload=$(echo $stdout | awk -F\| '{print $1}' | sed 's/.*, \([0-9]*\.[0-9]*\)$/\1/g')
        nohup echo $user:$host:load:$iload >/usr/local/nagios/fifo_nagios &
    elif [ "$object" = 'cbts_mount_env' ];then
        stdout=$(ssh -i cloud_key/${key}.pem ${user}@${host} "~/nagios/check_cbts_share_folder.sh")
    else
        stdout=$(ssh -i cloud_key/${key}.pem ${user}@${host} "~/nagios/check_disk -w $((100-warning))% -c $((100-critical))% -p $object")
    fi
popd >/dev/null

if echo $stdout | grep -i 'CRITICAL' >/dev/null;then
    echo $stdout
    exit 2
elif echo $stdout | grep -i 'WARNING' >/dev/null;then
    echo $stdout
    exit 1
elif echo $stdout | grep -i 'OK' >/dev/null;then
    echo $stdout
    exit 0
else
    echo $stdout
    exit 9
fi

