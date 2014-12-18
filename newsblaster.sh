#!/bin/bash
#
# Run-level Startup script for the NewsBlaster
#
# description: Startup/Shutdown Oracle listener and instance

NB_OWNR=`whoami`

# if NB_HOME not set -- display error
if [ -z "$NB_HOME" ]; then
    cd ~
    PWD_PATH=`pwd`
    echo "The path is $PWD"
    NB_HOME="$PWD_PATH/newsblaster_home"
    mkdir -p "$NB_HOME"
    set NB_HOME
    echo "Setting NB_HOME to $NB_HOME"
    echo "Setting OWNER to $NB_OWNER"
else
    echo "Override default NB_HOME with user variable $NB_HOME"
    #Set to users
    NB_HOME=$NB_HOME
fi

if [ ! -f $NB_HOME/bin/java -o ! -d $NB_HOME ]
then
        echo "NewsBlaster: cannot start. Please check your NB_HOME path"
        exit 1
fi

export PATH=$NB_HOME:$PATH

# depending on parameter -- startup, shutdown, restart 
# of the instance and listener or usage display 
case "$1" in
    start)
        echo -n "Starting NewsBlaster: "
        $NB_HOME/bin/elasticsearch > /dev/null &
        $NB_HOME/bin/rabbitmq-server > /dev/null &
        echo "OK"
				echo "Now check article search query here "
        ;;
    stop)
        echo -n "Shutdown NewsBlaster: "
        $NB_HOME/bin/rabbitmqctl stop
				curl -XPOST 'http://localhost:9200/_cluster/nodes/_local/_shutdown'

        echo "OK"
        ;;
    reload|restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Usage: $0 start|stop|restart|reload"
        exit 1
esac
exit 0

