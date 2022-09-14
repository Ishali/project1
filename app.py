import json
import ssl
import os
from io import StringIO
from lambda_stack.lambda_stack import LambdaStack

import aws_cdk
from aws_cdk import (
    App 
)


def get_config(environment):

    with open(os.getcwd() + "/conf/aws-lambda-stack-conf.json") as f:
        config_file = f.read()
        config_file = config_file.replace("{environment}", environment)
        config_file = StringIO(config_file)
        config = json.load(config_file)
    if config:
        return config
    else:
        raise Exception("Unable to load Config")


# *** Code Execution starts from here
app = App()
env_name = app.node.try_get_context("env")

if env_name not in ['sbx01', 'dev', 'test', 'prod']:
    raise Exception("Invalid env name received. Run Command Usage -> cdk <command> -c env=sbx01/dev/test/prod --all")

conf = get_config(env_name)
env = aws_cdk.Environment(account=conf['aws_account'][env_name], region=conf['region'])

Lambda_Stack = LambdaStack(app, conf['stack_name'], config=conf, envname=env_name, env=env)

# Adding Tags
aws_cdk.Tags.of(Lambda_Stack).add("Environment", f"{env_name}")
aws_cdk.Tags.of(Lambda_Stack).add("Application", "vdp")
aws_cdk.Tags.of(Lambda_Stack).add("Owner", "lambda-Stack")
aws_cdk.Tags.of(Lambda_Stack).add("Module", "lambda-Stack")

app.synth()
