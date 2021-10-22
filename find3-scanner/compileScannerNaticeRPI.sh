wget https://dl.google.com/go/go1.17.2.linux-armv6l.tar.gz

rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.2.linux-armv6l.tar.gz

rm go1.17.2.linux-armv6l.tar.gz

export PATH=$PATH:/usr/local/go/bin

sudo apt-get install wireless-tools net-tools libpcap-dev bluetooth

go get -u -v github.com/schollz/find3-cli-scanner

mv $GOPATH/bin/find3-cli-scanner /usr/local/bin