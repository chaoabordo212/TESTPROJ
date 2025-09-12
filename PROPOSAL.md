# Proširenje ideje projekta TESTPROJ i predlog implementacije

Ovaj dokument detaljnije razrađuje koncept TESTPROJ-a, analizira moguće implementacije i daje smernice za dalji razvoj.

## 1. Proširenje ideje projekta

TESTPROJ je zamišljen kao proaktivan alat za zaštitu lokalne mreže, fokusiran na identifikaciju i kontrolu pristupa uređaja. Glavni cilj je da se uspostavi "bela lista" (whitelist) pouzdanih uređaja i da se upozori administrator na svaki pokušaj povezivanja neautorizovanog uređaja.

**Ključni aspekti:**

*   **Jednostavnost i efikasnost:** Dizajniran za korisnike koji žele osnovnu, ali efikasnu zaštitu bez kompleksnih konfiguracija.
*   **Faza učenja/whitelistinga:** Inicijalna faza u kojoj se svi trenutno povezani uređaji automatski dodaju na belu listu. Ovo je ključno za lako pokretanje bez manuelnog unosa MAC adresa.
*   **Faza alarma/nadzora:** Nakon definisanog `TIMEOUT` perioda, sistem prelazi u režim aktivnog nadzora. Svaki uređaj koji se pojavi na mreži, a nije na beloj listi, pokreće definisanu `ACTION`.
*   **Prilagodljiva akcija:** Fleksibilnost u definisanju akcije (npr. slanje e-pošte, pokretanje skripte, logovanje događaja) omogućava prilagođavanje potrebama korisnika.
*   **Ciljna grupa:** Mali uredi/kućne mreže (SOHO), pojedinci zabrinuti za bezbednost svoje Wi-Fi mreže ili LAN-a.

**Potencijalni slučajevi upotrebe:**

*   **Kućna sigurnost:** Osiguravanje da se samo porodični uređaji (telefoni, računari, pametni uređaji) mogu povezati.
*   **Mali biznis:** Prevencija neautorizovanih uređaja koji se povezuju na mrežu kompanije.
*   **IoT nadzor:** Kontrola pristupa IoT uređajima i detekcija "shadow IT" uređaja.

## 2. Procena mogućih implementacija

Implementacija TESTPROJ-a zahteva rešavanje nekoliko ključnih tehničkih izazova:

### a) Skeniranje mreže i detekcija uređaja

*   **ARP skeniranje:** Najčešći i najefikasniji metod za otkrivanje uređaja na lokalnom segmentu mreže. Slanje ARP zahteva (ARP Who-has) za sve IP adrese u opsegu mreže (npr. 192.168.1.1-254) i prikupljanje ARP odgovora koji sadrže MAC adrese.
*   **DHCP Snooping/Monitoring:** Kompleksnije, zahteva pristup DHCP serveru ili mogućnost pasivnog presretanja DHCP saobraćaja. Manje praktično za samostalan alat.
*   **Nmap:** Snažan alat za skeniranje mreže. Može se pozvati putem `subprocess` modula u Pythonu. Nmap koristi razne tehnike, uključujući ARP skeniranje, ali je često preterano za jednostavnu detekciju prisustva.
*   **Pasivno prisluškivanje (sniffing):** Korišćenje biblioteka kao što je Scapy za pasivno presretanje ARP, ICMP ili drugih protokola kako bi se otkrili aktivni uređaji. Može biti manje nametljivo, ali zahteva više resursa i privilegije.

**Izbor:** ARP skeniranje putem Scapy biblioteke je verovatno najbolji balans između jednostavnosti, efikasnosti i fleksibilnosti za Python implementaciju.

### b) Identifikacija i skladištenje uređaja

*   **MAC adresa:** Najpouzdaniji identifikator za uređaje na lokalnoj mreži. Svakom mrežnom adapteru je dodeljena jedinstvena MAC adresa.
*   **IP adresa:** Dinamičke IP adrese (dodela putem DHCP-a) čine IP adresu manje pouzdanom za jedinstvenu identifikaciju tokom vremena. Može se koristiti kao sekundarni identifikator ili za praćenje promene adrese poznatog MAC-a.
*   **Hostname:** Moguće dobiti putem DNS upita, ali nije uvek dostupan ili pouzdan za sve uređaje.

**Skladištenje bele liste:**

