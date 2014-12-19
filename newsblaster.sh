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
if [ ! -f $NB_HOME/bin/java -o ! -d $NB_HOME ]
then
        echo "NewsBlaster: cannot start. Please check your NB_HOME path"
				exit 1	
fi

source $NB_HOME/venv/bin/activate
export PATH=$NB_HOME/bin:$PATH
export LD_LIBRARY_PATH=$NB_HOME/lib
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $DIR/nest

# depending on parameter -- startup, shutdown, restart 
# of the instance and listener or usage display 
case "$1" in
    start)
        echo -n "Starting NewsBlaster: "
        $NB_HOME/bin/elasticsearch > /dev/null &
        $NB_HOME/bin/rabbitmq-server > /dev/null &
				sleep  10	

				python $DIR/setup/broker_setup.py
        sleep 5	
				#Scrapyd	
				scrapyd > /dev/null &
				
				#Celery
				cd $DIR
				celery worker --app scheduler -l info -E -B -q > /dev/null &
				sleep 5			
	
				#Workers
				python $DIR/workers/es_worker.py > /dev/null &
				echo -ne '\n' 
        echo   "OK"
        ;;
    stop)
        echo -n "Shutdown NewsBlaster: "
				curl -XPOST 'http://localhost:9200/_cluster/nodes/_local/_shutdown'

				scrapy_pid=`ps aux | grep scrapyd | awk '{print $2}' `
				kill $scrapy_pid

				celery_pid=`ps aux | grep 'celery worker' | awk '{print $2}'`
				kill -9 $celery_pid	
       
				es_pid=`ps aux | grep 'es_worker' | awk '{print $2}'`
				kill -9 $es_pid	
				
				$NB_HOME/bin/rabbitmqctl stop
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

