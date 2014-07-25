ulimit -n
by default it returns 1024

cat /proc/sys/fs/file-max

--
http://stackoverflow.com/questions/2569620/socket-accept-error-24-to-many-open-files/4578356#4578356
http://www.cyberciti.biz/faq/linux-increase-the-maximum-number-of-open-files/

Params that configure max open connections.

at /etc/sysctl.conf (vi /etc/sysctl.conf ; insert ; add lines then :wq)

add:

net.core.somaxconn=131072
fs.file-max=131072

--
and then:

sudo sysctl -p

--
at /usr/include/linux/limits.h

change:

NR_OPEN = 65536

--
at /etc/security/limits.conf

add:

*                soft    nofile          65535
*                hard    nofile          65535
