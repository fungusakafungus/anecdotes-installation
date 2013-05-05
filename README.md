The videos should be in directory `videos`

Landscape videos should be named L&lt;number>_&lt;something>.mov 
    
Person videos should be named P&lt;number>_&lt;something>.mov 

TODO
----

 - how to put videos on pies -> per ftp, pi@192.168....
  - maybe pure-ftpd? -> yepp, worked very good, just installed it: `pi@raspberrypi ~ $ sudo apt-get install pure-ftpd`
 - how to make the show start on boot (write better `start` script)
 - how to configure distances? they may be different for different pies
  - config file, editable via ftp or locally
 - do we need debugging information, and when, where to show it
  - probably not, in the end it should just work!
 - we need black screen between videos, so we better do not start graphical environment
 - how to clone the sd cards
