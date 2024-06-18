import json

# Sample grants database
grants_db = {
    "grant1": {
        "name": "Industrial Research Assistance Program (IRAP)",
        "taxonomy": ["business", "research", "innovation"],
        "grant_url": "https://nrc.canada.ca/en/support-technology-innovation/industrial-research-assistance-program",
        "inputs": {
            "project_description": "",
            "solution_description": "",
            "company_info": "",
            "visible_minority": False
        }
    },
    "grant2": {
        "name": "Strategic Innovation Fund (SIF)",
        "taxonomy": ["business", "innovation", "technology"],
        "grant_url": "https://ised-isde.canada.ca/site/strategic-innovation-fund/en",
        "inputs": {
            "project_description": "",
            "solution_description": "",
            "company_info": "",
            "visible_minority": False
        }
    },
    "grant3": {
        "name": "Canada Cultural Spaces Fund",
        "taxonomy": ["non-profit", "community", "arts", "culture"],
        "grant_url": "https://www.canada.ca/en/canadian-heritage/services/funding/cultural-spaces-fund.html",
        "inputs": {
            "project_description": "",
            "organization_info": "",
            "community_impact": ""
        }
    },
}


def get_user_profile():
    project_description = input("Please describe your project: ")
    solution_description = input("Please describe your proposed solution: ")
    company_info = input(
        "Please provide information about your company (industry, size, etc.): ")
    visible_minority = input(
        "Are you a visible minority? (yes/no): ").lower() == "yes"

    user_profile = {
        "project_description": project_description,
        "solution_description": solution_description,
        "company_info": company_info,
        "visible_minority": visible_minority
    }

    return user_profile


def search_grants(user_profile):
    relevant_grants = []
    for grant_id, grant_info in grants_db.items():
        match_count = 0
        for keyword in grant_info["taxonomy"]:
            if keyword.lower() in user_profile["project_description"].lower() or \
               keyword.lower() in user_profile["solution_description"].lower() or \
               keyword.lower() in user_profile["company_info"].lower():
                match_count += 1
        if match_count > 0:
            relevant_grants.append((grant_id, grant_info))

    return relevant_grants


def populate_application_form(grant_info, user_profile):
    grant_info["inputs"].update(user_profile)
    populated_form = json.dumps(grant_info["inputs"], indent=2)
    return populated_form


def main():
    user_profile = get_user_profile()
    relevant_grants = search_grants(user_profile)

    if not relevant_grants:
        print("No relevant grants found based on your profile.")
    else:
        print("Relevant grants found:")
        for i, (grant_id, grant_info) in enumerate(relevant_grants, start=1):
            print(f"{i}. {grant_info['name']}")
            print(f"   URL: {grant_info['grant_url']}")

        selected_grants = input(
            "Please enter the numbers of the grants you want to apply for (separated by commas): ")
        selected_grants = [int(x.strip()) for x in selected_grants.split(",")]

        for grant_number in selected_grants:
            grant_id, grant_info = relevant_grants[grant_number - 1]
            populated_form = populate_application_form(
                grant_info, user_profile)
            print(
                f"\nPopulated form for grant {grant_info['name']}:\n{populated_form}")


if __name__ == "__main__":
    main()
