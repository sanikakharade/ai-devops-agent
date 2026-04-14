import subprocess
from langchain.tools import tool

def run_aws(cmd):
    """Run AWS CLI and filter CloudShell gRPC noise"""
    result = subprocess.run(cmd, capture_output=True, text=True)

    def clean(text):
        if not text:
            return ""
        return "\n".join([
            line for line in text.splitlines()
            if "ev_epoll1_linux" not in line
            and "epoll_wait" not in line
            and "Bad file descriptor" not in line
            and "event_engine" not in line
            and "Epoll1Poller" not in line
        ]).strip()

    return clean(result.stdout) or clean(result.stderr) or "No results found"

@tool
def get_s3_buckets(placeholder: str = "list") -> str:
    """List all S3 buckets in the AWS account"""
    return run_aws(["aws", "s3", "ls"])

@tool
def get_ec2_instances(placeholder: str = "list") -> str:
    """List all EC2 instances with their state and type"""
    return run_aws([
        "aws", "ec2", "describe-instances",
        "--query", "Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType}",
        "--output", "table"
    ])

@tool
def get_vpcs(placeholder: str = "list") -> str:
    """List all VPCs in the AWS account"""
    return run_aws([
        "aws", "ec2", "describe-vpcs",
        "--query", "Vpcs[].{ID:VpcId,CIDR:CidrBlock,Default:IsDefault}",
        "--output", "table"
    ])

@tool
def get_iam_users(placeholder: str = "list") -> str:
    """List all IAM users in the AWS account"""
    return run_aws([
        "aws", "iam", "list-users",
        "--query", "Users[].{User:UserName,Created:CreateDate}",
        "--output", "table"
    ])

@tool
def get_security_groups(placeholder: str = "list") -> str:
    """List all security groups in the AWS account"""
    return run_aws([
        "aws", "ec2", "describe-security-groups",
        "--query", "SecurityGroups[].{ID:GroupId,Name:GroupName,VPC:VpcId}",
        "--output", "table"
    ])

@tool
def get_cloudwatch_alarms(placeholder: str = "list") -> str:
    """List all CloudWatch alarms and their states"""
    return run_aws([
        "aws", "cloudwatch", "describe-alarms",
        "--query", "MetricAlarms[].{Name:AlarmName,State:StateValue,Metric:MetricName}",
        "--output", "table"
    ])
