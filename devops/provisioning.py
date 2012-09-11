#!/usr/bin/env python

import os
import sys
import logging

from fabric.api import env, run, sudo, cd
from fabric.contrib.files import append, exists

from fabtools import files
from fabtools import service
from fabtools import require

project_name = 'friendsmap'
env.use_ssh_config = True
env.hosts = [project_name + '.cloud.theo.do', ]
env.user = 'root'
env.password = 'root'


def install_bare():
    """
    Installs sudo and configures the local hostname
    - Installs sudo manually to enable fabtools provisioning (not installed on a minimal Debian)
    - Configures the local hostname to avoid future warnings
    """

    run('apt-get update')
    run('apt-get -y --force-yes install sudo')
    append('/etc/hosts', '127.0.0.1 ' + project_name)


def install_dotdeb():
    """
    Installs the dotdeb repository for latest stable PHP and MySQL packages for Debian
    """

    require.deb.package('wget')
    append('/etc/apt/sources.list',
"""deb http://packages.dotdeb.org stable all
deb-src http://packages.dotdeb.org stable all""")

    run('wget http://www.dotdeb.org/dotdeb.gpg')
    require.deb.add_apt_key('dotdeb.gpg')


def install_packages():
    """
    Installs the packages necessary for the project to run.
    TODO: customise as needed
    """

    packages = [

        ## usual sf2 stuff
        'lighttpd',
        'php5',
        'php5-fpm',
        'php5-sqlite',
        'php5-cli',
        'php5-apc',
        'php5-intl',
        'git',
        'curl',
        'nano',
        'acl',

        ## specific to the projet
        'php5-xsl'

    ]
    require.deb.packages(packages)
    
    # PHP settings should be overriden by the custom_php.ini file and not modified in php.ini !
    require.files.file(path='/etc/php5/conf.d/custom_php.ini', source = os.path.dirname(__file__) + '/files/custom_php.ini')

def install_mongodb():
    require.deb.packages([
        'mongodb',
        'php5-dev',
        'php-pear',
        'make'
        ])

    if not exists('/usr/lib/php5/20090626/mongo.so'):    
        sudo('pecl install mongo')

    
    require.files.file(path='/etc/php5/conf.d/mongo.ini', source = os.path.dirname(__file__) + '/files/mongo.ini')
    service.restart('php5-fpm')


def install_fpm():
    """
    Configures Lighttpd + PHP to communicate with FPM
    Rasmus' recommended way: Nginx + FPM
    """
    with files.watch('/etc/lighttpd/conf-enabled/15-fastcgi-fpm.conf', True, service.restart, 'lighttpd'):
        require.files.file(path='/etc/lighttpd/conf-available/15-fastcgi-fpm.conf', source = os.path.dirname(__file__) + '/files/15-fastcgi-fpm.conf')
        run('lighttpd-enable-mod fastcgi-fpm')

    # this is necessary if a Reverse-proxy like Varnish or HaProxy is in front
    with files.watch('/etc/lighttpd/conf-enabled/20-extforward.conf', True, service.restart, 'lighttpd'):
        require.files.file(path='/etc/lighttpd/conf-available/20-extforward.conf', source = os.path.dirname(__file__) + '/files/20-extforward.conf')
        run('lighttpd-enable-mod extforward')


def install_hosts():
    """
    Configures the web applications served by Lighttpd.
    - Redirects
    - document root
    - etc.
    """
    with files.watch('/etc/lighttpd/conf-enabled/90-hosts.conf', True, service.restart, 'lighttpd'):
        require.files.file(path='/etc/lighttpd/conf-available/90-hosts.conf', source = os.path.dirname(__file__) + '/files/90-hosts.conf')
        run('lighttpd-enable-mod hosts')


def create_user(name='theodo'):
    """
    Creates
     - a "theodo" user
     - a home directory
     - a ssh key for Github deployment
    
    Default directory for web applications: /home/theodo/www/mywebapplication
    """

    require.users.user(name=name, home='/home/%s' % name)
    run('chsh -s /bin/bash %s' % name)

    deploy_key_file = '/home/%s/.ssh/id_rsa.pub' % name
    if not exists(deploy_key_file):
        sudo('ssh-keygen', user=name)

    ssh_key = run('cat ' + deploy_key_file)

    print "******************** LA CLEF DE DEPLOY POUR GITHUB ******************"
    print ssh_key
    print "*********************************************************************"


def install():
    install_bare()
    install_dotdeb()
    install_packages()
    install_mongodb()
    install_fpm()
    install_hosts()
    create_user()