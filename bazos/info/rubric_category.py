def get_rubric(country: str, rubric: str):
    if country.lower() == "cz":
        return rubric
    elif country.lower() == "sk":
        cz_idx = list(RUBRICS_CZ.keys()).index(rubric)
        sk_rubric = list(RUBRICS_SK.keys())[
            cz_idx
        ]
        return sk_rubric


def get_category(country: str, rubric: str, category: str):
    if country.lower() == "cz":
        return category
    elif country.lower() == "sk":
        cz_idx = RUBRICS_CZ[rubric].index(category)
        sk_category = RUBRICS_SK[get_rubric(country, rubric)][cz_idx]
        return sk_category


RUBRICS_CZ = {
    'Auto': [
        'Alfa Romeo', 'Audi', 'BMW', 'Chevrolet', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Honda', 'Hyundai', 'Kia',
        'Mazda', 'Mercedes-Benz', 'Mitsubishi', 'Nissan', 'Opel', 'Peugeot', 'Renault', 'Seat', 'Suzuki', 'Škoda',
        'Toyota', 'Volkswagen', 'Volvo', 'Havarovaná', 'Ostatní značky', 'Náhradní díly', 'Pneumatiky, kola',
        'Příslušenství', 'Tuning', 'Veteráni', 'Autobusy', 'Dodávky', 'Karavany, vozíky', 'Mikrobusy',
        'Nákladní auta', 'Pick-up', 'Ostatní užitková', 'Havarovaná užitková', 'Náhradní díly užitková'
    ],
    'Děti': [
        'Autosedačky', 'Baby monitory, chůvičky', 'Hračky', 'Chodítka a hopsadla', 'Kočárky', 'Kojenecké potřeby',
        'Kola', 'Nábytek pro děti', 'Nosítka', 'Odrážedla', 'Sedačky na kolo', 'Sportovní potřeby',
        'Školní potřeby', 'Ostatní', 'Body, dupačky a overaly', 'Bundy a kabátky', 'Čepice a kloboučky',
        'Kalhoty, kraťasy a tepláky', 'Kombinézy', 'Komplety', 'Mikiny a svetry', 'Obuv', 'Plavky',
        'Ponožky a punčocháče', 'Pyžámka a župánky', 'Rukavice a šály', 'Spodní prádlo', 'Sukýnky a šatičky',
        'Trička a košile', 'Ostatní oblečení'
    ],
    'Dům a zahrada': [
        'Bazény', 'Čerpadla', 'Dveře, vrata', 'Klimatizace', 'Kotle, Kamna, Bojlery',
        'Malotraktory, Kultivátory', 'Míchačky', 'Nářadí', 'Okna', 'Pily', 'Radiátory', 'Rostliny',
        'Sekačky', 'Sněžná technika', 'Stavební materiál', 'Vybavení dílen', 'Vysavače/Foukače',
        'Zahradní grily', 'Zahradní technika', 'Ostatní'
    ],
    'Elektro': [
        'Autorádia', 'Digestoře', 'Domácí kina', 'Epilátory, Depilátory', 'Fény, Kulmy', 'Hifi systémy, Rádia',
        'Holící strojky', 'Kávovary', 'Ledničky', 'Mikrovlnné trouby', 'Mrazáky', 'Myčky', 'Nabíječky baterií',
        'Pračky', 'Projektory', 'Repro soustavy', 'Ruční šlehače, Mixéry', 'Šicí stroje', 'Sluchátka',
        'Sporáky', 'Sušičky', 'Svítidla, Lampy', 'Televize', 'Video, DVD přehrávače', 'Vysavače', 'Vysílačky',
        'Zesilovače', 'Zvlhčovače vzduchu', 'Žehličky', 'Ostatní - bílá', 'Ostatní audio video',
        'Ostatní drobné'
    ],
    'Foto': [
        'Analogové fotoaparáty', 'Digitální fotoaparáty', 'Drony', 'Videokamery', 'Zrcadlovky', 'Baterie',
        'Blesky a osvětlení', 'Brašny a pouzdra', 'Datové kabely', 'Filtry', 'Nabíječky baterií', 'Objektivy',
        'Paměťové karty', 'Stativy', 'Ostatní'
    ],
    'Hudba': [
        'Bicí nástroje', 'Dechové nástroje', 'Klávesové nástroje', 'Smyčcové nástroje', 'Strunné nástroje',
        'Ostatní nástroje', 'DVD, CD, MC, LP', 'Hudebníci a skupiny', 'Koncerty', 'Noty, texty',
        'Světelná technika', 'Zkušebny', 'Zvuková technika', 'Ostatní'
    ],
    'Knihy': [
        'Beletrie', 'Časopisy', 'Cizojazyčná literatura', 'Detektivky', 'Dětská literatura', 'Drama',
        'Encyklopedie', 'Esoterika', 'Historické romány', 'Hobby, odborné knihy', 'Kuchařky',
        'Mapy, cestovní průvodci', 'Počítačová literatura', 'Pro mládež', 'Romány pro ženy', 'Sci-fi, Fantasy',
        'Učebnice, skripta - Jazykové', 'Učebnice, skripta - SŠ', 'Učebnice, skripta - VŠ',
        'Učebnice, skripta - ZŠ', 'Zábavná', 'Zdravý životní styl', 'Ostatní'
    ],
    'Mobily': [
        'Apple', 'HTC', 'Huawei, Honor', 'LG', 'Motorola, Lenovo', 'Nokia, Microsoft', 'Samsung', 'Sony',
        'Xiaomi', 'Ostatní značky', 'Baterie', 'Bezdrátové telefony', 'Datové kabely', 'Faxy', 'Headsety',
        'HF Sady do auta', 'Chytré hodinky', 'Kryty', 'Nabíječky', 'Paměťové karty', 'Stolní telefony',
        'Ostatní'
        ''],
    'Motorky': [
        'Cestovní motocykly', 'Chopper', 'Čtyřkolky', 'Enduro', 'Minibike', 'Mopedy', 'Silniční motocykly',
        'Skútry', 'Skútry sněžné', 'Skútry vodní', 'Tříkolky', 'Veteráni', 'Náhradní díly',
        'Oblečení, obuv, helmy', 'Ostatní'
    ],
    'Nábytek': [
        'Jídelní kouty', 'Knihovny', 'Koberce a podlah. krytina', 'Koupelny', 'Křesla a gauče', 'Kuchyně',
        'Lampy, osvětlení', 'Ložnice', 'Matrace', 'Obývací stěny', 'Postele', 'Sedací soupravy', 'Skříně',
        'Stoly', 'Zahradní nábytek', 'Židle', 'Doplňky', 'Ostatní nábytek'
    ],
    'Oblečení': [
        'Batohy, Kufry', 'Boty', 'Bundy a Kabáty', 'Čepice a Šátky', 'Doplňky', 'Džíny', 'Halenky', 'Hodinky',
        'Kabelky', 'Kalhoty', 'Košile', 'Kožené oděvy', 'Mikiny', 'Obleky a Saka', 'Plavky', 'Roušky',
        'Rukavice a Šály', 'Šaty, Kostýmky', 'Šortky', 'Šperky', 'Spodní prádlo', 'Sportovní oblečení',
        'Sukně', 'Svatební šaty', 'Těhotenské oblečení', 'Svetry', 'Termo prádlo', 'Trička, tílka', 'Ostatní'
    ],
    'PC': [
        'Chladiče', 'DVD, Blu-ray mechaniky', 'GPS navigace', 'Grafické karty', 'Hard disky, SSD', 'Herní konzole',
        'Herní zařízení', 'Hry', 'Klávesnice, myši', 'Kopírovací stroje', 'LCD monitory', 'Modemy', 'Myši',
        'Notebooky', 'Paměti', 'PC, Počítače', 'Procesory', 'Scanery', 'Síťové prvky', 'Skříně, zdroje', 'Software',
        'Spotřební materiál', 'Tablety, E-čtečky', 'Tiskárny', 'Wireless, WiFi', 'Základní desky', 'Záložní zdroje',
        'Zvukové karty', 'Ostatní'
    ],
    'Práce': [
        'Administrativa', 'Brigády', 'Chemie a potravinářství', 'Doprava a logistika', 'Finance a ekonomika',
        'IT a telekomunikace', 'Management', 'Marketing a reklama', 'Obchod a prodej', 'Obrana a bezpečnost',
        'Pohostinství a ubytování', 'Práce v domácnosti', 'Právo, legislativa', 'Průmysl a výroba',
        'Řemeslné práce', 'Servis a služby', 'Stavebnictví', 'Technika a energetika', 'Tisk a polygrafie',
        'Výzkum a vývoj', 'Vzdělávání a personalistika', 'Zdravotnictví', 'Zemědělství', 'Ostatní'
    ],
    'Reality': [
        'Prodej', 'Pronájem'
    ],
    'Služby': [
        'Auto Moto', 'Cestování', 'Domácí práce', 'Esoterika', 'Hlídání dětí', 'IT, webdesign', 'Koně - služby',
        'Kurzy a školení', 'Opravy, servis', 'Pořádání akcí', 'Právo a bezpečnost', 'Překladatelství',
        'Přeprava a Stěhování', 'Půjčovny', 'Realitní služby', 'Reklama na auto', 'Reklamní plochy - ostatní',
        'Řemeslné a stavební práce', 'Služby pro zvířata', 'Tvůrčí služby', 'Ubytování',
        'Účetnictví, poradenství', 'Úklid', 'Výroba', 'Výuka hudby', 'Výuka, doučování', 'Zdraví a krása',
        'Zprostředkovatelské služby', 'Ostatní'
    ],
    'Sport': [
        'Fitness, jogging', 'Fotbal', 'Golf', 'In-line, Skateboarding', 'Kempink', 'Letectví', 'Míčové hry',
        'Myslivost, lov', 'Paintball, airsoft', 'Rybaření', 'Společenské hry', 'Tenis, squash, badminton',
        'Turistika, horolezectví', 'Vodní sporty, potápění', 'Vše ostatní', 'Koloběžky', 'Horská kola',
        'Silniční kola', 'Součástky a díly', 'Ostatní cyklistika', 'Běžkování', 'Lyžování', 'Skialpy',
        'Snowboarding', 'Hokej, bruslení', 'Ostatní zimní'
    ],
    'Stroje': [
        'Čerpadla', 'Čistící stroje', 'Dřevoobráběcí stroje', 'Generátory', 'Historické stroje',
        'Kovoobráběcí stroje', 'Motory', 'Potravinářské stroje', 'Skladová technika', 'Stavební stroje',
        'Textilní stroje', 'Tiskařské stroje', 'Vybavení provozoven', 'Výrobní linky', 'Zemědělská technika',
        'Náhradní díly', 'Ostatní'
    ],
    'Vstupenky': [
        'Dálniční známky', 'Dárkové poukazky', 'Jízdenky', 'Letenky', 'Permanentky', 'Divadlo', 'Festivaly',
        'Hudba, Koncerty', 'Pro děti', 'Společenské akce', 'Sport', 'Výstavy', 'Ostatní'
    ],
    'Zvířata': [

        'Akvarijní rybičky', 'Drobní savci', 'Kočky', 'Koně', 'Koně - potřeby', 'Psi', 'Ptactvo',
        'Terarijní zvířata', 'Ostatní domácí zvířata', 'Krytí', 'Ztraceni a nalezeni', 'Chovatelské potřeby',
        'Drůbež', 'Králíci', 'Ovce a kozy', 'Prasata', 'Skot', 'Ostatní hospodářská zvířata'

    ],
    'Ostatní': [
        'Mince, bankovky', 'Modelářství', 'Potraviny', 'Sběratelství', 'Sklo, keramika', 'Starožitnosti',
        'Umělecké předměty', 'Zdraví a krása', 'Známky, pohledy', 'Ostatní'
    ]
}

