from db import Base, Grant,engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Create some grants
grant1 = Grant(
    grant_name="Industrial Research Assistance Program (IRAP)",
    grant_url="https://nrc.canada.ca/en/support-technology-innovation/industrial-research-assistance-program",
    grant_amount="Varies",
    submission_timeline="Ongoing",
    application_process="Online application through NRC website",
    grant_category="Business",
    sponsor="National Research Council Canada",
    additional_info="Provides advisory services and funding to help Canadian small and medium-sized businesses increase their innovation capacity and take ideas to market.",
    conditions="Must be a Canadian business Focus on innovation",
    eligibility_criteria="Canadian SMEs Innovative projects",
    unusual_conditions="Must demonstrate potential for commercialization",
    domain="industry"
)



grant2 = Grant(
    grant_name="Strategic Innovation Fund (SIF)",
    grant_url="https://ised-isde.canada.ca/site/strategic-innovation-fund/en",
    grant_amount="Varies",
    submission_timeline="Ongoing",
    application_process="Online application through ISED website",
    grant_category="Business",
    sponsor="Innovation, Science and Economic Development Canada",
    additional_info="Supports innovative projects in key sectors of the Canadian economy.",
    conditions="Must be a Canadian non-profit organization Focus on arts and culture",
    eligibility_criteria="Canadian non-profit organizations Arts and culture projects",
    domain="arts"
)

grant3 = Grant(
    grant_name="Canada Cultural Spaces Fund",
    grant_url="https://www.canada.ca/en/canadian-heritage/services/funding/cultural-spaces-fund.html",
    grant_amount="Varies",
    submission_timeline="Ongoing",
    application_process="Online application through Canadian Heritage website",
    grant_category="Non-Profit",
    sponsor="Canadian Heritage",
    additional_info="Supports the improvement, renovation, and construction of arts and heritage facilities.",
    conditions="Must be a Canadian non-profit organization Focus on arts and heritage facilities",
    eligibility_criteria="Canadian non-profit organizations Arts and heritage projects",
    domain="arts"
)

#education
grant4 = Grant(
    grant_name="Canada Research Chairs Program",
    grant_url="http://www.chairs-chaires.gc.ca/home-accueil-eng.aspx",
    grant_amount="Varies",
    submission_timeline="Ongoing",
    application_process="Online application through the Canada Research Chairs Program website",
    grant_category="Education",
    sponsor="Canada Research Chairs Program",
    additional_info="Supports research excellence in engineering, natural sciences, health sciences, social sciences, and humanities.",
    conditions="Must be a Canadian educational institution Focus on research and innovation",
    eligibility_criteria="Canadian educational institutions Research and innovation projects",
    domain="education"
)

# ai

grant5 = Grant(
    grant_name="AI for Society",
    grant_url="https://www.nserc-crsng.gc.ca/Innovate-Innover/AI-AI/AFS-SEA_eng.asp",
    grant_amount="Varies",
    submission_timeline="Ongoing",
    application_process="Online application through NSERC website",
    grant_category="Business",
    sponsor="Natural Sciences and Engineering Research Council of Canada",
    additional_info="Supports research and development projects that use artificial intelligence to address societal challenges.",
    conditions="Must be a Canadian business Artificial intelligence projects",
    eligibility_criteria="Canadian businesses",
    domain="ai"
)

# Add the grants to the session and commit
session.add(grant1)
session.add(grant2)
session.add(grant3)
session.commit()


# Query the database
grants = session.query(Grant).all()
for grant in grants:
    print(f"Grant Name: {grant.grant_name}")
    print(f"URL: {grant.grant_url}")
    print(f"Amount: {grant.grant_amount}")
    print(f"Submission Timeline: {grant.submission_timeline}")
    print(f"Application Process: {grant.application_process}")
    print(f"Category: {grant.grant_category}")
    print(f"Sponsor: {grant.sponsor}")
    print(f"Additional Info: {grant.additional_info}")
    print(f"Conditions: {grant.conditions}")
    print(f"Eligibility Criteria: {grant.eligibility_criteria}")
    print(f"Unusual Conditions: {grant.unusual_conditions}")