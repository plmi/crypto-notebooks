```
|       \                     |  \                                   |  \      
| $$$$$$$\  ______   _______  | $$   __   ______   ______   __    __ | $$____  
| $$__/ $$ |      \ |       \ | $$  /  \ /      \ |      \ |  \  |  \| $$    \ 
| $$    $$  \$$$$$$\| $$$$$$$\| $$_/  $$|  $$$$$$\ \$$$$$$\| $$  | $$| $$$$$$$\
| $$$$$$$\ /      $$| $$  | $$| $$   $$ | $$   \$$/      $$| $$  | $$| $$  | $$
| $$__/ $$|  $$$$$$$| $$  | $$| $$$$$$\ | $$     |  $$$$$$$| $$__/ $$| $$__/ $$
| $$    $$ \$$    $$| $$  | $$| $$  \$$\| $$      \$$    $$ \$$    $$| $$    $$
 \$$$$$$$   \$$$$$$$ \$$   \$$ \$$   \$$ \$$       \$$$$$$$  \$$$$$$  \$$$$$$$ 
                                                                             
#####################################################################################
Sie wurden als IT-Security Spezialist zu einer forensischen Untersuchung hinzugezogen. Die Bank "SecureBank" wurde gehackt. Der Angreifer hat sich Zugang zu einem Server verschafft und alles gelöscht. Es wird vermutet, dass er Nachrichten hinterlassen hat. Ihre Aufgabe ist es nun diese Nachrichten zu rekonstruieren, um das Motiv für die Tat zu erfahren. 

Auf dem Server wurden alle Dateien gelöscht, weswegen auch der private Schlüssel zum Server Zertifikat verloren gegangen ist. Glücklicherweise hat SecureBank einen "Full Packet Capture" des Angriffs, und das automatische RAM-Einfriersystem konnte teile des "Keyblocks" der Verbindung des Angreifers rekonstruieren. 


B0 DF 56 TT TT 46 53 A0  57 84 E5 52 98 B9 2A 08
47 7F B1 TT TT D4 2A 1B  CE E5 58 28 81 FB 02 F4
DC 60 78 43 2D 2F 6B CB  TT TT TT TT TT 7F TT TT
94 B8 A6 6E 3B TT TT TT  A1 TT CA F9 50 49 C0 C4
45 E3 F5 B0 70 2E A7 53


Teile des Keyblocks konnten nicht wiederhergestellt werden. Diese wurden mit TT gekennzeichnet. Ihr Ziel in dieser Übung ist es, die ApplicationDaten zu entschlüsseln die der Client geschickt hat. Beantworten Sie dazu die folgenden Fragen.

1) Welche Teile des Keyblocks haben Sie?
2) Was fällt auf, wenn Sie sich die ausgetauschten Nachrichten anschauen? Was ist auffällig?
3) Rekonstruieren Sie den server_write_key
4) Erbeuten Sie den PrivateKey. (Hinweis: Berühmter Angriff!)
5) Wie lautet der private Exponent?
6) Wie lautet das ClientRandom?
7) Wie lautet das ServerRandom?
8) Der Angreifer hat im PMS eine Botschaft für den Server hinterlassen. Wie lautet diese?
9) Warum kann der Angreifer bei DHE CipherSuites keine ausgiebigen Botschaften hinterlassen?
10) Hat der Angreifer eine Botschaft im MasterSecret hinterlassen?
11) Wie lauten die fehlenden Bytes des Keyblocks?
12) Wie lautet der client_write Key?
13) Welche Nachricht hat der Angreifer für die Bank in der ApplicationData Nachricht hinterlassen?


#####################################################################################
								END OF MESSAGE
#####################################################################################
```

## Lösung

> 1. Welche Teile des Keyblocks haben Sie?

* SHA1      = 20 Byte Hashlänge
* AES-128   = 16 Byte Schlüssellänge

