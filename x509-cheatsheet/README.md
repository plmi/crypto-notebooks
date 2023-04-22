# X.509 Cheatsheet

## Task 1

> Validate certificate chain of https://ocsp.digicert.com.

Download certificate chain:
1. Server certificate: [digicert-edgecastcdn-net.pem](./ocsp.digicert.com/digicert-edgecastcdn-net.pem)
2. Intermediate certificate [digicert-global-g2.pem](./ocsp.digicert.com/digicert-global-g2.pem)
3. Root certificate [digicert-global-root-g2.pem](./ocsp.digicert.com/digicert-global-root-g2.pem)

Verify certificates with `openssl`
```bash
# validate root certificate
$ openssl verify digicert-global-root-g2.pem
digicert-global-root-g2.pem: OK

# validate intermediate certificate
$ openssl verify digicert-global-g2.pem
digicert-global-g2.pem: OK

# validate server certificate
$ openssl verify -CAfile digicert-global-g2.pem digicert-edgecastcdn-net.pem
digicert-edgecastcdn-net.pem: OK
```

Is certificate expired? No
```bash
$ openssl x509 -in digicert-edgecastcdn-net.pem -dates -noout
oout
notBefore=Apr 12 00:00:00 2023 GMT
notAfter=May 12 23:59:59 2024 GMT
```

Get common name (CN) and alternative names of server certificate
```bash
# check common name
$ openssl x509 -in digicert-edgecastcdn-net.pem -subject -noout
subject=C = US, ST = California, L = Los Angeles, O = Edgecast Inc., CN = digicert.edgecastcdn.net

# Subject Alternative Name extension (see below)
```

Extract extensions
```bash
# check: Key Usage
$ openssl x509 -in digicert-global-g2.pem -noout -ext keyUsage
X509v3 Key Usage: critical
    Digital Signature, Certificate Sign, CRL Sign

# check: Subject Alternative Name extension 
$ openssl x509 -in digicert-edgecastcdn-net.pem -ext subjectAltName -noout
X509v3 Subject Alternative Name:
    DNS:digicert.edgecastcdn.net, DNS:cacerts.digicert.com, DNS:dl.cacerts.digicert.com, DNS:vmc.digicert.com
```

**Solution:** Certificate not valid for `ocsp.digicert.com`!

Can the (intermediate) CA issue certificates? Yes
```bash
# root certificate: can issue unlimited intermediates
$ openssl x509 -in digicert-global-root-g2.pem -noout -text | grep "Basic Constraints" -A1
            X509v3 Basic Constraints: critical
                CA:TRUE

# intermediate certificate: pathlen: 0 = can issue other server but not intermediate certificates
$ openssl x509 -in digicert-global-g2.pem -noout -text | grep "Basic Constraints" -A1
            X509v3 Basic Constraints: critical
                CA:TRUE, pathlen:0
```

Is the certificate self-signed? No
```bash
# subject != issuer
$ openssl x509 -in digicert-edgecastcdn-net.pem -subject -issuer -noout
subject=C = US, ST = California, L = Los Angeles, O = Edgecast Inc., CN = digicert.edgecastcdn.net
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2020 CA1
```

**Make OCSP request to check revocation status**

1. Obtain server certificate
2. Obtain certificate chain. It contains of all intermediates without the root certiticate.
3. Get `ocsp_uri` of server certificate
```bash
$ openssl x509 -in digicert-edgecastcdn-net.pem -ocsp_uri -noout
http://ocsp.digicert.com
```
4. Make the OCSP request
```bash
$ openssl ocsp -issuer digicert-edgecastcdn-net-chain.pem -cert digicert-edgecastcdn-net.pem -text -url http://ocsp.digicert.com 
[...]
    Cert Status: good
```

## Task 2

> Validate certificate chain of https://www.fau.de.

