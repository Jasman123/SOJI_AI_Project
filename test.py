import json

data_test = [
    {"Aircraft Model": "MD-11", "MSN": 48123, "Modifications": "None"},
    {"Aircraft Model": "DC-10-30F", "MSN": 47890, "Modifications": "None"},
    {"Aircraft Model": "Boeing 737-800", "MSN": 30123, "Modifications": "None"},
    {"Aircraft Model": "A320-214", "MSN": 5234, "Modifications": "None"},
    {"Aircraft Model": "A320-232", "MSN": 6789, "Modifications": "mod 24591 (production)"},
    {"Aircraft Model": "A320-214", "MSN": 7456, "Modifications": "SB A320-57-1089 Rev 04"},
    {"Aircraft Model": "A321-111", "MSN": 8123, "Modifications": "None"},
    {"Aircraft Model": "A321-112", "MSN": 364, "Modifications": "mod 24977 (production)"},
    {"Aircraft Model": "A319-100", "MSN": 9234, "Modifications": "None"},
    {"Aircraft Model": "MD-10-10F", "MSN": 46234, "Modifications": "None"}
]


with open("cleaned.json", 'r') as f:
        data = json.load(f)



for item in data_test:
    aircraft_model = item["Aircraft Model"]
    msn = item["MSN"]
    modifications = item["Modifications"]

    # print(f"Aircraft Model: {aircraft_model}, MSN: {msn}, Modifications: {modifications}")
    applicable_ads = []
    for ad in data:
        applicability_rules = ad.get("applicability_rules", [])
        for rule in applicability_rules:
            models = rule.get("aircraft_models", [])
            msn_constraints = rule.get("msn_constraints", None)
            excluded_mods = rule.get("excluded_if_modifications", [])
            required_mods = rule.get("required_modifications", [])

            msn_check = False
            models_check = False
            modifications_check = False

            # Check aircraft model
            if aircraft_model not in models:
                continue
            # Check MSN constraints
            msn_constraints = msn_constraints.lower() if msn_constraints else ""

            if msn_constraints not in ["none", "", None, "all"]:
                continue

            applicable_ads.append(f"AD ID: {ad['ad_id']} - model match , msn check ok/no")
            
                 

            
    print(f"Aircraft Model: {aircraft_model}, MSN: {msn}, Modifications: {modifications}")
    print(f"Applicable ADs: {applicable_ads}\n")



      

            

    