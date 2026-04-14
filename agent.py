from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from tools import (
    get_s3_buckets,
    get_ec2_instances,
    get_vpcs,
    get_iam_users,
    get_security_groups,
    get_cloudwatch_alarms
)

load_dotenv()

tools = [
    get_s3_buckets,
    get_ec2_instances,
    get_vpcs,
    get_iam_users,
    get_security_groups,
    get_cloudwatch_alarms
]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=3,
    request_timeout=60
)

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=8,
    handle_parsing_errors=True
)

result = agent_executor.invoke({
    "input": """
    You are a senior DevOps assistant auditing an AWS account.
    Do the following steps one by one:
    1. List all S3 buckets
    2. List all EC2 instances and their states
    3. List all VPCs
    4. Check CloudWatch alarms and their states
    5. Give me a clean infrastructure summary with any issues or warnings you notice
    """
})

print("\n" + "="*50)
print("✅ INFRASTRUCTURE SUMMARY")
print("="*50)
print(result["output"])
