FROM odoo:18.0
USER root
RUN apt-get update && apt-get install -y python3-pip python3-pandas
RUN apt install -y python3-google-auth python3-google-auth-httplib2 python3-requests-oauthlib python3-google-auth-oauthlib python3-googleapi
USER odoo
