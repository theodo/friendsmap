#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="fabriceb"
__date__ ="$Aug 16, 2011 9:44:00 AM$"

projectname = 'amdevelop'

from fabric.api import *
from fabric.contrib.files import exists
import os
from time import strftime

env.use_ssh_config = True
env.roledefs = {'test': ['192.168.101.146'], 'remotetest': ['88.168.237.109:3001'], 'cloud': ['root@allomatch.cloud.theo.do']}
keys = [os.getenv("HOME") + '/.ssh/theodo-deploy', os.getenv("HOME") + '/.ssh/id_rsa']
env.key_filename = [key for key in keys if os.access(key, os.R_OK)]

path = { 'test': '/home/theodo/sfautohost/' + projectname, 'remotetest': '/home/theodo/sfautohost/' + projectname, 'cloud': '/home/theodo/www/allomatch' }

def theodo(command):
  return sudo(command, user='theodo')

def wwwdata(command):
  return sudo(command, user='www-data')

@roles('test')
def mkdir(dir):
  with cd(path[_getrole()]):
    if not exists(path[_getrole()] + '/' + dir, use_sudo=True):
      theodo('mkdir ' + dir)

@roles('test')
def init_test_env():
  with cd(path[_getrole()]):
    if not exists(path[_getrole()] + '/.git', use_sudo=True):
      theodo('git clone git@github.com:Allomatch/Allomatch.git .')

@roles('test')
def install_composer():
  with cd(path[_getrole()]):
    if not exists(path[_getrole()] + '/composer.phar', use_sudo=True):
      theodo('curl -s http://getcomposer.org/installer | php')


@roles('test')
def install():
  if not exists(path[_getrole()], use_sudo=True):
    theodo('mkdir -p ' + path[_getrole()])
  with cd(path[_getrole()]):
    init_test_env()
    mkdir('cache')
    mkdir('log')
    mkdir('sf2/app/logs')
    mkdir('sf2/app/cache')
    run('mount -o remount,acl /')
    run('setfacl -R -m u:www-data:rwx -m u:theodo:rwx sf2/app/cache sf2/app/logs cache log')
    run('setfacl -dR -m u:www-data:rwx -m u:theodo:rwx sf2/app/cache sf2/app/logs cache log')
    if not exists(path[_getrole()] + '/../symfony/v1.0', use_sudo=True):
      theodo('svn co http://svn.symfony-project.com/branches/1.0 ' + path[_getrole()] + '/../symfony/v1.0')
    if not exists(path[_getrole()] + '/lib/symfony', use_sudo=True):
      with cd(path[_getrole()] + '/lib'):
        theodo('ln -s ../../symfony/v1.0/lib symfony')
    if not exists(path[_getrole()] + '/data/symfony', use_sudo=True):
      with cd(path[_getrole()] + '/data'):
        theodo('ln -s ../../symfony/v1.0/data symfony')
    cc()
    install_composer()
    theodo('php checksamples.php ln')
    theodo('sh reset-test-data.sh')


    warn('Before updating the vendors libraries, please create or update environment-wise configuration files (you can refer to the README.md file if needed)')

@roles('test')
def deploy():
  local('git push')
  tag = "%s/%s" % (_getrole(), strftime("%Y/%m-%d-%H-%M-%S"))
  local('git tag -a %s -m "%s"' % (tag, _getrole()))
  local('git push --tags')
  with cd(path[_getrole()]):
    run('git fetch')
    tag = run('git tag -l %s/* | sort | tail -n1' % _getrole())
    run('git checkout ' + tag)
    run('git submodule update --init --recursive')
    run('php symfony propel-build-model')
    run('php symfony -q cc')


@roles('test')
def migrate():
  with cd(path[_getrole()]):
    theodo('php symfony migrate frontend')

@roles('test')
def cc():
  with cd(path[_getrole()]):
    theodo('rm -rf cache/*')

@roles('test')
def getam3db():
  dbfile = wwwdata('find /home/dav/dav_share/am-backups/databases/am3 | sort | grep partial | tail -n 1')
  for line in dbfile.split("\n"):
    if 'partial' in line:
      dbfile = line
      break

  wwwdata('mv ' + dbfile + ' /tmp/')
  filename = dbfile[45:]
  wwwdata('chmod 666 /tmp/' + filename)
  run('cp /tmp/' + filename + ' ~/')
  get(filename, '.')
  local('bunzip2 -f ' + filename)
  local('mysql -uamdbuser -pdevpwd am3 < ' + filename[:-4])

@roles('test')
def getsugarcrmdb():
  dbfile = wwwdata('find /home/dav/dav_share/am-backups/databases/sugarcrm | sort | grep full | tail -n 1')
  wwwdata('mv ' + dbfile + ' /tmp/')
  filename = dbfile[50:]
  wwwdata('chmod 666 /tmp/' + filename)
  run('cp /tmp/' + filename + ' ~/')
  get(filename, '.')
  local('bunzip2 -f ' + filename)
  local('mysql -uamdbuser -pdevpwd sugarcrm < ' + filename[:-4])



def _getrole():
  if env.host_string in env.roledefs['remotetest']:
    return 'remotetest'
  elif env.host_string in env.roledefs['cloud']:
    return 'cloud'
  else:
    return 'test'