1. Server certificate: [www-fau-de.pem](./fau.de/www-fau-de.pem)
2. Intermediate CA: [geant-ov-rsa-ca-4.pem](./fau.de/geant-ov-rsa-ca-4.pem)
3. Root CA: [usertrust-rsa-certification-authority.pem](./fau.de/usertrust-rsa-certification-authority.pem)
4. Certificate chain: [www-fau-de-chain.pem](./fau.de/www-fau-de-chain.pem)
5. CRL: [GEANTOVRSACA4.crl](./fau.de/GEANTOVRSACA4.crl)

Download server certificate
```bash
$ openssl s_client -connect www.fau.de:443 \
  < /dev/null 2>&1 | sed -n '/-----BEGIN/,/-----END/p' > certificate.pem
```

Download certificate chain (includes server certificate - needs to be removed normally for further analysis with `openssl`)
```bash
$ echo "" | openssl s_client -verify_quiet -showcerts \
  -connect www.fau.de:443 | awk '/BEGIN/ { i++; } /BEGIN/, /END/ { print }'
# or
$ openssl s_client -showcerts -connect www.fau.de:443 \
  < /dev/null 2>&1 | sed -n '/-----BEGIN/,/-----END/p'
```

Is the CA allowed to issue certificates? Yes
```bash
$ openssl verify usertrust-rsa-certification-authority.pem
usertrust-rsa-certification-authority.pem: OK

# is CA, can issue intermediate certificates
$ openssl x509 -in usertrust-rsa-certification-authority.pem -noout -text | grep "Basic Constraints" -A1
  X509v3 Basic Constraints: critical
      CA:TRUE

# is allowed to issue other certificates
$ openssl x509 -in usertrust-rsa-certification-authority.pem -noout -ext keyUsage
X509v3 Key Usage: critical
    Certificate Sign, CRL Sign
```

Is the certificate valid? Yes
```bash
$ openssl x509 -in www-fau-de.pem -dates -noout
notBefore=Jun  2 00:00:00 2022 GMT
notAfter=Jun  2 23:59:59 2023 GMT
```

Is the intermediate trusted? Yes
```bash
$ openssl verify geant-ov-rsa-ca-4.pem
geant-ov-rsa-ca-4.pem: OK
```

Is the certificate self-signed? No
```bash
$ openssl x509 -in www-fau-de.pem -subject -issuer -noout
subject=C = DE, ST = Bayern, O = Friedrich-Alexander-Universit\C3\A4t Erlangen-N\C3\BCrnberg, OU = Webmaster, CN = www.fau.de
issuer=C = NL, O = GEANT Vereniging, CN = GEANT OV RSA CA 4
```

Has the certificate expired? No
```bash
$ openssl x509 -in www-fau-de.pem -dates -noout
notBefore=Jun  2 00:00:00 2022 GMT
notAfter=Jun  2 23:59:59 2023 GMT
```

Is the intermediate allowed to issue certificates? Yes
```bash
# Key Usage extension: Allowed to sign certificates
$ openssl x509 -in geant-ov-rsa-ca-4.pem -noout -ext keyUsage
X509v3 Key Usage: critical
    Digital Signature, Certificate Sign, CRL Sign
# is CA, can not sign other intermediates
$ openssl x509 -in geant-ov-rsa-ca-4.pem -noout -text | grep "Basic Constraints" -A1
        X509v3 Basic Constraints: critical
            CA:TRUE, pathlen:0
# make ocsp request: intermediate is not revoked
$ openssl ocsp -noout -text -issuer usertrust-rsa-certification-authority.pem \
  -cert geant-ov-rsa-ca-4.pem -text -url http://ocsp.usertrust.com
OCSP Response Data:
    OCSP Response Status: successful (0x0)
    Response Type: Basic OCSP Response
    Version: 1 (0x0)
    Responder Id: 67E44CA5D0F03F5F8D00F9C7CD2F84571A03853E
    Produced At: Apr 20 04:37:30 2023 GMT
    Responses:
    Certificate ID:
      Hash Algorithm: sha1
      Issuer Name Hash: CD30D24C343A82AB1F0570158AD7A107762992E9
      Issuer Key Hash: 5379BF5AAA2B4ACF5480E1D89BC09DF2B20366CB
      Serial Number: DA43BD139BD258BB4DD61CACC4F3DBE0
    Cert Status: good
```

