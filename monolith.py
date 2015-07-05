from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
import sys
import subprocess

requires_api_version = '2.3'
plugin_type = (TYPE_CORE, TYPE_INTERACTIVE)

global yum_cmd
global commit_name
global rollback_name

def args_hook(conduit):
	global yum_cmd
	yum_cmd= conduit.getArgs()[0]
	print yum_cmd
	if yum_cmd!='commit' and yum_cmd!='rollback':
		print "Wrong command"
		sys.exit()
	print "Hello"
	if yum_cmd=='commit':
		print "Performing commit"
		commit_name = conduit.getArgs()[1]
		print 'Commit name : ' + commit_name
		cmd = 'umount /btrfs'
		subprocess.call(cmd,shell=True)
		cmd = 'mount -t btrfs -o subvolid=0 LABEL="fedora" /btrfs'
		subprocess.call(cmd,shell=True)
		print "Mounted"
		cmd = 'echo "LABEL=\"fedora\" /btrfs btrfs defaults,noauto,subvolid=0 0 0" >> /etc/fsta'
		subprocess.call(cmd,shell=True)
		cmd = 'btrfs subvolume snapshot /btrfs/root /btrfs/' + commit_name
		subprocess.call(cmd,shell=True)
		print "Snapshot created"
		sys.exit()
	if yum_cmd=='rollback':
		print "Performing rollback"
		rollback_name = conduit.getArgs()[1]
		print "Rollback name : "+rollback_name
		print "Checking subvolume ID"
		cmd = 'btrfs subvolume list /. | grep '+rollback_name+' | cut -d " " -f 2'
		test_str = subprocess.check_output(cmd,shell=True)
		test_str=test_str[:-1]
		cmd = 'btrfs subvolume set-default '+test_str+' /.'
		print cmd
		print "Rolling back"
		subprocess.call(cmd,shell=True)
		cmd = "sed -i 's/rootflags=subvol=root //' /boot/grub2/grub.cfg"
		subprocess.call(cmd,shell=True)
		print "Rollback complete. Reboot for effect"
		cmd = 'reboot'
		subprocess.call(cmd,shell=True)
		sys.exit()
