listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 0 
  tls_cert_file = "/etc/vault/cert/vault.crt"
  tls_key_file = "/etc/vault/cert/vault.key"
  tls_root_cer =  "/opt/vault/tls/chain.crt"
}

storage "mysql" {
  address  = "<ipdbaddress>"
  username = "<dbusername>"
  password = "<dbpassword>"
  database = "<dbdatabasename>"
}

api_addr = "https://<dockeripaddress>:8200"
ui = true

max_lease_ttl = "10h"
default_lease_ttl = "10h"
disable_mlock = true


