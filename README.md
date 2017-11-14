# presto-manager
presto cluster management

# Requirements
```
pip3 install fabric3
```
# Usage
```
cd ${presto_manger_dir}
```

```
fab -f presto-manager.py {start|stop|restart|deploy|reload:cmd={all|common|coordinator|worker|common-worker|worker-coordinator}]}
```

