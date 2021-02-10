import requests

# urls of rmv api anzeigetafel
current_time = re.findall(r'\d\d:\d\d:\d\d', str(datetime.now()))[0]
urls = [
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=MainzHaupt_3006904_396855748&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=FrankfurtM_3001830_1780579642&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=Rsselsheim_3004912_59409684&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=MainzMnste_3025439_1601009508&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=MainzHecht_3029139_1212749291&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=MainzMnchf_3029013_1498928858&dataOnly=true&start=1maxJourneys=198&{current_time}"
]
stations = [
    'Mainzer Hauptbahnhof',
    'Frankfurter Hauptbahnhof',
    'Rüsselsheimer Bahnhof',
    'Mainz Münsterplatz', 
    'Mainz Am Schinnergraben', 
    'Mainz Im Münchfeld'
    ]
	