Is the certificate valid for `www.fau.de`? Yes
```bash
$ openssl x509 -in www-fau-de.pem -noout -subject -ext subjectAltName
subject=C = DE, ST = Bayern, O = Friedrich-Alexander-Universit\C3\A4t Erlangen-N\C3\BCrnberg, OU = Webmaster, CN = www.fau.de
X509v3 Subject Alternative Name:
    DNS:www.fau.de, DNS:fau.de, DNS:uni-erlangen.de, DNS:www.uni-erlangen.de
```

Was the certificate revoked? No
```bash
# get ocsp uri
$ openssl x509 -in www-fau-de.pem -ocsp_uri -noout
http://GEANT.ocsp.sectigo.com

# make ocsp request
$ openssl ocsp -text -issuer www-fau-de-chain.pem -cert www-fau-de.pem \
  -text -url http://GEANT.ocsp.sectigo.com
[...]
OCSP Response Data:
    OCSP Response Status: successful (0x0)
    Response Type: Basic OCSP Response
[...]
      Serial Number: CB841FFA5A2208CE06FBEC9BAEFD86EB
    Cert Status: good
[...]
```

The certificate can be used to sign other certificates? No
```bash
$ openssl x509 -in www-fau-de.pem -noout -ext keyUsage
X509v3 Key Usage: critical
    Digital Signature, Key Encipherment
```

What's the RSA modulus?
```bash
$ openssl x509 -in www-fau-de.pem -noout -modulus
Modulus=D08FD008716F7A6E6287D7135702E40DA65CBC5B344E27D4A6D2701BA53A33B7BFD702F39A53E13C58FDBB2DD336A4DA84822D052C31EB613C97609B65A910F18C13B0C182075B6D370B600B897FC328AE690D826E545558A6BC53B9DAD0478EFCF8FE77C0A7E6457E1B747FBA8B1D6F590E7ABFA32EAE8A3725CD2CC1F976E253ABB6B2E12A1E6D7D33C8AE0559F983D40E7C1B2E6A7EB21A02DDD4CBDC76DA88F3CD7AD8ABE4659EAC47B41BB096FA251A828B30092F430E2372C16E04E9A37CCCC61F35EF9D8CD742798343086E086ACE56D306142D712896F0A3396EAE6CEB77FA0A57695CC35464F4AF80058151EF9748DA27126756376E01E2D99DFA5DD80B216FBC81E566949D1A4B06E75DCD0EB655FC8EA4234569EBB27296736CF2EAD19F437B405D0EE9E53F3992DB09C4428CB82FDB53A8246A4E41F9338F1B62FB042EAAA9E3A6F9823697E1097DF5CB019F1A92CEF8FF7C5F2BCE4053D3580C6E6E4E5F995FFEF3C68954991B98B28BDAF3D28741F3BDBF038BE79A9094612B03DC59D2B00E795957C528962988B420FDFBC6E376704464632643E281A967F77BA9CC86A11632C35E8D3E87F955C54FDAAF77A52AF5C8FA41D676669E3BB054E5E2F0407C6414F0543BA52EDAC17691EF6610A6614C7445B37A1C4537478557718AC22BA297E88DEF2AAD85F3B08E95EF2B5384C3A886FBE36006DE2A061CB1
```

What's the RSA exponent?
```bash
$ openssl x509 -in www-fau-de.pem -noout -text | grep -i exponent
Exponent: 65537 (0x10001)
```

List all hostnames this certificate is valid for
```bash
$ openssl x509 -in www-fau-de.pem -noout -subject -ext subjectAltName
subject=C = DE, ST = Bayern, O = Friedrich-Alexander-Universit\C3\A4t Erlangen-N\C3\BCrnberg, \
  OU = Webmaster, CN = www.fau.de
X509v3 Subject Alternative Name:
    DNS:www.fau.de, DNS:fau.de, DNS:uni-erlangen.de, DNS:www.uni-erlangen.de

- fau.de
- uni-erlangen.de
- www.uni-erlangen.de
- www.fau.de
```