*   **JSON/YAML fajl:** Jednostavan format za skladištenje liste MAC adresa i opcionih imena uređaja. Lako za čitanje i pisanje u Pythonu.
*   **SQLite baza podataka:** Robusnije rešenje za veći broj uređaja ili potrebu za dodatnim podacima (npr. poslednje viđeno vreme, IP istorija). Ugrađen u Python.

**Izbor:** Za početnu verziju, JSON fajl je dovoljan. Za naprednije funkcije, prelazak na SQLite je preporučljiv.

### c) Vremensko upravljanje i petlja nadzora

*   **`TIMEOUT`:** Za implementaciju `TIMEOUT` perioda, može se koristiti jednostavan tajmer (npr. `time.sleep()` u petlji) koji odbrojava vreme pre prelaska u režim alarma.
*   **Periodično skeniranje:** U režimu alarma, sistem mora periodično da skenira mrežu. To se može postići unutar beskonačne petlje sa `time.sleep()` pozivom između skeniranja.

### d) Mehanizam za pokretanje akcije (`ACTION`)

*   **Izvršavanje shell komandi:** `subprocess` modul u Pythonu omogućava izvršavanje spoljnih komandi ili skripti. Ovo je najfleksibilniji pristup za `ACTION`.
*   **Slanje e-pošte:** `smtplib` modul za slanje e-pošte preko SMTP servera.
*   **API pozivi:** Korišćenje `requests` biblioteke za slanje notifikacija preko servisa kao što su Pushbullet, Pushover, Telegram bot API, SMS gateway.

## 3. Postojeći alati i rešenja

Postoji nekoliko alata koji delimično ili potpuno ispunjavaju ciljeve TESTPROJ-a:

*   **ARPwatch:** Klasični Unix alat koji prati ARP aktivnost i upozorava na promene MAC-IP mapiranja, što može ukazati na nove uređaje ili ARP spoofing. Robustan, ali CLI orijentisan.
*   **Nmap:** Iako primarno skener, Nmap se može skriptovati za detekciju novih hostova. Nije rešenje "iz kutije" za kontinuirani nadzor.
*   **Fing:** Popularna mobilna i desktop aplikacija za skeniranje mreže i identifikaciju uređaja. Nudi detaljne informacije, ali nije open-source za prilagođavanje.
*   **Netdata / PRTG / Zabbix:** Kompleksniji alati za nadzor mreže koji mogu pratiti prisustvo hostova, ali su preterani za jednostavan zadatak TESTPROJ-a.
*   **Router-based Intrusion Detection:** Neki napredniji ruteri imaju ugrađene funkcije za detekciju nepoznatih uređaja, ali su često ograničene.
*   **Python projekti na GitHubu:** Postoje razni open-source projekti koji koriste Scapy za skeniranje mreže, ali retko sa fokusom na jednostavan whitelisting i alarmiranje kao primarnu funkciju.

TESTPROJ se izdvaja po svojoj jednostavnosti i fokusiranosti na automatsko generisanje bele liste i prilagodljivu akciju, ciljajući na korisnike koji traže specifično rešenje za ovaj problem bez kompleksnosti alata za nadzor čitave mreže.

## 4. Implementacija/Integracija u Pythonu

### a) Biblioteke

*   **`scapy`:** Nezaobilazan za ARP skeniranje. Omogućava kreiranje i slanje ARP paketa, kao i presretanje odgovora.
    *   *Primer:* `ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24"), timeout=2)`
*   **`json` / `sqlite3`:** Za skladištenje konfiguracije i bele liste.
*   **`time`:** Za implementaciju `TIMEOUT` i pauza između skeniranja.
*   **`subprocess`:** Za izvršavanje spoljnih komandi definisanih u `ACTION`.
*   **`logging`:** Za evidentiranje događaja i grešaka.
*   **`smtplib` / `requests`:** Opciono, za naprednije mehanizme obaveštavanja.

### b) Osnovna struktura koda (pseudokod)