Client Write MAC Key
```
B0 DF 56 TT TT 46 53 A0 57 84 E5 52 98 B9 2A 08
47 7F B1 TT
```

Server Write MAC Key
```
TT D4 2A 1B  CE E5 58 28 81 FB 02 F4 DC 60 78 43
2D 2F 6B CB
```

Client Write Key
```
TT TT TT TT TT 7F TT TT 94 B8 A6 6E 3B TT TT TT
```

Server Write Key
```
A1 TT CA F9 50 49 C0 C4 45 E3 F5 B0 70 2E A7 53
```

> 2. Was fällt auf, wenn Sie sich die ausgetauschten Nachrichten anschauen? Was ist auffällig?

Die 2. `Encrypted Heartbeat` Nachricht ist auffällig lang.  
Hier könnte es sich um einen Heartbleed-Angriff handeln.

> 3. Rekonstruieren Sie den server_write_key

Skript [brute-server-write-key.py](./scripts/brute-server-write-key.py)  
Das fehlende Byte lautet: `13`
```
13: 1400000c8fef30a8aa6073e0b80593adf2699432eb2b3b005312373bfdde3953f4ef81a20b0b0b0b0b0b0b0b0b0b0b0b
```

Der Server Write Key lautet:
```
A1 13 CA F9 50 49 C0 C4 45 E3 F5 B0 70 2E A7 53
```

> 4. Erbeuten Sie den PrivateKey. (Hinweis: Berühmter Angriff!)

Skript: [decrypt-heartbeat.py](./scripts/decrypt-heartbeat.py)

Privater RSA Schlüssel
```
-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAMEZOBznkJG1wWoM
NFmn0RkrV+9bEe4b8mKez3gKVnmpXBfjnivvtmDq6E9JC9Pv82V2eE9uHeaAvsK2
1Gti/oqcQcVOVE/GVzUmAaN1cf0+lj8irpL4amBXVPdCUilvAuhfGdBD7zz+4AdX
3ZeDb8lpqUj1SmoXhz6sLfYESZERAgMBAAECgYBf9J9MxcmyjsZxY2U0VE91GXPW
LsRHNb4KQe7JMSHtzTpFaMf1/2X63WDZ3WuyQuAJwIhiuE7Fd57T9bSzNHtWGhKH
g1NSMG3I+N//2T03lek610LFg5+30/CfYypTjRpZhprThKjfzq30m+Kl0XyEgSUF
f4gAgLRt21u6gn5sAQJBAPOItEFatbU/6EW9dAuP7JOjQBAK4CvSriDohJheBDav
bLuNVmmrDTnxH9kMSfLaWGNhD/Itq3y/zjjK3/Zc0NECQQDK+5pc42w1lKbqVg4G
+p+VHROl99Na7LzZ0B6GQKfuuhuIuaaLeazUNV2Qip8qdGUmT3cZgOfSFm1c9rQf
ssxBAkEAj7kM0EkNVcM6e/X8B1rP/q1ogE86zwIN+6PdpOJPUEqlO+aEqeXl710L
M5faCHWtljDRLVagjwXPWZr5I7bREQJAGQKVS3quG4/8XQVLZyq8PPg/MoTtotdm
kYPmLu6Kgoyl1dviHG9ajy8gHy4lXGrJB8Zky1yps6YVxY2UNg+mwQJBAI11gXT9
bhwtdtoQe4znmtI0dR7SKFFJp7sKAy9QZMnHWUzxRvybekzF2rAkI5m5q3YR6QdE
ER6Z7F+I6qK++Ug=
-----END PRIVATE KEY-----
```

