"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class shutit_copyserver(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches) 
		#                                    - Returns True if any lines in output match any of 
		#                                      the regexp strings in the matches list
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		# 
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		#
		# LOGGING AND DEBUG
		# shutit.log(msg)                    - Send a message to the log
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of 
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is 
		#                                      a boolean type
		if not shutit.send_and_match_output('whoami','root'):
			shutit.fail('You must be root to run this')
		shutit.install('python-pip')
		shutit.install('git')
		if not shutit.send_and_match_output('git config -l','user.email'):
			shutit.send('git config --global user.email "shutit@shutit.tk"')
		if not shutit.send_and_match_output('git config -l','user.name'):
			shutit.send('git config --global user.name "ShutIt"')
		shutit.send('rm -rf /tmp/shutit_copyserver')
		shutit.send('pip install blueprint')
		shutit.send('''echo ':package:apt/docker' >> /etc/blueprintignore''')
		shutit.send('''echo ':package:apt/docker.io' >> /etc/blueprintignore''')
		shutit.send('''echo ':package:apt/docker-engine' >> /etc/blueprintignore''')
		shutit.send('''echo ':package:apt/virtualbox' >> /etc/blueprintignore''')
		shutit.send('''echo ':package:apt/virtualbox-dkms' >> /etc/blueprintignore''')
		shutit.send('''echo ':package:apt/virtualbox-qt' >> /etc/blueprintignore''')
		shutit.send('shutit skeleton --output_dir --base_image ' + shutit.cfg[self.module_id]['base_image'] + ' --pattern docker --name /tmp/shutit_copyserver --domain shutit.copied_server --delivery docker')
		shutit.send('cd /tmp/shutit_copyserver')
		shutit.send('blueprint create shutit_copyserver')
		shutit.send('blueprint show -S shutit_copyserver')
		# Edit out the service startups from the blueprint
		shutit.send('''sed -i 's/^...n "$SERVICE_.*$//g' shutit_copyserver/bootstrap.sh''')
		pwd = shutit.send_and_get_output('pwd')
		filename = shutit.send_and_get_output('ls *py')
		shutit.insert_text('''
		shutit.install('python-pip')
		shutit.send_host_dir('/tmp/shutit_copyserver','/tmp/shutit_copyserver/shutit_copyserver')
		shutit.send('cd /tmp/shutit_copyserver/shutit_copyserver')
		shutit.send('sh ./*.sh')
''',pwd + '/' + filename,'return True',before=True)
		shutit.multisend(shutit.host['shutit_path'] + '/shutit build -d docker -s repository tag yes -s repository name copyserver -l DEBUG',{'shutit appears not':'n'},timeout=999999)
		return True

	def get_config(self, shutit):
		shutit.get_config(self.module_id, 'base_image', hint='Please input an appropriate docker base image, eg:\nubuntu\nubuntu:12.04\ncentos\n\nYou can use any base image you want, but be aware that non-apt or yum-based images are less likely to succeed.')
		return True


def module():
	return shutit_copyserver(
		'shutit.shutit_copyserver.shutit_copyserver.shutit_copyserver', 1161086295.00,
		description='Copy a server\'s config divined using blueprint',
		maintainer='ian.miell@gmail.com',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup']
	)

