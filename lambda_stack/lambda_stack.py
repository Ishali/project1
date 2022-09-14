import os
import string
import json
from io import StringIO

import aws_cdk
from aws_cdk import (
    aws_lambda as lambda_,
    App, Duration, Stack,
    aws_ec2 as ec2,
    aws_s3 as aws_s3,
    aws_iam
)

class LambdaStack(Stack):

    def __init__(self, app: App, id: str, config: dict, envname: string, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        ## Creating a lambda function for the Generic Logger Lambda Function
        generic_layer = lambda_.LayerVersion(self, f"{config['lambda_fn']['stack_name']}-layer",
                                   layer_version_name=config['lambda_fn']['lambda_layers']['name'],
                                   code=lambda_.AssetCode(config['lambda_fn']['lambda_layers']['path']),
                                   compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
                                   compatible_architectures=[lambda_.Architecture.X86_64])
        # Lambda-Role
        generic_lambda_role = aws_iam.Role(self, f"{config['lambda_fn']['stack_name']}-lambda-role",
                                   assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                                   role_name=f"{config['lambda_fn']['function_name']}-lambda-role",
                                   managed_policies=[
                                       aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                                           "service-role/AWSLambdaBasicExecutionRole"),
                                       aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                                           "service-role/AWSLambdaVPCAccessExecutionRole")
                                   ]
                                   )

        policy_statements = []
        for policy_statement in config['lambda_fn']['lambda_permissions']:
            stmt = aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW, actions=policy_statement['actions'],
                resources=policy_statement['resources'])
            policy_statements.append(stmt)

        role_policy = aws_iam.ManagedPolicy(self, f"{config['lambda_fn']['stack_name']}-lambda-role-policy",
                                            managed_policy_name=f"{config['lambda_fn']['function_name']}-lambda-role-policy",
                                            statements=policy_statements,
                                            roles=[generic_lambda_role])

        logger_lambda_function = lambda_.Function(self,
                                           id=config['lambda_fn']['stack_name'],
                                           function_name=config['lambda_fn']['function_name'],
                                           description=config['lambda_fn']['description'],
                                           runtime=lambda_.Runtime.PYTHON_3_9,
                                           architecture=lambda_.Architecture.X86_64,
                                           vpc= ec2.Vpc.from_vpc_attributes(
                                                                self, 'VpcDefault',
                                                                vpc_id=config['lambda_fn']['vpc'][envname],
                                                                vpc_cidr_block=config['lambda_fn']['vpc_cidr_block'][envname],
                                                                availability_zones=config['lambda_fn']['availability_zones'][envname],
                                                                private_subnet_ids=config['lambda_fn']['vpc_subnets'][envname],
                                                                private_subnet_route_table_ids=config['lambda_fn']['private_subnet_route_table_ids'][envname]
                                                            ),
                                        #    vpc=ec2.Vpc.from_lookup(self, f"{config['lambda_fn']['stack_name']}-vpc",
                                        #                            vpc_id=config['lambda_fn']['vpc'][envname]),
                                           security_groups=[ec2.SecurityGroup.from_security_group_id(self,
                                                                                                     f"{config['lambda_fn']['stack_name']}-sg",
                                                                                                     config['lambda_fn'][
                                                                                                         'security_groups'][
                                                                                                         envname])],
                                           allow_public_subnet=True,
                                           role=generic_lambda_role,
                                           code=lambda_.Code.from_asset(
                                               os.getcwd() + "/" + config['lambda_fn']['handler_dir_path']),
                                           handler=config['lambda_fn']['handler_fn'],
                                           timeout=Duration.seconds(config['lambda_fn']['timeout_duration_sec']),
                                           retry_attempts=config['lambda_fn']['retries'],
                                           environment=config['lambda_fn']['environment_vars'],
                                           layers=[generic_layer],
                                           memory_size=config['lambda_fn']['memory_size']
                                           # on_failure="",
                                           # on_success=""
                                           )        