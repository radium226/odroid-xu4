# OVH
## Configuration de base
### Serveurs DNS
 - ns112.ovh.net
 - dns112.ovh.net
### Zone DNS
```
$TTL 3600
@	IN SOA dns112.ovh.net. tech.ovh.net. (2018100101 86400 3600 3600000 300)
                          IN NS     ns112.ovh.net.
                          IN NS     dns112.ovh.net.
                          IN MX 1   redirect.ovh.net.
                          IN A      213.186.33.5
                          IN TXT    "1|www.rouages.xyz"
                      600 IN TXT    "v=spf1 include:mx.ovh.com ~all"
_autodiscover._tcp        IN SRV    0 0 443 mailconfig.ovh.net.
_imaps._tcp               IN SRV    0 0 993 ssl0.ovh.net.
_submission._tcp          IN SRV    0 0 465 ssl0.ovh.net.
autoconfig                IN CNAME  mailconfig.ovh.net.
autodiscover              IN CNAME  mailconfig.ovh.net.
ftp                       IN CNAME  rouages.xyz.
imap                      IN CNAME  ssl0.ovh.net.
mail                      IN CNAME  ssl0.ovh.net.
pop3                      IN CNAME  ssl0.ovh.net.
smtp                      IN CNAME  ssl0.ovh.net.
www                       IN MX 1   redirect.ovh.net.
www                       IN A      213.186.33.5
www                       IN TXT    "l|fr"
www                       IN TXT    "3|welcome"
```

## Liens
 - https://openclassrooms.com/forum/sujet/delegation-de-serveur-dns-chez-ovh-41990
 - https://julienc.io/2/nom_de_domaine_et_dns_sur_un_serveur_dedie
 - https://www.afnic.fr/ext/dns/html/cours245.html

