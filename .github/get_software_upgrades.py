import requests

rest = "https://lcd.osmosis.zone"
gov_version = "v1"

r = requests.get("{}/cosmos/gov/{}/proposals?pagination.limit=1000".format(rest, gov_version))
proposals = r.json()["proposals"]

legacyUrl = "/cosmos.gov.v1.MsgExecLegacyContent"
v1SoftwareUrl = "/cosmos.upgrade.v1beta1.MsgSoftwareUpgrade"
v1beta1SoftwareUrl = "/cosmos.upgrade.v1beta1.SoftwareUpgradeProposal"
upgrades = []

for p in proposals:
  if p["status"] != "PROPOSAL_STATUS_PASSED":
    continue

  if gov_version == "v1":
    for m in p["messages"]:
      if m["@type"] == v1SoftwareUrl:
        upgrades.append({
          "name": m["plan"]["name"],
          "height": int(m["plan"]["height"])
        })
      elif m["@type"] == legacyUrl:
        if m["content"]["@type"] == v1SoftwareUrl or m["content"]["@type"] == v1beta1SoftwareUrl:
          upgrades.append({
            "name": m["content"]["plan"]["name"],
            "height": int(m["content"]["plan"]["height"])
          })
  
  if gov_version == "v1beta1":
    if p["content"]["@type"] == v1beta1SoftwareUrl:
      upgrades.append({
        "name": p["content"]["plan"]["name"],
        "height": int(p["content"]["plan"]["height"])
      })

for u in upgrades:
  print("- name: {}".format(u["name"]))
  print("  height: {}".format(u["height"]))
