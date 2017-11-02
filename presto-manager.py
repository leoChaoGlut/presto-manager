from fabric.api import run, env
from fabric.decorators import roles
from fabric.operations import put
from fabric.tasks import execute

coordinatorHosts = ['fp-bd5']
workerHosts = ['fp-bd4']

env.user = 'root'
env.roledefs = {
    'coordinator': coordinatorHosts,
    'worker': workerHosts,
    'allHost': coordinatorHosts + workerHosts
}

prestoName = "presto-server-0.186"
prestoTar = prestoName + '.tar.gz'
localPrestoTarPath = '/Users/chao.liao/dev/package/linux/bigdata/' + prestoTar

pkgDir = '/usr/package'
programDir = '/program'


@roles('allHost')
def deployCommonComponent():
    run('mkdir -p ' + pkgDir)
    put(localPrestoTarPath, pkgDir)
    run('mkdir -p ' + programDir)
    run('tar -xf ' + pkgDir + '/' + prestoTar + ' -C ' + programDir)


@roles('allHost')
def configCommon():
    put('common/etc', programDir + '/' + prestoName)
    run('echo "\nnode.id=' + env.host + '" >> ' + programDir + '/' + prestoName + '/etc/node.properties')


@roles('coordinator')
def configCoordinator():
    put('coordinator/etc/config.properties', programDir + '/' + prestoName + '/etc')


@roles('worker')
def configWorker():
    put('worker/etc/config.properties', programDir + '/' + prestoName + '/etc')


@roles('allHost')
def reloadCatalogForAllHost():
    run('rm -r ' + programDir + '/' + prestoName + '/etc/catalog')
    loadCatalogForAllHost()


@roles('allHost')
def loadCatalogForAllHost():
    put('common/etc/catalog', programDir + '/' + prestoName + '/etc')


@roles('allHost')
def startAll():
    run(programDir + '/' + prestoName + '/bin/launcher start')


@roles('allHost')
def stopAll():
    run(programDir + '/' + prestoName + '/bin/launcher stop')


# ============ Avaliable methods as follow ============

def deploy():
    execute(deployCommonComponent)
    execute(configCommon)
    execute(configCoordinator)
    execute(configWorker)
    execute(loadCatalogForAllHost)
    execute(stopAll)
    execute(startAll)


def reload(cmd='all'):
    cmds = cmd.split('-')
    cmdDict = {}
    for c in cmds:
        cmdDict[c] = True
    print(cmdDict)

    if 'all' in cmdDict.keys():
        execute(configCommon)
        execute(configCoordinator)
        execute(configWorker)
    else:
        if 'common' in cmdDict.keys():
            execute(configCommon)
        if 'coordinator' in cmdDict.keys():
            execute(configCoordinator)
        if 'worker' in cmdDict.keys():
            execute(configWorker)


def start():
    execute(startAll)


def stop():
    execute(stopAll)


def restart():
    execute(stopAll)
    execute(startAll)
