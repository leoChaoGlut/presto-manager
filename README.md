# presto-manager
presto cluster management

#Usage
'''
cd ${presto_manger_dir}
fab -f presto-manager.py {start|stop|restart|deploy|reload:cmd={all|common|coordinator|worker|common-worker|worker-coordinator}]}
'''