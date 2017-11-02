from fabric.api import run, env
from fabric.decorators import roles
from fabric.operations import put
from fabric.tasks import execute

# ========== Config Begin ==========

coordinatorHosts = ['fp-bd5']
workerHosts = ['fp-bd4']

sshUser = 'root'

prestoName = "presto-server-0.186"
prestoTar = prestoName + '.tar.gz'
prestoInstallationDir = '/program'
prestoPackageDir = '/usr/package'

localPrestoTarPath = '/Users/chao.liao/dev/package/linux/bigdata/' + prestoTar

# ========== Config End ==========

env.user = sshUser
env.roledefs = {
    'coordinator': coordinatorHosts,
    'worker': workerHosts,
    'allHost': coordinatorHosts + workerHosts
}


@roles('allHost')
def deployCommonComponent():
    run('mkdir -p ' + prestoPackageDir)
    put(localPrestoTarPath, prestoPackageDir)
    run('mkdir -p ' + prestoInstallationDir)
    run('tar -xf ' + prestoPackageDir + '/' + prestoTar + ' -C ' + prestoInstallationDir)


@roles('allHost')
def configCommon():
    put('common/etc', prestoInstallationDir + '/' + prestoName)
    run('echo "\nnode.id=' + env.host + '" >> ' + prestoInstallationDir + '/' + prestoName + '/etc/node.properties')


@roles('coordinator')
def configCoordinator():
    put('coordinator/etc/config.properties', prestoInstallationDir + '/' + prestoName + '/etc')


@roles('worker')
def configWorker():
    put('worker/etc/config.properties', prestoInstallationDir + '/' + prestoName + '/etc')


@roles('allHost')
def reloadCatalogForAllHost():
    run('rm -r ' + prestoInstallationDir + '/' + prestoName + '/etc/catalog')
    loadCatalogForAllHost()


@roles('allHost')
def loadCatalogForAllHost():
    put('common/etc/catalog', prestoInstallationDir + '/' + prestoName + '/etc')


@roles('allHost')
def startAll():
    run(prestoInstallationDir + '/' + prestoName + '/bin/launcher start')


@roles('allHost')
def stopAll():
    run(prestoInstallationDir + '/' + prestoName + '/bin/launcher stop')


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
