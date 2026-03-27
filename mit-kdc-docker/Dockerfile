FROM alpine:latest

# 1. Install pre-compiled MIT Kerberos binaries
RUN apk add --no-cache krb5-server krb5

# 2. Configure the Realm (LAB.LOCAL)
RUN cat <<EOF > /etc/krb5.conf
[libdefaults]
    default_realm = LAB.LOCAL
[realms]
    LAB.LOCAL = {
        kdc = 127.0.0.1
        admin_server = 127.0.0.1
    }
EOF

RUN mkdir -p /var/lib/krb5kdc && touch /var/lib/krb5kdc/kadm5.acl

# 3. Create the startup script
RUN cat <<EOF > /entrypoint.sh
#!/bin/sh
# If the Kerberos database doesn't exist, create it
if [ ! -f /var/lib/krb5kdc/principal ]; then
    echo "Creating Kerberos Database..."
    # Create DB with master password 'admin'
    printf "admin\nadmin\n" | kdb5_util create -s -r LAB.LOCAL
    # Add an admin user (admin/admin@LAB.LOCAL) with password 'admin'
    kadmin.local -q "addprinc -pw admin admin/admin"
fi

echo "Starting KDC and Admin Server..."
/usr/sbin/krb5kdc
/usr/sbin/kadmind -nofork
EOF

RUN chmod +x /entrypoint.sh

# Expose Kerberos Authentication (88) and Admin Server (749) ports
EXPOSE 88 749

CMD ["/entrypoint.sh"]