```python
import scapy.all as scapy
import time
import json
import os
import logging
# (ostali importi za ACTION, npr. smtplib, subprocess)

# Konfiguracija (može biti iz fajla ili env varijabli)
TIMEOUT = 3600 # sekunde za fazu učenja
ACTION = "echo 'Unauthorized device detected!' >> alerts.log" # Primer akcije
WHITELIST_FILE = "whitelist.json"

# Logovanje
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_network_info():
    # Funkcija za dobijanje IP opsega lokalne mreže
    # Npr. 192.168.1.0/24
    # Može se koristiti `netifaces` biblioteka ili `ipconfig`/`ifconfig` komande
    return "192.168.1.0/24"

def scan_network(ip_range):
    # Skenira mrežu i vraća listu aktivnih MAC adresa
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        devices.append(element[1].hwsrc) # MAC adresa
    return devices

def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, 'r') as f:
            return json.load(f)
    return []

def save_whitelist(whitelist):
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(whitelist, f, indent=4)

def execute_action(message):
    logging.info(f"Pokrećem akciju: {message}")
    # Ovde se ACTION string izvršava, npr:
    # subprocess.run(ACTION, shell=True)
    # Ili poziv smtplib, requests itd.
    pass # Simulacija akcije

def main():
    whitelist = load_whitelist()
    network_range = get_network_info()
    learning_phase_end = time.time() + TIMEOUT

    logging.info("TESTPROJ pokrenut. Faza učenja...")

    # Faza učenja
    while time.time() < learning_phase_end:
        current_devices = scan_network(network_range)
        for mac in current_devices:
            if mac not in whitelist:
                whitelist.append(mac)
                logging.info(f"Dodat novi uređaj na belu listu: {mac}")
        save_whitelist(whitelist)
        time.sleep(30) # Skeniraj svakih 30 sekundi tokom faze učenja

    logging.info(f"Faza učenja završena. Bela lista sadrži {len(whitelist)} uređaja.")
    logging.info("Prebacivanje u režim alarma...")

    # Režim alarma
    while True:
        current_devices = scan_network(network_range)
        for mac in current_devices:
            if mac not in whitelist:
                alert_message = f"NEAUTORIZOVAN UREĐAJ DETEKTOVAN: {mac}"
                logging.warning(alert_message)
                execute_action(alert_message)
        time.sleep(60) # Skeniraj svakih 60 sekundi u režimu alarma

if __name__ == "__main__":
    main()
```

## 5. Ideje za dalji razvoj

1.  **Konfiguracioni fajl:** Umesto hardkodovanih `TIMEOUT` i `ACTION` varijabli, implementirati čitanje konfiguracije iz `config.ini`, `.env` ili YAML fajla.
2.  **Web interfejs:** Razviti jednostavan web interfejs (koristeći Flask ili FastAPI) za:
    *   Prikaz trenutno povezanih uređaja.
    *   Upravljanje belom listom (dodavanje/uklanjanje MAC adresa manuelno).
    *   Prikaz logova i obaveštenja.
    *   Konfigurisanje `TIMEOUT` i `ACTION`.
3.  **Naprednija identifikacija uređaja:**
    *   Lookup MAC adresa za proizvođača (OUI - Organizationally Unique Identifier) kako bi se prikazao vendora uređaja.
    *   Pokušaj rešavanja hostnama za detektovane IP adrese.
4.  **Persistentni podaci:** Koristiti SQLite bazu podataka za skladištenje:
    *   Bele liste (sa dodatnim informacijama kao što su ime uređaja, poslednji put viđeno, IP istorija).
    *   Logova detekcija neautorizovanih uređaja.
5.  **Poboljšani mehanizmi obaveštavanja:**
    *   Integracija sa Telegram botom.
    *   Integracija sa servisima za push notifikacije (npr. Pushover, Pushbullet).
    *   Slanje SMS poruka (preko Twilio ili sličnih servisa).
6.  **"Zaboravi uređaj" funkcionalnost:** Omogućiti brisanje uređaja sa bele liste.
7.  **Detaljnije logovanje:** Snimanje više detalja o detektovanim uređajima, uključujući IP adresu, vreme detekcije, itd.
8.  **Automatsko ponovno pokretanje:** Konfigurisanje aplikacije kao `systemd` servisa na Linuxu kako bi se automatski pokretala pri startovanju sistema i oporavila od grešaka.
9.  **Dockerizacija:** Pakovanje aplikacije u Docker kontejner radi lakšeg deploya i izolacije.
10. **Testovi:** Implementacija jedinica (unit) i integracionih testova za ključne komponente.
11. **Poboljšanje stabilnosti:** Bolje rukovanje greškama (npr. mrežni problemi, nedostajuće privilegije).
12. **Upozorenja o poznatim uređajima:** Detekcija promena (npr. MAC adresa poznatog IP-a, ili obrnuto) za uređaje na beloj listi, što može ukazivati na ARP spoofing.
