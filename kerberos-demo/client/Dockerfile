FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    krb5-user \
    python3 \
    python3-gssapi \
    && rm -rf /var/lib/apt/lists/*

RUN cat <<EOF > /etc/krb5.conf
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

WORKDIR /app
COPY . .
