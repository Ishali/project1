## vertex-impact-common-stack

This stack containes common resources required by all modules such as omnichannel, cmo, acquia and so on...

### Prerequisite
 * Python 3.9 should be installed, as codebase has been written using Python3.9 or venv created using Python3.9
 * Check your pip using `pip -V`, it should point to Python3.9
 * Install npm, https://nextgentips.com/2021/12/26/how-to-install-node-js-17-on-ubuntu-20-04/

### Build

To build this app, you need to be at the root folder. Then run the following:

```bash
$ python3.9 -m venv .cdk_env
$ source .cdk_env/bin/activate
$ pip install -r requirements.txt
```
This will install the necessary CDK, and other test dependencies, and then build your Python files and your CloudFormation template.

Install the latest version of the AWS CDK CLI:

```shell
$ npm i -g aws-cdk
$ cdk --version
```


### Deploy

Set Env Var
```bash
export environment_name="sbx01/dev/test/prod"
```

Install Python Lambda Layer
```bash
mkdir -p ./lambda-layers/vertex-impact-${environment_name}-layer/python/lib/python3.9/site-packages/
pip install -r lambda-layer.txt --target ./lambda-layers/vertex-impact-${environment_name}-layer/python/lib/python3.9/site-packages/
```

Run the below command after setting up your aws-credentials in your terminal.

To list the resources -
```bash
cdk ls -c env=${environment_name} --all -v
``` 
cdk synth -c env=${environment_name} --all -v

Check which resource will cdk create, replace or destroy - 
```bash
cdk diff -c env=${environment_name} --all -v
``` 


To deploy the resources -
```bash
cdk deploy -c env=${environment_name} --all -v
``` 

##### References 
* https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/README.html#execution-role
* https://docs.aws.amazon.com/cdk/v2/guide/serverless_example.html
* https://cdkworkshop.com/30-python/30-hello-cdk/200-lambda.html
* https://github.com/aws-samples/aws-cdk-examples
* 
Test Commit