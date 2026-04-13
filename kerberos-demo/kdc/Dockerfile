FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    bison \
    flex \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

ENV KRB5_VERSION=1.21.2
RUN wget https://kerberos.org/dist/krb5/1.21/krb5-${KRB5_VERSION}.tar.gz && \
    tar -xzf krb5-${KRB5_VERSION}.tar.gz && \
    rm krb5-${KRB5_VERSION}.tar.gz

RUN cd krb5-${KRB5_VERSION}/src && \
    ./configure && \
    make && \
    make install && \
    ldconfig /usr/local/lib

ENV KRB5_KDC_PROFILE=/usr/local/var/krb5kdc/kdc.conf

RUN mkdir -p /etc && cat <<EOF > /etc/krb5.conf
[libdefaults]
    default_realm = LAB.LOCAL
    dns_lookup_kdc = false

[realms]
    LAB.LOCAL = {
        kdc = kdc.lab.local:88
        admin_server = kdc.lab.local:749
    }

[domain_realm]
    .lab.local = LAB.LOCAL
    lab.local = LAB.LOCAL
EOF

RUN mkdir -p /usr/local/var/krb5kdc && \
    mkdir -p /var/log && \
    cat <<EOF > /usr/local/var/krb5kdc/kdc.conf
[kdcdefaults]
    kdc_listen = 88
    kdc_tcp_listen = 88

[realms]
    LAB.LOCAL = {
        kadmind_port = 749
        max_life = 12h 0m 0s
        max_renewable_life = 7d 0h 0m 0s
        master_key_type = aes256-cts
        supported_enctypes = aes256-cts:normal aes128-cts:normal
        database_name = /usr/local/var/krb5kdc/principal
        key_stash_file = /usr/local/var/krb5kdc/.k5.LAB.LOCAL
        acl_file = /usr/local/var/krb5kdc/kadm5.acl
    }

[logging]
    kdc = FILE:/var/log/krb5kdc.log
    admin_server = FILE:/var/log/kadmin.log
    default = FILE:/var/log/krb5lib.log
EOF

RUN echo "*/admin@LAB.LOCAL *" > /usr/local/var/krb5kdc/kadm5.acl

RUN cat <<EOF > /entrypoint.sh
#!/bin/sh
if [ ! -f /usr/local/var/krb5kdc/principal ]; then
    echo "Creating Kerberos Database..."
    printf "admin\nadmin\n" | /usr/local/sbin/kdb5_util create -s -r LAB.LOCAL
    /usr/local/sbin/kadmin.local -q "addprinc -pw admin admin/admin@LAB.LOCAL"
fi

echo "Starting KDC and Admin Server..."
/usr/local/sbin/krb5kdc
/usr/local/sbin/kadmind -nofork
EOF

RUN chmod +x /entrypoint.sh

EXPOSE 88 749

CMD ["/entrypoint.sh"]
