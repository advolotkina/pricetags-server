#!/bin/bash
ADDRESS=$1
PATH=$2
/usr/bin/scp $PATH/good.bin root@$ADDRESS:/opt/goods/good1/
/usr/bin/scp $PATH/name root@$ADDRESS:/opt/goods/good1/
/usr/bin/scp $PATH/price root@$ADDRESS:/opt/goods/good1/