if [ -z "$NB_HOME" ]; then
    NB_HOME="$HOME/newsblaster_home"
		mkdir -p "$NB_HOME"
		set NB_HOME
    echo "Setting NB_HOME to $NB_HOME."
else
		echo "Override default NB_HOME with user variable $NB_HOME"
		#Set to users 
		NB_HOME=$NB_HOME
fi 

BIN_DIR="$NB_HOME/bin"
SRC_DIR="$NB_HOME/src"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Create bin directory to be used by NewsBlaster
if [ ! -d $BIN_DIR ]; then
		echo "Creating bin directory"
		mkdir -p "$BIN_DIR"
fi

export PATH=$BIN_DIR:$PATH

# Creates install  dependencies directory
if [ ! -d $SRC_DIR ]; then
		echo "Creating source directory"
		mkdir -p "$SRC_DIR"
fi

#-------------------------------------------------------#
# Start installing and compiling required sources here  #
#-------------------------------------------------------#

ERL_PATH="$BIN_DIR/erl"
if [ ! -f $ERL_PATH ]; then
		echo "Downloading & installing erlang "
		cd "$SRC_DIR"
    curl -O http://www.erlang.org/download/otp_src_17.1.tar.gz
    tar zxvf otp_src_17.1.tar.gz
    cd otp_src_17.1
    ./configure --prefix=$NB_HOME
    make 
    make install
fi

if [ ! -f "$BIN_DIR/rabbitmq-server" ]; then
		cd "$SRC_DIR"
    curl -O http://www.rabbitmq.com/releases/rabbitmq-server/v3.3.5/rabbitmq-server-generic-unix-3.3.5.tar.gz
    tar zxvf rabbitmq-server-generic-unix-3.3.5.tar.gz
	
		cd rabbitmq_server-3.3.5
		rmq_temp=`pwd`
	
		ln -s "$rmq_temp/sbin/rabbitmq-server" "$BIN_DIR/rabbitmq-server"
		ln -s "$rmq_temp/sbin/rabbitmq-env" "$BIN_DIR/rabbitmq-env"
		ln -s "$rmq_temp/sbin/rabbitmq-plugins" "$BIN_DIR/rabbitmq-plugins"
		ln -s "$rmq_temp/sbin/rabbitmqctl" "$BIN_DIR/rabbitmqctl"
		
		# Create default broker username and pass
    echo "Add nlp user to RabbitMQ"
		$BIN_DIR/rabbitmq-server > /dev/null & 
		sleep 30
		$BIN_DIR/rabbitmqctl add_user nlp columbia
		$BIN_DIR/rabbitmqctl set_user_tags nlp administrator
		$BIN_DIR/rabbitmqctl set_permissions -p / nlp ".*" ".*" ".*"
		$BIN_DIR/rabbitmq-plugins enable rabbitmq_management	

		#Stop RabbitMQ
		$BIN_DIR/rabbitmqctl stop

fi


if [ ! -f $NB_HOME/lib/libxml2.a ]; then
		cd "$SRC_DIR"
    curl -O http://xmlsoft.org/sources/libxml2-2.9.1.tar.gz
    tar zxvf libxml2-2.9.1.tar.gz
    cd libxml2-2.9.1
    ./configure --prefix=$NB_HOME
    make
    make install
fi

if [ ! -f $NB_HOME/lib/libxslt.a ]; then
		cd "$SRC_DIR"
    curl -O http://xmlsoft.org/sources/libxslt-1.1.28.tar.gz
    tar zxvf libxslt-1.1.28.tar.gz
    cd libxslt-1.1.28
    ./configure --prefix=$NB_HOME
    make
    make install
fi

if [ ! -f $BIN_DIR/elasticsearch ]; then
		cd "$SRC_DIR"
    curl -O https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.2.tar.gz
    tar -zxvf elasticsearch-1.4.2.tar.gz

		cd elasticsearch-1.4.2
		es_temp=`pwd`

		ln -s "$es_temp/bin/elasticsearch" "$BIN_DIR/elasticsearch"
		ln -s "$es_temp/bin/elasticsearch.in.sh" "$BIN_DIR/elasticsearch.in.sh"
		
		#Set Indices
		$NB_HOME/bin/elasticsearch > /dev/null &
		sleep 15
		bash $DIR/setup/es_setup.sh 
		sleep 5
		curl -XPOST 'http://localhost:9200/_cluster/nodes/_local/_shutdown'
fi

if [ ! -f $BIN_DIR/java ]; then
		OS_TYPE=`uname`
    cd "$SRC_DIR"

    if [ "$OS_TYPE" != "Darwin" ]; then
        echo "Installing Java for Linux"
		    curl -O -v -j -k -L -H  "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u67-b01/jdk-7u67-linux-x64.tar.gz
        tar -zxvf jdk-7u67-linux-x64.tar.gz
		    cd jdk1.7.0_67
		    jdk_temp=`pwd`
		    ln -s "$jdk_temp/bin/java" "$BIN_DIR/java"
    else
        echo "Installing Java for OSX"
		    curl -O -v -j -k -L -H  "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u72-b14/jre-7u72-macosx-x64.tar.gz
        tar -zxvf jre-7u72-macosx-x64.tar.gz
        cd jre1.7.0_72.jre/Contents/Home	    
        jdk_temp=`pwd`
		    ln -s "$jdk_temp/bin/java" "$BIN_DIR/java"
    fi
fi

#exit 1
#Exports
export LD_LIBRARY_PATH=$NB_HOME/lib
set LD_LIBRARY_PATH
export LIBRARY_PATH=$NB_HOME/lib
export C_INCLUDE_PATH=$NB_HOME/include:$NB_HOME/include/libxml2
export CPLUS_INCLUDE_PATH=$NB_HOME/include/libxslt/:$NB_HOME/include/libexslt

cd $NB_HOME
if [ ! -d $NB_HOME/venv ]; then
		pip install virtualenv
		virtualenv venv
fi

source venv/bin/activate
pip install lxml
pip install -U setuptools
pip install -U cython
pip install service_identity
pip install scrapy
pip install pyyaml
pip install pika 
pip install scrapyd
pip install Celery
pip install requests
pip install elasticsearch
pip install -U numpy scipy scikit-learn
pip install BeautifulSoup
pip install scipy