RUBRICS_SK = {
    'Auto': [
        'Alfa Romeo', 'Audi', 'BMW', 'Chevrolet', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Honda', 'Hyundai', 'Kia',
        'Mazda', 'Mercedes-Benz', 'Mitsubishi', 'Nissan', 'Opel', 'Peugeot', 'Renault', 'Seat', 'Suzuki', 'Škoda',
        'Toyota', 'Volkswagen', 'Volvo', 'Havarované', 'Ostatné značky', 'Náhradné diely', 'Pneumatiky, kolesá',
        'Príslušenstvo', 'Tuning', 'Veterány', 'Autobusy', 'Dodávky', 'Karavany, vozíky', 'Mikrobusy',
        'Nákladné autá', 'Pick-up', 'Ostatná užitková', 'Havarované užitková', 'Náhradné diely užitková'
    ],
    'Deti': [
        'Autosedačky', 'Baby monitory', 'Bicykle', 'Hračky', 'Chodítka a hopsadlá', 'Kočíky', 'Kojenecké potreby',
        'Nábytok pre deti', 'Nosiče', 'Odrážadlá', 'Sedačky na bicykel', 'Školské potreby', 'Športové potreby',
        'Ostatné', 'Body, dupačky a overaly', 'Bundy a kabátiky', 'Čiapky a klobúčiky', 'Kombinézy', 'Komplety',
        'Mikiny a svetre', 'Nohavice, kraťasy a tepláky', 'Obuv', 'Plavky', 'Ponožky a pančušky',
        'Pyžamká a župančeky', 'Rukavice a šály', 'Spodná bielizeň', 'Sukničky a šatočky', 'Tričká a košieľky',
        'Ostatné oblečenie'
    ],
    'Dom a záhrada': [
        'Bazény', 'Čerpadlá', 'Dvere, brány', 'Klimatizácie', 'Kosačky', 'Kotle, Kachle, Bojlery',
        'Malotraktory, Kultivátory', 'Miešačky', 'Náradie', 'Okná', 'Píly', 'Radiátory', 'Rastliny',
        'Snežná technika', 'Stavebný materiál', 'Vybavenie dielne', 'Vysávače/Fúkače',
        'Záhradná technika', 'Záhradné grily', 'Ostatné'
    ],
    'Elektro': [
        'Autorádiá', 'Chladničky', 'Digestory', 'Domáce kiná', 'Epilátory, Depilátory', 'Fény, Kulmy',
        'Hifi systémy, Rádiá', 'Holiace strojčeky', 'Kávovary', 'Mikrovlnné rúry', 'Mrazničky',
        'Nabíjačky batérií', 'Práčky', 'Projektory', 'Repro sústavy', 'Ručné šľahače, Mixéry', 'Šijacie stroje',
        'Slúchadlá', 'Sporáky', 'Sušičky', 'Svietidlá, Lampy', 'Televízory', 'Umývačky riadu',
        'Video, DVD prehrávače', 'Vysávače', 'Vysielačky', 'Zosilňovače', 'Zvlhčovače vzduchu', 'Žehličky',
        'Ostatné - biela', 'Ostatné audio video', 'Ostatné drobné'
    ],
    'Foto': [
        'Kinofilm', 'Digitálne fotoaparáty', 'Drony', 'Videokamery', 'Zrkadlovky', 'Batérie',
        'Blesky a osvetlenie', 'Brašne a púzdra', 'Dátové káble', 'Filtre', 'Nabíjačky', 'Objektívy',
        'Pamäťové karty', 'Statívy', 'Ostatné'
    ],
    'Hudba': [
        'Bicie nástroje', 'Dychové nástroje', 'Klávesové nástroje', 'Sláčikové nástroje', 'Strunové nástroje',
        'Ostatné nástroje', 'DVD, CD, MC, LP', 'Hudobníci a skupiny', 'Koncerty', 'Noty, texty', 'Skúšobne',
        'Svetelná technika', 'Zvuková technika', 'Ostatné'
    ],
    'Knihy': [
        'Beletria', 'Časopisy', 'Cudzojazyčná literatúra', 'Detektívky', 'Detská literatúra', 'Dráma',
        'Encyklopédie', 'Ezoterika', 'Historické romány', 'Hobby, odborné knihy', 'Kuchárky', 'Mapy, cestovanie',
        'Počítačová literatúra', 'Pre mládež', 'Romány pre ženy', 'Sci-fi, Fantasy',
        'Učebnice, skriptá - Jazykové', 'Učebnice, skriptá - SŠ', 'Učebnice, skriptá - VŠ',
        'Učebnice, skriptá - ZŠ', 'Zábavná literatúra', 'Zdravý životný štýl', 'Ostatné'
    ],
    'Mobily': [
        'Apple', 'HTC', 'Huawei, Honor', 'LG', 'Motorola, Lenovo', 'Nokia, Microsoft', 'Samsung', 'Sony',
        'Xiaomi', 'Ostatné značky', 'Batérie', 'Bezdrôtové telefóny', 'Dátové kabely', 'Faxy', 'Headsety',
        'HF Sady do auta', 'Inteligentné hodinky', 'Klasické telefóny', 'Kryty', 'Nabíjačky', 'Pamäťové karty',
        'Ostatné'
    ],
    'Motocykle': [
        'Cestné motocykle', 'Cestovné motocykle', 'Chopper', 'Enduro', 'Minibike', 'Mopedy', 'Skútre',
        'Skútre snežné', 'Skútre vodné', 'Štvorkolky', 'Trojkolky', 'Veterány', 'Náhradné diely',
        'Oblečenie, obuv, helmy', 'Ostatné'
    ],
    'Nábytok': [
        'Jedálenské kúty', 'Knižnice', 'Koberce a podlahová krytina', 'Kreslá a gauče', 'Kuchyne', 'Kúpeľne',
        'Lampy, osvetlenie', 'Matrace', 'Obývacie steny', 'Postele', 'Sedacie súpravy', 'Skrine', 'Spálne',
        'Stoličky', 'Stoly', 'Záhradný nábytok', 'Doplnky', 'Ostatný nábytok'
    ],
    'Oblečenie': [
        'Blúzky', 'Bundy a Kabáty', 'Čiapky, Šatky', 'Doplnky', 'Džínsy', 'Funkčné prádlo', 'Hodinky',
        'Kabelky', 'Košele', 'Kožené oblečenie', 'Mikiny', 'Nohavice', 'Obleky, Saká', 'Plavky',
        'Plecniaky a kufre', 'Rukavice a Šály', 'Rúška', 'Šaty, Kostýmy', 'Šortky', 'Šperky',
        'Spodná bielizeň', 'Športové oblečenie', 'Sukne', 'Svadobné šaty', 'Svetre', 'Tehotenské oblečenie',
        'Topánky, obuv', 'Tričká, roláky, tielka', 'Ostatné'
    ],
    'PC': [
        'Chladiče', 'DVD, Blu-ray mechaniky', 'FDD, ZIPy', 'GPS navigácia', 'Grafické karty', 'Hard disky, SSD',
        'Herné konzoly', 'Herné zariadenia', 'Hry', 'Klávesnice', 'Kopírovacie stroje', 'LCD monitory', 'Modemy',
        'Myši', 'Notebooky', 'Pamäte', 'PC, Počítače', 'Procesory', 'Scanery', 'Sieťové komponenty',
        'Skrine, zdroje', 'Software', 'Spotrebný materiál', 'Tablety, E-čítačky', 'Tlačiarne', 'Wireless, WiFi',
        'Základné dosky', 'Záložné zdroje', 'Zvukové karty', 'Ostatné'
    ],
    'Práca': [
        'Administratíva', 'Brigády', 'Chémia a potravinárstvo', 'Doprava a logistika', 'Financie a ekonomika',
        'IT a telekomunikácie', 'Management', 'Marketing a reklama', 'Obchod a predaj', 'Obrana a bezpečnosť',
        'Pohostinstvá a ubytovanie', 'Poľnohospodárstvo', 'Práca v domácnosti', 'Právo, legislatíva',
        'Priemysel a výroba', 'Remeselné práce', 'Servis a služby', 'Stavebníctvo', 'Technika a energetika',
        'Tlač a polygrafia', 'Výskum a vývoj', 'Vzdelávánie a personalistika', 'Zdravotníctvo', 'Ostatné'
    ],
    'Reality': [
        'Predaj', 'Prenájom'
    ],
    'Služby': [
        'Auto Moto', 'Cestovanie', 'Domáce práce', 'Ezoterika', 'IT, webdesign', 'Kone - služby',
        'Kurzy a školenia', 'Opravy a servis', 'Organizovanie akcií', 'Požičovne', 'Právo a bezpečnosť',
        'Prekladateľstvo', 'Preprava a sťahovanie', 'Realitné služby', 'Reklama na auto',
        'Reklamné plochy - ostatné', 'Remeselné a stavebné práce', 'Služby pre zvieratá',
        'Sprostredkovateľské služby', 'Stráženie detí', 'Tvorivá práca', 'Ubytovanie',
        'Účtovníctvo, poradenstvo', 'Upratovanie', 'Výroba', 'Výuka hudby', 'Výuka, doučovanie',
        'Zdravie a krása', 'Ostatné'
    ],
    'Šport': [
        'Fitness, jogging', 'Futbal', 'Golf', 'In-lines, Skateboarding', 'Kemping', 'Letectvo', 'Loptové hry',
        'Paintball, airsoft', 'Poľovníctvo', 'Rybolov', 'Spoločenské hry', 'Tenis, squash, badminton',
        'Turistika, horolezectvo', 'Vodné športy, potápanie', 'Všetko ostatné', 'Kolobežky', 'Cestné bicykle',
        'Horské bicykle', 'Súčiastky a diely', 'Ostatná cyklistika', 'Bežkovanie', 'Lyžovanie', 'Skialpy',
        'Snowboarding', 'Hokej, korčuľovanie', 'Ostatné zimné'
    ],
    'Stroje': [
        'Čerpadlá', 'Čistiace stroje', 'Drevoobrábacie stroje', 'Generátory', 'Historické stroje',
        'Kovoobrábacie stroje', 'Motory', 'Poľnohospodárska technika', 'Potravinárske stroje',
        'Skladová technika', 'Stavebné stroje', 'Textilné stroje', 'Tlačiarenské stroje',
        'Vybavenie prevádzkarne', 'Výrobná linka', 'Náhradné diely', 'Ostatné'
    ],
    'Vstupenky': [
        'Darčekové poukážky', 'Diaľničné známky', 'Cestovné lístky', 'Letenky', 'Permanentky', 'Divadlo',
        'Festivaly', 'Hudba, Koncerty', 'Pre deti', 'Spoločenské akcie', 'Šport', 'Výstavy', 'Ostatné'
    ],
    'Zvieratá': [
        'Akvarijné rybičky', 'Drobné cicavce', 'Kone', 'Kone - potreby', 'Mačky', 'Psy', 'Terárijné zvieratá',
        'Vtáctvo', 'Ostatné domáce zvieratá', 'Krytie', 'Stratení a nájdení', 'Chovateľské potreby', 'Dobytok',
        'Hydina', 'Králiky', 'Ovce a kozy', 'Prasatá', 'Ostatné hospodárske zvieratá'
    ],
    'Ostatné': [
        'Mince, bankovky', 'Modelárstvo', 'Potraviny', 'Sklo, keramika', 'Starožitnosti', 'Umelecké predmety',
        'Zberateľstvo', 'Zdravie a krása', 'Známky, pohľadnice', 'Ostatné'
    ]
}
