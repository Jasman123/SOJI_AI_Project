import json
from copy import deepcopy

def clean_ad_json(data):
    cleaned = {}

    def normalize(v):
        # Normalize "None" and empty strings
        if v in ["None", "", None]:
            return None
        return v  # keep lists/dicts intact

    for entry in data:
        ad_id = entry.get("ad_id")

        # Normalize AD ID
        if ad_id in ["None", "", None]:
            ad_id = None

        rules_block = entry.get("applicability_rules")

        # Ensure rules_block is a list
        if isinstance(rules_block, dict):
            rules_block = [rules_block]
        elif rules_block is None:
            rules_block = [{}]

        # Process each rule separately
        for r in rules_block:
            rule = {
                "aircraft_models": normalize(r.get("aircraft_models", [])) or [],
                "msn_constraints": normalize(r.get("msn_constraints")),
                "excluded_if_modifications": normalize(r.get("excluded_if_modifications", [])) or [],
                "required_modifications": normalize(r.get("required_modifications", [])) or []
            }

            # Create container
            if ad_id not in cleaned:
                cleaned[ad_id] = []

            # Avoid duplicates
            if rule not in cleaned[ad_id]:
                cleaned[ad_id].append(rule)

    # Convert dict → list format
    result = []
    for ad_id, rules in cleaned.items():
        result.append({
            "ad_id": ad_id,
            "applicability_rules": rules
        })

    return result


if __name__ == "__main__":
    with open("ad_results.json", "r") as f:
        data = json.load(f)

    cleaned_output = clean_ad_json(data)

    with open("cleaned.json", "w") as f:
        json.dump(cleaned_output, f, indent=2)

    print("Done! cleaned.json generated.")
