from typing import List, Optional
from pydantic.v1 import BaseModel, Field

class MergedSurvey(BaseModel):
    # Personal Details
    name: Optional[str] = Field(description="Name of the user")
    email: Optional[str] = Field(description="Email of the user")
    website: Optional[str] = Field(description="Website of the user")
    position: Optional[str] = Field(description="Position of the user, CEO, CTO, CIO, Founder or if others please specify")

    # General Problem Identification
    skills: Optional[str] = Field(description="""* Not identifying the right AI use cases for our business
* Not having access to skilled AI professionals
* Lack of understanding of AI technologies and their potential
* Struggling with integrating AI into existing processes
* Difficulty in managing AI projects and timelines
* Wasting resources on AI projects that don’t deliver ROI
* Not getting enough internal support for AI initiatives
* Struggling with data quality and quantity for AI models
* Difficulty in scaling AI solutions
* Not effectively responding to RFPs/RFQs for AI projects
* Overcoming concerns about AI costs and ROI""")
    skill_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    staff: Optional[str] = Field(description="""* Hiring AI experts who don’t fit into the team
* Difficulty in upskilling current employees to work with AI
* High turnover rates among AI specialists
* Not having a clear career path for AI professionals
* Managing the collaboration between AI and non-AI staff
* Difficulty in finding AI project managers
* AI experts being overworked and under-resourced
* Accepting subpar performance from AI staff due to high demand
* Lack of effective leadership in AI projects
* Potential issues if key AI personnel leave the company""")
    staff_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    structuring: Optional[str] = Field(description="""* Lack of a clear AI strategy
* Unclear accountability for AI projects
* Ineffective AI project management structure
* Lack of systems and processes for managing AI initiatives
* AI managers not having systems for pre-implementation strategy and post-implementation review
* No regular training or role-playing for AI-related scenarios""")
    structuring_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    strategies: Optional[str] = Field(description="""* Not having a clear AI adoption roadmap
* Ineffective strategies for integrating AI into business operations
* Difficulty in differentiating our AI solutions from competitors
* AI projects not leading to desired business growth
* Client retention issues due to lack of AI-driven innovation
* Employees uncomfortable with leveraging AI for upselling and cross-selling
* Not defining the balance between new AI initiatives and maintaining current operations
* Lack of clarity on proactive vs. reactive AI adoption mindsets
* Struggling to demonstrate the value of AI to avoid seeing it as a commodity""")
    strategies_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    additional_comments: Optional[str] = Field(description="Any additional comments")

    # CEO Survey
    strategic_leadership: Optional[str] = Field(description="""* Identifying high-impact AI use cases for business growth
* Securing top AI talent to drive initiatives
* Ensuring executive buy-in and support for AI projects
* Integrating AI seamlessly into strategic business operations
* Managing AI project timelines and deliverables effectively
* Maximizing ROI from AI investments
* Aligning AI initiatives with overall business strategy
* Overcoming internal resistance to AI adoption
* Ensuring data readiness and quality for AI applications
* Responding effectively to competitive AI-driven RFPs/RFQs""")
    strategic_leadership_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    talent_management: Optional[str] = Field(description="""* Recruiting AI experts who deliver results
* Upskilling the current workforce for AI readiness
* Retaining high-performing AI specialists
* Defining clear career paths and growth opportunities in AI
* Bridging collaboration between AI teams and other departments
* Finding and empowering AI project leaders
* Managing workload and resources for AI teams
* Maintaining high performance standards in AI roles
* Developing effective leadership for AI-driven projects
* Mitigating risks if key AI personnel leave""")
    talent_management_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    operational_excellence: Optional[str] = Field(description="""* Establishing a clear and actionable AI strategy
* Defining accountability and ownership for AI initiatives
* Implementing an efficient AI project management structure
* Developing robust systems and processes for AI management
* Conducting strategic planning and reviews for AI projects
* Providing regular training and scenario planning for AI-related challenges""")
    operational_excellence_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    competitive_advantage: Optional[str] = Field(description="""* Developing a clear AI adoption roadmap aligned with business goals
* Executing strategies for effective AI integration
* Differentiating AI solutions from competitors
* Achieving business growth through AI innovations
* Enhancing client retention with AI-driven services
* Leveraging AI for effective upselling and cross-selling
* Balancing new AI initiatives with ongoing business operations
* Cultivating a proactive AI adoption mindset
* Demonstrating the unique value of AI to avoid commoditization""")
    competitive_advantage_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    # CIO or CTO Survey
    technical_strategy: Optional[str] = Field(description="""* Identifying precise AI use cases for technical optimization
* Ensuring high-quality data availability for AI projects
* Establishing clear protocols for AI integration into IT infrastructure
* Managing detailed project plans and timelines for AI initiatives
* Ensuring robust ROI calculations and projections for AI investments
* Aligning AI technologies with existing IT and business systems
* Overcoming technical challenges and barriers to AI adoption
* Implementing effective data governance for AI
* Responding accurately to technical RFPs/RFQs involving AI
* Maintaining rigorous testing and validation for AI solutions""")
    technical_strategy_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    talent_resource_and_management: Optional[str] = Field(description="""* Recruiting technically proficient AI professionals
* Providing detailed upskilling programs for existing staff
* Retaining highly skilled AI talent through structured career development
* Creating clear roles and responsibilities for AI team members
* Facilitating precise collaboration between AI and other technical teams
* Identifying and empowering project managers with technical expertise
* Allocating resources efficiently for AI projects
* Upholding high technical standards and performance within the AI team
* Developing thorough leadership within AI-driven projects
* Managing contingencies for the potential departure of key AI personnel""")
    talent_resource_and_management_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    process_and_system_efficiency: Optional[str] = Field(description="""* Defining a comprehensive AI strategy with detailed action plans
* Establishing clear accountability and ownership for AI projects
* Implementing a structured AI project management framework
* Developing systematic processes for AI deployment and maintenance
* Conducting thorough pre-implementation and post-implementation reviews
* Ensuring regular and detailed training for AI-related scenarios""")
    process_and_system_efficiency_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    innovation_and_differentiation: Optional[str] = Field(description="""* Creating a precise AI adoption roadmap aligned with IT objectives
* Executing detailed strategies for seamless AI integration
* Differentiating our AI solutions through technical excellence
* Achieving business growth through innovative AI applications
* Enhancing client retention with technically advanced AI solutions
* Utilizing AI for detailed upselling and cross-selling opportunities
* Balancing new AI initiatives with existing IT operations
* Cultivating a methodical approach to AI adoption
* Demonstrating the technical value of AI to prevent commoditization""")
    innovation_and_differentiation_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    # Founder Survey
    strategic_clarity_and_alignment: Optional[str] = Field(description="""* Identifying AI use cases that align with our core principles and vision
* Ensuring that our AI initiatives support sustainable, long-term growth
* Gaining consensus among stakeholders on AI strategy
* Integrating AI solutions without disrupting our established processes
* Managing timelines and milestones effectively to ensure timely AI deployment
* Achieving a balanced ROI from our AI investments
* Aligning AI projects with our broader business goals and values
* Overcoming resistance and fostering a supportive culture for AI
* Ensuring our data is reliable and comprehensive for AI applications
* Responding effectively to AI-related RFPs/RFQs to maintain competitive edge""")
    strategic_clarity_and_alignment_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    building_and_nurturing_talent: Optional[str] = Field(description="""* Recruiting AI experts who fit our company culture and values
* Investing in upskilling our team to be proficient with AI technologies
* Retaining top AI talent by creating a supportive and growth-oriented environment
* Defining clear career paths and growth opportunities for AI professionals
* Facilitating effective collaboration between AI teams and other departments
* Identifying and empowering leaders within our AI initiatives
* Allocating resources wisely to support our AI projects
* Maintaining high performance standards without sacrificing our core values
* Developing strong leadership within AI-driven projects
* Managing the risk if key AI personnel leave, ensuring continuity""")
    building_and_nurturing_talent_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    process_optimization_and_efficiency: Optional[str] = Field(description="""* Establishing a clear, principled AI strategy
* Defining accountability and ownership for AI initiatives
* Implementing a structured and disciplined AI project management framework
* Developing robust processes for AI deployment, ensuring efficiency and consistency
* Conducting thorough reviews and learning from each AI project
* Ensuring regular and comprehensive training for AI-related scenarios""")
    process_optimization_and_efficiency_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    competitive_differentiation_and_growth: Optional[str] = Field(description="""* Creating a detailed AI adoption roadmap that aligns with our long-term vision
* Executing strategies that ensure seamless integration of AI
* Differentiating our AI solutions by adhering to our principles and values
* Leveraging AI to drive significant, sustainable business growth
* Enhancing client retention through innovative, AI-driven solutions
* Utilizing AI to create additional value through upselling and cross-selling
* Balancing new AI initiatives with maintaining our core business operations
* Fostering a proactive mindset towards AI adoption
* Demonstrating the unique value of our AI solutions to prevent commoditization""")
    competitive_differentiation_and_growth_rating: Optional[int] = Field(description="Rating of the problem on a scale of 1 to 5 where 1 is the least and 5 is the most")

    additional_comments: Optional[str] = Field(description="Any additional comments")

print(MergedSurvey.schema_json())
