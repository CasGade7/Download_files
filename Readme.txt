PDF Downloader

Beskrivelse:
Dette program downloader PDF-filer fra angivne URL'er, der er angivet i en Excel-fil. 
Det opdaterer også Excel-filen med status for om de er blevet downloadet, så du kan se, hvilke filer der er blevet hentet og gemmer denne fil/kopi i en ny mappe.

Funktioner:
Læser en Excel-fil med URL'er og downloader dem som PDF-dokumenter til en mappe.
Downloader op til 20 filer i alt, men begrænser samtidige downloads til maksimalt 10 ad gangen.
Opdaterer Excel-filen med downloadstatus (Ja/Nej) og gemmer den som en kopi i en anden mappe.

Installation:
Sørg for at have Python installeret, har har brugt Python version 3.12.
Installer de nødvendige biblioteker ved at køre:
pip install pandas aiohttp openpyxl

Brug:
Angiv stien til Excel-fil med URL'erne der skal downloades fra i variablen list_pth.
Angiv stien til den mappe hvor den opdaterede Excel-filen bliver gemt i variablen pth.
Angiv stien til den mappe hvor de downloadede pdf'ere bliver gemt i variablen dwn_pth.
Kør programmet.

Begrænsninger:
Disse begrænsninger er implementeret for at undgå at programmet bruger for meget ressourcer,
men har beskrevet nedenfor hvordan man andrer disse begrænsninger.
Programmet downloader maksimalt 20 filer i alt.
Det downloader kun 10 filer ad gangen for at undgå overbelastning af serveren.

Ændre begrænsninger:
Hvis du ønsker at ændre begrænsningerne for downloads, kan du justere disse linjer i koden:

For at ændre det maksimale antal filer, der kan downloades, skal du finde linjen:

if len(tasks) >= 20:
og ændre 20 til det ønskede antal.

For at ændre antallet af samtidige downloads, skal du finde disse 2 linjer:

current_tasks = tasks[:10]
tasks = tasks[10:]
og ændre 10 til det ønskede antal på begge linjer.

License
Specialisterne