What's the serial number of this certificate?
```bash
$ openssl x509 -in www-fau-de.pem -serial -noout
serial=CB841FFA5A2208CE06FBEC9BAEFD86EB
```

Get the URL of the Certificate Revocation List
```bash
$ openssl x509 -in www-fau-de.pem -ext crlDistributionPoints -noout
X509v3 CRL Distribution Points:
    Full Name:
      URI:http://GEANT.crl.sectigo.com/GEANTOVRSACA4.crl
```

View CRL. Which algorithm was used to sign this list? SHA-384 RSA
```bash
$ wget "http://GEANT.crl.sectigo.com/GEANTOVRSACA4.crl"
$ openssl crl -inform DER -text -noout -in GEANTOVRSACA4.crl
Signature Algorithm: sha384WithRSAEncryption
```

When and why was the certificate with serial `6A63F43046EC411F22834D936EA6CE28` revoked?  
15.03.2023, Key Compromise
```bash
$ openssl crl -inform DER -text -noout -in GEANTOVRSACA4.crl | grep 6A63F43046EC411F22834D936EA6CE28 -A4
    Serial Number: 6A63F43046EC411F22834D936EA6CE28
        Revocation Date: Mar 15 10:12:38 2023 GMT
        CRL entry extensions:
            X509v3 CRL Reason Code:
                Key Compromise
```

## Task 3

> Create a manual OCSP request for https://www.studon.fau.de

1. Server certificate: [www-studon-fau-de.pem](./studon.fau.de/www-studon-fau-de.pem)
2. Certificate chain: [www-studon-fau-de-chain.pem](./studon.fau.de/www-studon-fau-de-chain.pem)
3. Root CA: [www-studon-fau-de-root.pem](./studon.fau.de/www-studon-fau-de-root.pem)
4. OCSP request: [ocsp-request](./studon.fau.de/ocsp-request)

Get OCSP URI of the server certificate
```bash
$ openssl x509 -in www-studon-fau-de.pem -ocsp_uri -noout
http://GEANT.ocsp.sectigo.com
```

Generate OCSP request and display it
```bash
$ openssl ocsp -issuer www-studon-fau-de-chain.pem -cert www-studon-fau-de.pem -reqout ocsp-request
$ openssl ocsp -reqin ocsp-request -text
OCSP Request Data:
    Version: 1 (0x0)
    Requestor List:
        Certificate ID:
          Hash Algorithm: sha1
          Issuer Name Hash: C3FDEA1EAA0EBEDE75016EEC6E5BB393F0F12E5D
[...]
```

Send the previously generated OCSP request
```bash
$ openssl ocsp -reqin ocsp-request -url http://GEANT.ocsp.sectigo.com
WARNING: no nonce in response
Response Verify Failure
40F767EBC27F0000:error:13800076:OCSP routines:OCSP_basic_verify:signer certificate not found:crypto/ocsp/ocsp_vfy.c:107:
```

Repeat OCSP request and append certificate chain to validate response and the certificate chain
```bash
$ openssl ocsp -reqin ocsp-request -verify_other www-studon-fau-de-chain.pem \
  -url http://GEANT.ocsp.sectigo.com -text
OCSP Response Data:
    OCSP Response Status: successful (0x0)
    Response Type: Basic OCSP Response
[...]
WARNING: no nonce in response
Response verify OK
```

## Task 4

> Analyse certificate signing request (CSR) csr.pem

1. CSR: [csr.pem](./csr.pem)

Get common name (CN) of certificate signing request (CSR)
```bash
$ openssl req -text -noout -in csr.pem
Certificate Request:
    Data:
        Version: 1 (0x0)
        Subject: C = DE, O = FAU Exam Server, CN = www.secret.domain.fau.de
```
