#!/usr/bin/env bash
set -e
IFS=$' \t\n'
SCRIPT_PATH=$(dirname "${BASH_SOURCE[0]}")

err_disk=''

check_mount(){
    local disk_list="/mnt/CBTS_HZ /mnt/CBTS_ESPOO /build/ltesdkroot /build/rcp /build/cbts_release"
    local err="no"
    for disk in $disk_list
    do
        if ! ${SCRIPT_PATH}/check_disk -w 1% -c 0% -p $disk >/dev/null 2>&1;then
            err="yes"
            err_disk=${err_disk},${disk}
        fi
    done
    if [ "$err" = "yes" ];then
        return 1
    else
        return 0
    fi
}

if check_mount ;then
    echo Share folder OK - All disk mount ok. \|
else
    echo Share folder WARNING - ${err_disk#,} mount error,please check! \|
    exit 1
fi
