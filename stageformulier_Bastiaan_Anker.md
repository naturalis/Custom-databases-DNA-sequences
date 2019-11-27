## Omschrijving van de afstudeeropdracht, zoals deze door de betreffende instantie is geformuleerd:

Voor de Europese kaderrichtlijnen Water (WFD) en Marien (MSFD) worden met regelmaat zoete en zoute wateren onderzocht op aanwezige soorten macrofauna - oa insecten, schelpdieren, krabben en wormen. De aangetroffen soortensamenstelling wordt gebruikt als indicator voor de ecologische kwaliteit van het waterlichaam. Traditioneel worden soorten gevangen, gesorteerd en gedetermineerd, wat zeer tijdrovend is, foutgevoelig en kostbaar. Naturalis werkt aan genetische technieken om soorten te identificeren op basis van hun DNA ('metabarcoding'). In een waterlichaam wordt een monster genomen waarvan het aanwezige DNA wordt vergeleken (middels Blast searches) met de DNA profielen van soorten in (inter)nationale DNA bibliotheken. Helaas blijken deze bibliotheken nogal eens vervuild doordat soorten verkeerd zijn geïdentificeerd of onder een verouderde taxonomische naam zijn ingevoerd. Naturalis beheert hiertoe eigen interne databases (als referentie) die gedeeltelijk gesynchroniseerd zijn met publieke databases en gedeeltelijk gevoed worden door intern sequencen. Op dit moment geschied het samenstellen van interne databases nog handmatig. In dit project zouden we graag een systeem ontwikkeld zien waarmee we periodiek data uit de internationale bibliotheek exporteren, via rekenregels controleren op betrouwbaarheid en zodoende de interne database incrementeel kunnen updaten.

Deze interne databases moeten op een aantal manieren beheerd worden:
-	Samenstelling en kwaliteit moeten inzichtelijk zijn via rapportages
-	Externe data moeten toegevoegd kunnen worden zonder duplicaties, eerder waargenomen externe data van lage kwaliteit moeten permanent geblokkeerd worden
-	Diverse ‘views’ – bijvoorbeeld taxonomische filters, of filters op basis van te definiëren kwaliteitscriteria – moeten toepasbaar zijn

De opdracht bestaat dan ook uit:
1.	Verzamelen van de specifieke requirements bij de diverse stakeholders binnen Naturalis: i) de laboratoria, ii) de gebruikers, net name van BioMon, iii) de bioinformatici
2.	Ontwikkelen van relationele database met metadata over sequentierecords
3.	Koppelen van geïndexeerde BLAST-data aan de relationele database
4.	Koppelen van KLASSE-data aan de relationele database
5.	Koppelen van collectie registratiesysteemdata aan de relationele database
6.	CRUD operaties op de database mogelijk maken (bijvoorbeeld via Galaxy) en selecties (op basis van marker of taxon) kunnen exporteren als fasta voor local Blast*.

* Ter indicatie: de NT database van GenBank is ~350 GB waar om het Blasten efficient te laten verlopen selecties van worden gemaakt (COI, 16S, 12S,18S, ITS, MatK, Rbcl en trnL). Databases die oa. worden gebruikt zijn Bold (~4GB), Unite (~1 GB) en Silva (~6 GB).



## Beschrijving van de aard van de werkzaamheden die je gaat uitvoeren, teneinde deze afstudeeropdracht tot een goed einde te brengen:

-	Contact leggen en overleggen met belanghebbenden binnen de organisatie
-	Verzamelen van requirements
-	Ontwikkelen van een plan van aanpak 
-	Ontwerpen van database schema (ERD, SQL)
-	Ontwikkelen van object relational mappings voor database (Python)
-	Ontwikkelen van views/rapportages/visualizaties van de database (Python, HTML)
-	Ontwikkelen van controllers voor CRUD-operaties (Python)
-	Verslaglegging in woord en schrift
-	Bijwonen van groepsoverleg
