# Contiki CoAP CLI

## Requirement
* Python 2.7
* pip

## Installing
* pip install requests (2.19.1)
* pip install beautifulsoup4 (4.6.3)
* npm install coap-cli -g (use sudo to install it.)

## Command Line
* getallmotes
    * Ex : getallmotes fd00::201:1:1:1
    * (get all motes address to created list table)

* list
    * Ex : list
    * (show current list, not last new, if you want new table, just run getallmotes again)

* post
    * Ex : post fd00::202:2:2:2 bcollect thd=5&pp=2
    * (post node's resource and query to node)

* postall
    * Ex : postall bcollect thd=5&pp=2
    * (postall resource and query to node)

* observe
    * Ex : observe fd00::202:2:2:2 bcollect
    * (observing bcollect resource)

* observelist
    * Ex : observelist
    * (show current observing list)

* delete
    * Ex : delete fd00::202:2:2:2
    * (cancel observing node)

* quit
    * Ex : quit
    * (exiting tool, if you want exit, need delete to all motes)