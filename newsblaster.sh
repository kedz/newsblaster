#!/bin/bash
# Run-level Startup script for the NewsBlaster
#
# description: Startup/Shutdown Oracle listener and instance

# if NB_HOME not set -- display error
if [ -z "$NB_HOME" ]; then
    NB_HOME="$HOME/newsblaster_home"
    mkdir -p "$NB_HOME"
    export NB_HOME
    echo "Setting NB_HOME to $NB_HOME"
else
    echo "Override default NB_HOME with user variable $NB_HOME"
    #Set to users
    NB_HOME=$NB_HOME
fi

# Ensure that NB_HOME was set correctly 
if [ ! -f $NB_HOME/bin/mongo -o ! -d $NB_HOME ]
then
        echo "NewsBlaster: cannot start. Please check your NB_HOME path"
				exit 1	
fi

source $NB_HOME/venv/bin/activate
export PATH=$NB_HOME/bin:$PATH
export LD_LIBRARY_PATH=$NB_HOME/lib
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
DATA_DIR="$NB_HOME/data/db"

cd $DIR/nest

# depending on parameter -- startup, shutdown, restart 
# of the instance and listener or usage display 
case "$1" in
    start)
        echo -n "Starting NewsBlaster: "

        #Mongodb
        $NB_HOME/bin/mongod --dbpath $DATA_DIR --fork --logpath "$DATA_DIR/mongodb.log"

        #Scrapyd	
        scrapyd > /dev/null &

        #Celery
        cd $DIR
        celery worker --app scheduler -l info -E -B -q  --concurrency 1 &> "$DATA_DIR/celery.log" &
        sleep 5			

        echo -ne '\n' 
        echo   "OK"
        ;;
    stop)
        echo -n "Shutdown NewsBlaster: "

        scrapy_pid=`ps aux | grep scrapyd | awk '{print $2}' `
        #echo "Stop scrapyd manually by running: sudo kill -9 $scrapy_pid. Process requires root "
        kill -9 $scrapy_pid	

        celery_pid=`ps aux | grep 'celery worker' | awk '{print $2}'`
        kill -9 $celery_pid	
      
        $NB_HOME/bin/mongo --eval "db.getSiblingDB('admin').shutdownServer()"
        sleep 5

        echo "OK"
        ;;
    reload|restart)
        bash $DIR/newsblaster.sh stop
        sleep 10
        bash $DIR/newsblaster.sh start
        ;;
    *)
        echo "Usage: $0 start|stop|restart|reload"
        exit 1
esac
exit 0

