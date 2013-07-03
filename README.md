The videos should be in directory `videos`

Landscape videos should be named L&lt;number>_&lt;something>.mov 
    
Person videos should be named P&lt;number>_&lt;something>.mov 

To have blank screen after boot:

Edit /etc/inittab:

Change this:

    1:2345:respawn:/sbin/getty --noclear 38400 tty1 

to this:

    1:2345:off:/sbin/getty --noclear 38400 tty1 

Edit /etc/rc.local, add the following before `exit 0`

    sudo -u pi /home/pi/show/start &
    setterm -blank force


USEFUL INFORMATION
------------------

 - how to put videos on pies -> per ftp, pi@192.168....
  - maybe pure-ftpd? -> yepp, worked very good, just installed it: `pi@raspberrypi ~ $ sudo apt-get install pure-ftpd`
 - debugging information is sent to syslog_host with facility local0
  - to configure syslog on a mac and to direct local0 facility to a file: `host:~ root# echo "local0.* /var/log/pi.log" >> /etc/syslog.conf`
    cd /System/Library/LaunchDaemons
    su
    /usr/libexec/PlistBuddy -c "add :Sockets:NetworkListener dict" com.apple.syslogd.plist
    /usr/libexec/PlistBuddy -c "add :Sockets:NetworkListener:SockServiceName string syslog" com.apple.syslogd.plist
    /usr/libexec/PlistBuddy -c "add :Sockets:NetworkListener:SockType string dgram" com.apple.syslogd.plist
    echo "local0.* /var/log/pi.log" >> /etc/syslog.conf
    launchctl unload com.apple.syslogd.plist
    launchctl load com.apple.syslogd.plist
  - to see log messages from pi on a mac do this in a terminal: `$ tail -f /var/log/pi.log`
