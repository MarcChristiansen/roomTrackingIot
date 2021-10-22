wget https://dl.google.com/go/go1.17.2.linux-armv6l.tar.gz

rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.2.linux-armv6l.tar.gz

rm go1.17.2.linux-armv6l.tar.gz

export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go