Privaten Exponent ermitteln
```bash
$ openssl rsa -in rsa_priv.key -text

Private-Key: (1024 bit, 2 primes)
modulus:
    00:c1:19:38:1c:e7:90:91:b5:c1:6a:0c:34:59:a7:
    d1:19:2b:57:ef:5b:11:ee:1b:f2:62:9e:cf:78:0a:
    56:79:a9:5c:17:e3:9e:2b:ef:b6:60:ea:e8:4f:49:
    0b:d3:ef:f3:65:76:78:4f:6e:1d:e6:80:be:c2:b6:
    d4:6b:62:fe:8a:9c:41:c5:4e:54:4f:c6:57:35:26:
    01:a3:75:71:fd:3e:96:3f:22:ae:92:f8:6a:60:57:
    54:f7:42:52:29:6f:02:e8:5f:19:d0:43:ef:3c:fe:
    e0:07:57:dd:97:83:6f:c9:69:a9:48:f5:4a:6a:17:
    87:3e:ac:2d:f6:04:49:91:11
publicExponent: 65537 (0x10001)
privateExponent:
    5f:f4:9f:4c:c5:c9:b2:8e:c6:71:63:65:34:54:4f:
    75:19:73:d6:2e:c4:47:35:be:0a:41:ee:c9:31:21:
    ed:cd:3a:45:68:c7:f5:ff:65:fa:dd:60:d9:dd:6b:
    b2:42:e0:09:c0:88:62:b8:4e:c5:77:9e:d3:f5:b4:
    b3:34:7b:56:1a:12:87:83:53:52:30:6d:c8:f8:df:
    ff:d9:3d:37:95:e9:3a:d7:42:c5:83:9f:b7:d3:f0:
    9f:63:2a:53:8d:1a:59:86:9a:d3:84:a8:df:ce:ad:
    f4:9b:e2:a5:d1:7c:84:81:25:05:7f:88:00:80:b4:
    6d:db:5b:ba:82:7e:6c:01
prime1:
    00:f3:88:b4:41:5a:b5:b5:3f:e8:45:bd:74:0b:8f:
    ec:93:a3:40:10:0a:e0:2b:d2:ae:20:e8:84:98:5e:
    04:36:af:6c:bb:8d:56:69:ab:0d:39:f1:1f:d9:0c:
    49:f2:da:58:63:61:0f:f2:2d:ab:7c:bf:ce:38:ca:
    df:f6:5c:d0:d1
prime2:
    00:ca:fb:9a:5c:e3:6c:35:94:a6:ea:56:0e:06:fa:
    9f:95:1d:13:a5:f7:d3:5a:ec:bc:d9:d0:1e:86:40:
    a7:ee:ba:1b:88:b9:a6:8b:79:ac:d4:35:5d:90:8a:
    9f:2a:74:65:26:4f:77:19:80:e7:d2:16:6d:5c:f6:
    b4:1f:b2:cc:41
exponent1:
    00:8f:b9:0c:d0:49:0d:55:c3:3a:7b:f5:fc:07:5a:
    cf:fe:ad:68:80:4f:3a:cf:02:0d:fb:a3:dd:a4:e2:
    4f:50:4a:a5:3b:e6:84:a9:e5:e5:ef:5d:0b:33:97:
    da:08:75:ad:96:30:d1:2d:56:a0:8f:05:cf:59:9a:
    f9:23:b6:d1:11
exponent2:
    19:02:95:4b:7a:ae:1b:8f:fc:5d:05:4b:67:2a:bc:
    3c:f8:3f:32:84:ed:a2:d7:66:91:83:e6:2e:ee:8a:
    82:8c:a5:d5:db:e2:1c:6f:5a:8f:2f:20:1f:2e:25:
    5c:6a:c9:07:c6:64:cb:5c:a9:b3:a6:15:c5:8d:94:
    36:0f:a6:c1
coefficient:
    00:8d:75:81:74:fd:6e:1c:2d:76:da:10:7b:8c:e7:
    9a:d2:34:75:1e:d2:28:51:49:a7:bb:0a:03:2f:50:
    64:c9:c7:59:4c:f1:46:fc:9b:7a:4c:c5:da:b0:24:
    23:99:b9:ab:76:11:e9:07:44:11:1e:99:ec:5f:88:
    ea:a2:be:f9:48
writing RSA key
```

