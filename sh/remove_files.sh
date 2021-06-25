#!/bin/bash
#ex: 59 23 * * * /var/www/spdpaas/regularly/remove_files.sh /var/www/html/CHUNZU/csvfile all
path=$1
file=$2

if [ "$2" = "all" ]
then
    for file in "$path"/*; do
        [[ $file = "${filename}" ]] || rm "${file}"
    done
else
    if [ -f "$path/$file" ]; then
        rm $path/$file
    fi
fi