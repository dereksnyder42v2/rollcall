#!/bin/bash

prompt() {
    read -p "$@ [Y/n] " 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        : # proceed
    else
        exit 1 # quit program execution
    fi  
    #echo $REPLY
}

# check if python3 is installed
command -v python3 > /dev/null
if [[ $? -ne 0 ]]; then
	echo "You need to install python3."
	exit 1
fi

# check if pip is installed
command -v pip > /dev/null
if [[ $? -ne 0 ]]; then
	echo "You need to install pip...make sure it's the right version!"
	echo "i.e. $ python3 -m pip"
	exit 1
fi

# check if python library requests is installed
python3 -c "import requests" > /dev/null
if [[ $? -ne 0 ]]; then
	prompt "Would you like to install requests?"
	python3 -m pip install requests
	if [[ $? -ne 0 ]]; then
		echo "Hmm...pip install failed. Exiting"
		exit 1
	fi
fi

# add cron job
trap "echo Removing $TEMPFILE...; rm -f $TEMPFILE" EXIT
TEMPFILE=$(mktemp)
crontab -l > /dev/null
if [[ $? -ne 0 ]]; then
	# you don't have a crontab! YOU FOOL!
	cat <<- EOF > $TEMPFILE
	# Edit this file to introduce tasks to be run by cron.
	# 
	# Each task to run has to be defined through a single line
	# indicating with different fields when the task will be run
	# and what command to run for the task
	# 
	# To define the time you can provide concrete values for
	# minute (m), hour (h), day of month (dom), month (mon),
	# and day of week (dow) or use '*' in these fields (for 'any').# 
	# Notice that tasks will be started based on the cron's system
	# daemon's notion of time and timezones.
	# 
	# Output of the crontab jobs (including errors) is sent through
	# email to the user the crontab file belongs to (unless redirected).
	# 
	# For example, you can run a backup of all your user accounts
	# at 5 a.m every week with:
	# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
	# 
	# For more information see the manual pages of crontab(5) and cron(8)
	# 
	# m h  dom mon dow   command	
	EOF
else
	# you do have a crontab
	crontab -l > $TEMPFILE
fi
echo "*/15 * * * * $PWD/rollcall-client.py" >> $TEMPFILE
crontab $TEMPFILE && echo "crontab updated."	
[[ $? -ne 0 ]] && echo "crontab update failed."


