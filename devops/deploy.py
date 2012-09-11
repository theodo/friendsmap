#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="fabriceb"
__date__ ="$Aug 16, 2011 9:44:00 AM$"

projectname = 'friendsmap'

from fabric.api import *
from fabric.contrib.files import exists
import os
from time import strftime

env.use_ssh_config = True
env.roledefs = {'cloud': ['root@friendsmap.cloud.theo.do'], }
env.password = 'root'
keys = [os.getenv("HOME") + '/.ssh/theodo-deploy', os.getenv("HOME") + '/.ssh/id_rsa']
env.key_filename = [key for key in keys if os.access(key, os.R_OK)]

path = { 'cloud': '/home/theodo/www/friendsmap', }

def theodo(command):
  return sudo(command, user='theodo')

def wwwdata(command):
  return sudo(command, user='www-data')

@roles('cloud')
def mkdir(dir):
  with cd(path[_getrole()]):
    if not exists(path[_getrole()] + '/' + dir, use_sudo=True):
      theodo('mkdir ' + dir)

@roles('cloud')
def install_composer():
  with cd(path[_getrole()]):
    if not exists(path[_getrole()] + '/composer.phar', use_sudo=True):
      theodo('curl -s http://getcomposer.org/installer | php')


@roles('cloud')
def install():
  if not exists(path[_getrole()], use_sudo=True):
    theodo('mkdir -p ' + path[_getrole()])
  with cd(path[_getrole()]):
    if not exists(path[_getrole()] + '/.git', use_sudo=True):
      theodo('git clone git@github.com:theodo/friendsmap.git .')
    mkdir('app/logs')
    mkdir('app/cache')
    run('mount -o remount,acl /')
    run('setfacl -R -m u:www-data:rwx -m u:theodo:rwx app/cache app/logs')
    run('setfacl -dR -m u:www-data:rwx -m u:theodo:rwx app/cache app/logs')
    cc()
    install_composer()

    theodo('php composer.phar update')

@roles('cloud')
def deploy():
  local('git push')
  tag = "%s/%s" % (_getrole(), strftime("%Y/%m-%d-%H-%M-%S"))
  local('git tag -a %s -m "%s"' % (tag, _getrole()))
  local('git push --tags')
  with cd(path[_getrole()]):
    run('git fetch')
    tag = run('git tag -l %s/* | sort | tail -n1' % _getrole())
    run('git checkout ' + tag)
    theodo('php composer.phar install')
    theodo('php app/console cache:clear')
    theodo('php app/console assetic:dump')
    theodo('php app/console cache:clear -e prod')
    theodo('php app/console assetic:dump -e prod')

@roles('cloud')
def cc():
  with cd(path[_getrole()]):
    theodo('rm -rf app/cache/*')

def _getrole():
  return 'cloud'
  