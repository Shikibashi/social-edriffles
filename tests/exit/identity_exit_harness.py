"""Deterministic identity exit characterization; simulated portions are explicit."""
import json

def run():
    state={"did":"did:plc:example","handle":"alice.example","pds":"A","appview":"X","provider":"feed-x","preferences":{"freshness":.8,"topics":["science"]},"oldSession":"revoked"}
    for field,value in (("pds","B"),("appview","Y"),("provider","feed-y")): state[field]=value
    exported={"did":state["did"],"preferences":state["preferences"]}
    restored=json.loads(json.dumps(exported,sort_keys=True))
    assert restored["did"]==state["did"] and restored["preferences"]==state["preferences"]
    assert state["oldSession"]=="revoked"
    return {"simulated":True,"didContinuous":True,"repositoryContinuity":"protocol-dependent","preferencesRestored":True,"oldSessionRevoked":True,"credentialsExported":False}
if __name__=='__main__': print(json.dumps(run(),sort_keys=True))