Privater Exponent
```
5ff49f4cc5c9b28ec671636534544f751973d62ec44735be0a41eec93121edcd3a4568c7f5ff65fadd60d9dd6bb242e009c08862b84ec5779ed3f5b4b3347b561a1287835352306dc8f8dfffd93d3795e93ad742c5839fb7d3f09f632a538d1a59869ad384a8dfceadf49be2a5d17c848125057f880080b46ddb5bba827e6c01
```

> 6. Wie lautet das ClientRandom?

```
41f023c160b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c
```

> 7. Wie lautet das ServerRandom?

```
41f023fa60b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c
```

> 8. Der Angreifer hat im PMS eine Botschaft für den Server hinterlassen. Wie lautet diese?

TLS RSA:

```
pms = Version(2)|Random(46)  
CKE = PKCS1.5(pms)^e mod n  
pms = CKE^d mod n  
PKCS1.5 Encoding = 00 02 (>= 8 non-zero bytes) 00 <2 byte version> <46 byte pms>
```

Verschlüsseltes PMS
```
484817070083d39006630d5727642d49a884a92b642288f940b784c3cc5e888f8b3cda45b44bc54a928708996943c466e056c6419f8faa31861d962cd3c6d0f2bacbf8e02c86efd71667f1ecc7854c6a328511994ac20e0a957a196a15ca1b63433444299d87ac4b40b5c66f2408f5bec92bbd88a5ac9455a85826d5c4dc1023
```

Skript: [decrypt-pms.py](./scripts/decrypt-pms.py)

PMS lautet
```
0303495f614d5f676f696e475f746f5f64657374726f795f796f755f666f725f796f75725f73696e7300000000000000
```

Plaintext: `I_aM_goinG_to_destroy_you_for_your_sins`

> 9. Warum kann der Angreifer bei DHE CipherSuites keine ausgiebigen Botschaften hinterlassen?

Das PMS wird bei DHE über die Berechnung der Client- und Server-Anteile g^c und g^s berechnet:  
`PMS = CDH(g^c, g^s).`  
Es kann nicht sichergestellt werden, dass eine lesbare Zeichenkette dabei rauskommt.

> 10. Hat der Angreifer eine Botschaft im MasterSecret hinterlassen?

Skript: [calculate-master-secret.py](./scripts/calculate-master-secret.py)

Master Secret = TLS-PRF(pms, "master secret", client_random|server_random)
```
fee43619219b66e3a8651fcf3ca7380cea8378d76a5c0762293d2078f2746d76e4e0e8954e0d75beb9c4f33e6b27700f
```

Es ist keine Nachricht im Master Secret eingebettet.

> 11. Wie lauten die fehlenden Bytes des Keyblocks?

Keyblock = TLS-PRF(master_secret, "key expansion", server_random|client_random)

Skript: [calculate-keyblock.py](./scripts/calculate-keyblock.py)

```
b0df56a5b04653a05784e55298b92a08
477fb12dabd42a1bcee5582881fb02f4
dc6078432d2f6bcba7bf8900807f2bb4
94b8a66e3b4ae040a113caf95049c0c44
5e3f5b0702ea753
```

Client Write MAC Key: `b0df56a5b04653a05784e55298b92a08477fb12d`
Server Write MAC Key: `abd42a1bcee5582881fb02f4dc6078432d2f6bcb`
Client Write Key: `a7bf8900807f2bb494b8a66e3b4ae040`
Server Write Key: `a113caf95049c0c445e3f5b0702ea753`

> 13. Welche Nachricht hat der Angreifer für die Bank in der ApplicationData Nachricht hinterlassen?

Skript: [decrypt-application-data.py](./scripts/decrypt-application-data.py)

Nachricht: `rm / -rf # secureBank kills caused the climate crisis`
