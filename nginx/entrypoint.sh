#!/bin/sh

# obtain cert only if certs file are not present. Be careful not to hit rate
# https://letsencrypt.org/docs/rate-limits/
if [ ! -e "/etc/letsencrypt/live/grocerfinder.com/fullchain.pem" ]  || \
[ ! -e "/etc/letsencrypt/live/grocerfinder.com/privkey.pem" ]; then
    certbot --nginx --non-interactive --keep-until-expiring --agree-tos \
        -m tinutmap@gmail.com -d grocerfinder.com -d www.grocerfinder.com
    echo "new get obtained!";
fi 

# auto renew cert
SLEEPTIME=$(awk 'BEGIN{srand(); print int(rand()*(3600+1))}'); \
echo "0 0,12 * * * sleep $SLEEPTIME && certbot renew --deploy-hook \"nginx -s reload\"" \
| tee -a /etc/crontabs/root > /dev/null
