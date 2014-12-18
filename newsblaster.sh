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

echo "Completed check"
exit 1

# depending on parameter -- startup, shutdown, restart 
# of the instance and listener or usage display 

case "$1" in
    start)
        echo -n "Starting NewsBlaster: "
        su - $NB_OWNR -c "$NB_HOME/bin/elasticsearch"
        su - $NB_OWNR -c "$NB_HOME/bin/rabbitmq-server"
        
				#su - $ORA_OWNR -c $ORA_HOME/bin/dbstart
        #touch /var/lock/subsys/oracle
        echo "OK"
        ;;
    stop)
 	# Oracle listener and instance shutdown
        echo -n "Shutdown Oracle: "
        su - $ORA_OWNR -c "$ORA_HOME/bin/lsnrctl stop"
        su - $ORA_OWNR -c $ORA_HOME/bin/dbshut
        rm -f /var/lock/subsys/oracle
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

