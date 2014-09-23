if [ -z "$NB_HOME" ]; then
    echo "Please set NB_HOME in env.sh and source env.sh before installing."
    exit 1
fi 


# Install dependencies
mkdir -p ${NB_HOME}/src
cd ${NB_HOME}/src

if [ ! -d ${NB_HOME}/lib/erlang ]; then
    wget http://www.erlang.org/download/otp_src_17.1.tar.gz
    tar zxvf otp_src_17.1.tar.gz
    cd otp_src_17.1
    ./configure --prefix=${NB_HOME}
    make 
    make install

fi

if [ ! -f ${NB_HOME}/sbin/rabbitmq-server ]; then
    wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.3.5/rabbitmq-server-generic-unix-3.3.5.tar.gz
    tar zxvf rabbitmq-server-generic-unix-3.3.5.tar.gz
    cp -r ${NB_HOME}/src/rabbitmq_server-3.3.5  ${NB_HOME}/lib/erlang/lib/
    cp -r ${NB_HOME}/src/rabbitmq_server-3.3.5/sbin ${NB_HOME}/sbin
fi

if [ ! -f ${NB_HOME}/lib/libxml2.a ]; then
    wget http://xmlsoft.org/sources/libxml2-2.9.1.tar.gz
    tar zxvf libxml2-2.9.1.tar.gz
    cd libxml2-2.9.1
    ./configure --prefix=${NB_HOME}
    make
    make install
fi

if [ ! -f ${NB_HOME}/lib/libxslt.a ]; then
    wget http://xmlsoft.org/sources/libxslt-1.1.28.tar.gz
    tar zxvf libxslt-1.1.28.tar.gz
    cd libxslt-1.1.28
    ./configure --prefix=${NB_HOME}
    make
    make install
fi


cd $NB_HOME
virtualenv venv
source venv/bin/activate
pip install -U setuptools
pip install -U cython
pip install service_identity
pip install scrapy

