 #!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
#
import json
# Complete
#z=["σύνδεσμοι.json","προθέσεις.json","μόρια.json","επιφωνήματα.json", "επιρρήματα.json"]
#άρθρα.json, ουσιαστικά.json
#z=["αντωνυμίες.json"]
#επίθετα.json
z=["ρήματα.json"]
acc = []
for zz in z:
	f=open(zz)
	data = f.read()
	f.close()
	js = json.loads(data, 'utf-8')
	
	for k,v in js.items():
		for vv in v:
			for k2, v2 in vv.items():
				for k3,v3 in v2.items():
					for k4,v4 in v3.items():
						for k5, v5 in v4.items():
							for katal in v5["καταλήξεις"]:
								for ypo in katal:
									if ypo not in acc:
										acc.append(ypo)
acc=list(set(acc))
for a in acc:
	print(a)