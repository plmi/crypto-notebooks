```
Gegeben seien die folgenden Client Keys für die Session aus handshake.pcapng: 

Key 1:  
67d545b020c46aef2da4c1220380cde0 

Key 2: 
5f6fa4951a65884ab239d9af9b481874f6324df63bdca909a4bacdfe9c62f9ba
```

# Lösung

> 1. Welcher der beiden Schlüssel ist der Client Write Key, welcher Client Write Mac Key? 

Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (0xc027)

SHA256 = 32 Byte MAC  
Client Write Key: `67d545b020c46aef2da4c1220380cde0`  
Client Write MAC Key: `5f6fa4951a65884ab239d9af9b481874f6324df63bdca909a4bacdfe9c62f9ba`

> 2. Sie sollen nun selbst einen Record erzeugen und eine ApplicationData Nachricht verschlüsseln, die vom Client and den Server (nach der Finished Nachricht) gesendet werden soll. 
> Die Nachricht, die Sie verschlüsseln sollen, lautet: 
>
> 4576656e2074686520736d616c6c65737420706572736f6e2063616e206368616e67652074686520636f75727365206f6620746865206675747572652e
> 
> TLS in der ausgehandelten Version folgt dem "MAC-then-Pad-then-Encrypt"-Paradigma. Daher müssen Sie zunächst die HMAC berechnen. Diese wird wie folgt berechnet: 
>
> HMAC[key] (Sequenznummer | Content Type des Records | Versionsbytes der TLS-Version | Länge der zu verschlüsselnden Nachricht (2 Bytes) | Nachricht)
>
> Sie sollen nun selbst einen Record erzeugen und eine ApplicationData Nachricht verschlüsseln, die vom Client and den Server (nach der Finished Nachricht) gesendet werden soll.
>
> Die Sequenznummer ist eine 64-Bit Zahl, welche die Anzahl der bisher gesendeten Records (unter dem aktuellen Schlüssel) wiedergibt. Da Sie den zweiten verschlüsselten Record (des Clients) dieser Verbindung senden wollen, müssen Sie die Sequenznummer 0x0000000000000001 verwenden. Der Content Type ist 0x17 (Application Data).
>
> Über welche Bytes wird der HMAC gebildet? 


SQN: `0x0000000000000001`  
Content-Type: `0x17`  
Version: `0x0303`  
Länge: Länge Klartext = 61 = `0x003d`

```
HMAC = TLS-PRF[client_write_mac_key](0000000000000001 17 0303 003d 4576656e2074686520736d616c6c65737420706572736f6e2063616e206368616e67652074686520636f75727365206f6620746865206675747572652e)
```

> 3. Wie lautet der HMAC? Verwenden Sie tls_ hmac.py

```bash
$ python tls_hmac.py

4167a102881164829869b4633b0c59b462a651f66c367d0e1bc8db40dace705c
```

> 4. Wie viele Padding Bytes werden mindestens benötigt, um den Record zu verschlüsseln? 

Padding: 61 + 32 + 3 = 96

> 5. Wie lautet das minimale Padding für den Record? 

Padding: `020202`

> 6. Sie haben nun alle benötigten Informationen, um den Record zu verschlüsseln.  Nutzen sie den IV 443020de1cad09bfd6381ffb94daafbb. Wie lautet der Inhalt des verschlüsselten Records (ohne IV)? Verwenden Sie aes_encrypt.py
> 
> Hinweise: Die ersten acht Bytes lauten: 06557245f3a1e9b0

Payload: `Klartext|MAC|Padding`
```
4576656e2074686520736d616c6c65737420706572736f6e2063616e206368616e67652074686520636f75727365206f6620746865206675747572652e4167a102881164829869b4633b0c59b462a651f66c367d0e1bc8db40dace705c020202
```

```bash
$ python aes_encrypt.py
06557245F3A1E9B01B754B65F54607612378570630A127F330010B432B0134AE4F3D7D3AA5B9DF98675D9B144557849C3B0954C2B9279FF7E6EABBE2191FD6F6D14142249772847CEDC56E07567248A744D002AE5410BE21D8EE2AF241622478
```

> 7. Wie lautet der vollständige Record?
> Hinweis: der vollständige Record sollte 117 Bytes umfassen

Vollständige Record: `TYP | VERSION | LAENGE | (IV wenn >= TLS 1.1) | ENC(PLAINTEXT + MAC + PADDING)`  
```
17 0303 0070 443020de1cad09bfd6381ffb94daafbb 06557245F3A1E9B01B754B65F54607612378570630A127F330010B432B0134AE4F3D7D3AA5B9DF98675D9B144557849C3B0954C2B9279FF7E6EABBE2191FD6F6D14142249772847CEDC56E07567248A744D002AE5410BE21D8EE2AF241622478
```
Länge = 117 Byte
