# nagios-ibm-connections
Nagios Plugins for IBM Connections

These Nagios Plugins can be used to monitor an IBM Connections environment.

<b>check_connections_search_index.py</b><br>
This plugin will login to IBM Connections and do a search. Then it will compare the serach index date/time with the actual date/time.<br>
Example check command:<br>
check_connections_search_index.py -H $ARG1$ -w $ARG2$ -c $ARG3$ -u $ARG4$ -p $USER4$<br>
-H: IBM Connections Hostname<br>
-w: warning if search index is older than w hours<br>
-c: critical if search index is older than c hours<br>
-u: username which can login and search the index<br>
-p: password of this user<br>
<br>
Sample results:<br>
<li>Status OK - Search Index date 2015-11-10 12:41:02<br></li>
<li>Status Warning - Search Index older than 4 hours - Search Index date 2015-11-10 12:41:02<br></li>
<li>Status Critical - Search Index older than 8 hours - Search Index date 2015-11-10 12:41:02<br></li>
<br>
<b>check_connections_comm_owners.py</b><br>
This plugin will directly connect to the DB2 database of IBM Connections and will get all Communities without an owner<br>
Example check command:<br>
check_connections_comm_owners.py -H $ARG1$ -u $ARG2$ -p $USER13$ -w $ARG3$ -c $ARG4$<br>
-H: DB2 Hostname or IP address<br>
-u: DB2 username which can search the databases<br>
-p: password of this DB2 user<br>
-w: warning if there are more than w communities without an owner<br>
-c: critical if there are more than c communities without an owner<br>

<br>
Sample results:<br>
<li>Communites are OK, 1 Communities without an owner:<br>
WGC Fotos ID: 0af79ebe-a381-451c-a305-7373w788e7ec<br></li>
<li>Warning - 1 Communities without an owner:<br>
WGC Fotos ID: 0af79ebe-a381-451c-a305-7373w788e7ec<br></li>
<li>Critical - 1 Communities without an owner:<br>
WGC Fotos ID: 0af79ebe-a381-451c-a305-7373w788e7ec<br></li>
<br></li>
<br>
<b>check_connections_comm_updates.py</b><br>
This plugin will directly connect to the DB2 database of IBM Connections and will get all Communities without any activity since x days<br>
Example check command:<br>
check_connections_comm_updates.py -H $ARG1$ -u $ARG2$ -p $USER13$ -w $ARG3$ -c $ARG4$<br>
-H: DB2 Hostname or IP address<br>
-u: DB2 username which can search the databases<br>
-p: password of this DB2 user<br>
-w: warning if there are more than w communities without an owner<br>
-c: critical if there are more than c communities without an owner<br>

<br>
Sample results:<br>
<li>Communites are OK<br></li>
<li>Warning: There are communites which were not updates since 1460 days<br>
WGC Fotos<br>
Eclipse RCP Entwicklungen<br></li>
<li>Critical: There are communites which were not updates since 1460 days<br>
WGC Fotos<br>
Eclipse RCP Entwicklungen<br></li>
<br></li>

