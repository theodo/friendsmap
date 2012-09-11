#!/usr/bin/env python

import os
import sys

from fabric.api import env, run, sudo, cd
import fabtools

project_name = 'allomatch'
env.use_ssh_config = True
env.hosts = [project_name + '.cloud.theo.do', ]
env.user = 'root'
env.password = 'root'


def backup_daily():
	pass

def backup_weekly():
	pass

def install_backup_crons():
	user = 'theodo'
	fabtools.cron.add_daily('Daily backup of ' + project_name, user, 'fab -f /home/%s/www/%s/devops/backup.py backup_daily' % (user, project_name))
	fabtools.cron.add_task('Weekly backup of ' + project_name, '@weekly', user, 'fab -f /home/%s/www/%s/devops/backup.py backup_weekly' % (user, project_name))