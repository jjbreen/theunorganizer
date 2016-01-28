# Config files

This folder contains config files for setting up Unorganizr on a new server.

Clone Unorganizr into /var/www/unorganizr.

The ini file is the uwsgi config template, copy to /var/www/unorganizr.

The cron file is the cron job for automatically updating the 25 live data, install in /etc/cron.d/

The conf file is the upstart script for launching uwsgi. Copy to /etc/init/

The nginx file is the nginx configuration site. Copy to /etc/nginx/sites-available/ and link to from sites-enabled


