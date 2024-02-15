#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import sys
import string
import argparse
import logging
import logging.config
from pathlib import Path
import subprocess
from datetime import datetime
import re
import thepower


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def main(args):

    t = string.Template(
        """# Configuration file for The Power generated by configure.py

#These two are used for debugging and should remain commented in most cases
# set -a
# shopt -s -o nounset


### [GitHub Enterprise Server](ttps://docs.github.com/en/enterprise-server/rest/guides/getting-started-with-the-rest-api)
# these are setting for GitHub's on premises server 
number_of_users_to_create_on_ghes=${number_of_users_to_create_on_ghes}
U=ghe-admin
admin_user=${admin_user}
admin_password="${admin_password}"
mgmt_port=${mgmt_port}
mgmt_password="${mgmt_password}"
# GHES LDAP Settings
ldap_dn="cn=Enterprise Ops,ou=teams,dc=github,dc=com"


### [Authorization](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
token=${token}
GITHUB_TOKEN=${token}
auth_header="Authorization: token ${token}"
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token


hostname=${hostname}
path_prefix=${path_prefix}
graphql_path_prefix=${graphql_path_prefix}
GITHUB_API_BASE_URL=${http_protocol}://${hostname}${path_prefix}
GITHUB_APIV4_BASE_URL=${http_protocol}://${hostname}${graphql_path_prefix}
mail_domain="example.com"


### GitHub Enterprise
enterprise="${enterprise_name}"


### GitHub API Version
# https://docs.github.com/en/rest/overview/api-versions
github_api_version=${github_api_version}

### [Organization](https://docs.github.com/en/rest/orgs)
# https://docs.github.com/en/organizations
org="${org}"
owner="${org}"
org_secret_name="ORGANIZATION_SECRET_001"
org_owner="${org_owner}"
org_members="${org_members}"
default_org_webhook_id=1
# Org self hosted runners
org_self_hosted_runner_group_name="org self hosted runners"



### [Repository](https://docs.github.com/en/rest/repos/repos#create-an-organization-repository)
# https://docs.github.com/en/repositories
repo="${repo_name}"
default_repo_visibility="private"
allow_auto_merge="${allow_auto_merge}"
repo_secret_name="REPOSITORY_SECRET_001"
repo_secret_value="repository_secret_string"
# webhook url is also used by the organization
webhook_url=${webhook_url}
has_issues=true
has_wiki=true
has_projects=true
has_discussions=true
has_pages=false
#### [Repository ruleset](https://docs.github.com/en/free-pro-team@latest/rest/repos/rules?apiVersion=2022-11-28#create-a-repository-ruleset)
ruleset_name="the-power-repo-ruleset1"
target="branch"
commit_message_pattern="MAGIC-MIKE"
operator="starts_with" 
enforcement="evaluate"
bypass_mode="always"


### [Team](https://docs.github.com/en/rest/teams)
# https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams
team="${team_name}"
team_slug="${team_slug}"
team_id=
team_members="${team_members}"
team_admin="${team_admin}"
team_privacy="closed"
team_permission="admin"


### [Issues](https://docs.github.com/en/rest/issues/issues)
# https://docs.github.com/en/issues
# https://docs.github.com/en/get-started/writing-on-github
default_issue_id=1


### [Pull requests](https://docs.github.com/en/rest/pulls)
# https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
# https://docs.github.com/en/get-started/writing-on-github
default_pull_request_id=2
# When using xxx
files_changed=15

# A Pull request may not be approved by it's author.
# create a PAT for the pull request approver
# place it below to allow the default pull request
# to be approved vi automation.
pr_approver_token=${pr_approver_token}
pr_approver_name=${pr_approver_name}
default_pr_event="COMMENT"


### [Branches](https://docs.github.com/en/rest/commits/commits)
# https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches
branch_name="new_branch"
protected_branch_name="${base_branch}"
required_approving_reviewers=1
required_status_check_name="ci-test/this-check-is-required"
enforce_admins="false"
base_branch=${base_branch}
delete_branch_on_merge=${delete_branch_on_merge}


### [Commits](https://docs.github.com/en/rest/commits/commits)
default_committer="${default_committer}"


### [Checks](https://docs.github.com/en/rest/guides/getting-started-with-the-checks-api)
# https://docs.github.com/en/developers/apps/guides/creating-ci-tests-with-the-checks-api
default_check_run_id=1


### [Pagination](https://docs.github.com/en/rest/guides/traversing-with-pagination)
per_page=30


### [Pre-receive hook (GitHub Enteprise Server only)](https://docs.github.com/en/enterprise-server/rest/enterprise-admin/pre-receive-hooks)
pre_receive_hook_name=demo-pre-receive-hook
pre_receive_hook_repo=hook-repo
pre_receive_environment_id=1
pre_receive_hook_script=pre-receive-hook.sh
pre_hook_environment=default
pre_hook_enforcement=enabled
pre_hook_allow_downstream=true


### [SSH Key](https://docs.github.com/en/rest/users/keys)
# https://docs.github.com/en/authentication/connecting-to-github-with-ssh
# https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification
my_ssh_pub_key=~/.ssh/id_rsa.pub


### [GPG Key](https://docs.github.com/en/rest/users/gpg-keys)
# https://docs.github.com/en/authentication/managing-commit-signature-verification/checking-for-existing-gpg-keys
# https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification 
my_gpg_pub_key=~/.gnupg/public.key
# To export your pub key:
# gpg --export -a "key_name" > public.key


### [Deployment environments](https://docs.github.com/en/rest/deployments/environments)
default_environment_name="environment_1"
environment_secret_name="ENVIRONMENT_SECRET_001"


### [Packages](https://docs.github.com/en/rest/packages)
# https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages
default_package_type="container"


### [Deployments](https://docs.github.com/en/rest/deployments/deployments)
# https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-deployment-activity-for-your-repository
default_deployment_id=1


### [GitHub Apps](https://docs.github.com/en/rest/apps)
# https://docs.github.com/en/developers/apps/getting-started-with-apps/about-apps
# Set private_pem_file name to the private key you've generated and downloaded..
#
# If you set a relative path, it is regarded as a relative path from your home directory.
#
# Relative path example (no leading slash):
#   private_pem_file=Downloads/testapp.YYYY-MM-DD.private-key.pem
#   #=> The absolute path of the pem file is /home/username/Downloads/testapp.YYYY-MM-DD.private-key.pem

# Absolute path example (leading slash):
#   private_pem_file=/opt/the-power/testapp.YYYY-MM-DD.private-key.pem
#   #=> The absolute path of the pem file is /opt/the-power/Downloads/testapp.YYYY-MM-DD.private-key.pem
#
private_pem_file=${private_key_pem_file}
# When working with the power in a codespace you may need a path like:
#private_pem_file=../../workspaces/the-power/ft-testapp.2022-03-23.private-key.pem
# The App ID: value at https://github.com/organizations/<org>/settings/apps/<appname>
default_app_id=${default_app_id}
# https://github.com/organizations/<org>/settings/installations/<installation_id>
default_installation_id=${default_installation_id}
# The Client ID is used when using the device authentication flow
client_id=${client_id}
app_client_secret=${app_client_secret}


### [Oauth Apps API](https://docs.github.com/en/rest/apps/oauth-applications)
# https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app
# https://docs.github.com/en/developers/apps/getting-started-with-apps/migrating-oauth-apps-to-github-apps
x_client_id="$x_client_id"
x_client_secret="$x_client_secret"
fingerprint="fingerprint1"
authorization_id=1
oauth_token_scope="read:enterprise read:org"
# A browser can be started for the oauth device flow scripts
# default is chrome.
preferred_browser=${preferred_browser}
# default is "incognito". "normal" is allowed.
browser_mode=${preferred_browser_mode}
# This gist is helpful for chrome profile
# https://gist.github.com/gm3dmo/98247152b375b84ac7a9d4cbb7f92e3b
chrome_profile="${chrome_profile}"


### [GitHub Actions](https://docs.github.com/en/rest/actions)
enterprise_shr_group_name="my-enterprise-self-hosted-runners"


### [Codespaces](https://docs.github.com/en/rest/codespaces/codespaces?apiVersion=2022-11-28)
### [Managing secrets for your codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-secrets-for-your-codespaces)
codespaces_secret_001="the-power-codespaces-secret"


### [Self hosted runner setup](https://docs.github.com/en/rest/actions/self-hosted-runner-groups)
# https://docs.github.com/en/rest/actions/self-hosted-runners
runner_version=${runner_version}
runner_os=${runner_os}
runner_platform=${runner_platform}
runner_name="the-power-example-runner"
runner_labels="the-power,self-hosted"


### [gh cli](https://cli.github.com/manual/gh_api)
preferred_client="${preferred_client}"
gh_custom_flags="--paginate --hostname ${hostname}"
gh_custom_headers=""


### [Curl](https://curl.se/)
# latest version of curl is recommended.
# `curl has --write-out json` for timing testing etc.
# using https://daniel.haxx.se/blog/2020/03/17/curl-write-out-json/
# example:
# curl_custom_flags="-kso /dev/null --write-out '%{json}'"
#
# use a custom value for user-agent make things traceable
curl_custom_flags="${curl_custom_flags}"


## Default values for scripts that generate many of a resource.
# mostly used for testing things on GHES.
number_of_orgs=${number_of_orgs}
number_of_repos=${number_of_repos}
number_of_teams=${number_of_teams}
number_of_branches=${number_of_branches}
repo_prefix="testrepo"
org_prefix="testorg"
user_prefix="testuser"
team_prefix="testteam"
branch_prefix="testbranch"
file_prefix="testfile"
file_extension="c"
# Dispatcher
pool_size=10



"""
    )

    ghe_config = thepower.read_ghe_boot_file()

    args.path_prefix = "/api/v3"
    args.graphql_path_prefix = "/api/graphql"
    args.org_owner = "mona"
    args.org_members = "mona"
    token_validation ="strict"

    # use "\" for these so that they get written to the conf
    # file including quotes:

    if args.dotcom_config != "":
        dotcom_config = thepower.read_dotcom_config(args.dotcom_config)
        logger.info(f"""config: {dotcom_config}""")
        ghe_config["hostname"] = dotcom_config.get("dummy_section", "hostname")
        ghe_config["token"] = dotcom_config.get("dummy_section", "token")
        args.org = dotcom_config.get("dummy_section", "org")
        args.default_app_id = dotcom_config.get("dummy_section", "default_app_id")
        args.default_installation_id = dotcom_config.get(
            "dummy_section", "default_installation_id"
        )
        args.client_id = dotcom_config.get("dummy_section", "client_id")
        args.app_client_secret = dotcom_config.get("dummy_section", "app_client_secret")
        args.team_members = dotcom_config.get("dummy_section", "team_members")
        args.team_admin = dotcom_config.get("dummy_section", "team_admin")
        args.org_owner = dotcom_config.get("dummy_section", "org_owner")
        args.org_members = dotcom_config.get("dummy_section", "org_members")
        args.default_committer = dotcom_config.get("dummy_section", "default_committer")
        args.private_pem_file = dotcom_config.get("dummy_section", "private_pem_file")

    if args.hostname != "":
        logger.info(f"GitHub hostname = {args.hostname}")
    elif "hostname" in ghe_config:
        args.hostname = ghe_config["hostname"]
    else:
        args.hostname = input(f"Enter GitHub hostname: ")

    #print(ghe_config)

    if args.admin_password != "":
        logger.info(f"Password is set")
    elif "admin_password" in ghe_config:
        args.admin_password = ghe_config["admin_password"]

    if args.mgmt_password != "":
        logger.info(f"MGMT password is set")
    elif "mgmt_password" in ghe_config:
        args.mgmt_password = ghe_config["mgmt_password"]



    if args.hostname == "api.github.local":
        args.http_protocol = "http"

    if args.hostname == "api.github.com" or args.hostname == "api.github.local":
        args.path_prefix = ""
        args.graphql_path_prefix = "/graphql"
    else:
        # Set the path up for a GHES server
        default_app_id = 1
        default_installation_id = 1
        client_id = 1


    if args.token != "":
        logger.info(f"Token = args.token") 
    elif "token" in ghe_config and ghe_config["token"] not in [None, ""]:
        args.token = ghe_config["token"]
    else:
        args.token = input(f"Enter Personal Access Token: ")


    assert thepower.token_validator(args.token), "Invalid format: token should have a valid prefix, or should be 40 characters string."

    if args.team_name != "":
        args.team_slug = thepower.slugify(args.team_name)

    if args.org != "":
        logger.info(f"Org = {args.org}")
    else:
        args.org = input(f"Enter Org name: ")

    # If configuring a GitHub App:
    if args.configure_github_app != "no":
        if args.app_id != "":
            logger.info(f"default_app_id = {args.app_id}")
        else:
            args.app_id = input(f"Enter App Id ({args.app_id}): ") or args.app_id

        if args.installation_id != "":
            logger.info(f"default_installation_id = {args.installation_id}")
        else:
            args.installation_id = (
                input(f"Enter Installation Id ({args.installation_id}): ")
                or args.installation_id
            )

        if args.client_id != "":
            logger.info(f"client_id = {args.client_id}")
        else:
            args.client_id = input(f"Enter Client Id: ")

        # Private key
        if args.private_pem_file != "":
            logger.info(f"private_key_pem_file = {args.private_pem_file}")
        else:
            args.private_key_pem_file = input(
                f"Enter path relative from home to app private key: "
            )

    if args.webhook_url == "smee":
        webhook_url = thepower.get_webhook_url()
        if webhook_url is None:
            webhook_url = input(f"Enter webhook URL: ")

        args.webhook_url = webhook_url
        if re.match(r"^https?://", args.webhook_url):
            thepower.open_webhook_url_in_browser(args.webhook_url)
        else:
            logger.info(
                "No webhook URL supplied. You can still set a webhook URL in .gh-api-examples.conf file."
            )
    elif args.webhook_url:
        logger.info(f"Webhook URL = {args.webhook_url}")
    else:
        args.webhook_url = input(f"Enter webhook url: ")

    values = {
        "token": args.token,
        "hostname": args.hostname,
        "path_prefix": args.path_prefix,
        "graphql_path_prefix": args.graphql_path_prefix,
        "webhook_url": args.webhook_url,
        "private_pem_file": args.private_pem_file,
        "org": args.org,
        "enterprise_name": args.enterprise_name,
        "base_branch": args.base_branch,
        "delete_branch_on_merge": args.delete_branch_on_merge,
        "pr_approver_token": args.pr_approver_token,
        "pr_approver_name": args.pr_approver_name,
        "default_app_id": args.app_id,
        "default_installation_id": args.installation_id,
        "private_key_pem_file": args.private_pem_file,
        "client_id": args.client_id,
        "app_client_secret": args.app_client_secret,
        "admin_user": args.admin_user,
        "admin_password": args.admin_password,
        "mgmt_password": args.mgmt_password,
        "mgmt_port": args.mgmt_port,
        "team_name": args.team_name,
        "team_slug": args.team_slug,
        "team_members": args.team_members,
        "team_admin": args.team_admin,
        "org_owner": args.org_owner,
        "org_members": args.org_members,
        "default_committer": args.default_committer,
        "repo_name": args.repo_name,
        "number_of_users_to_create_on_ghes": args.number_of_users_to_create_on_ghes,
        "runner_version": args.runner_version,
        "runner_os": args.runner_os,
        "runner_platform": args.runner_platform,
        "number_of_orgs": args.number_of_orgs,
        "number_of_repos": args.number_of_repos,
        "number_of_teams": args.number_of_teams,
        "number_of_branches": args.number_of_branches,
        "curl_custom_flags": args.curl_custom_flags,
        "allow_auto_merge": args.allow_auto_merge,
        "preferred_client": args.preferred_client,
        "preferred_browser": args.preferred_browser,
        "preferred_browser_mode": args.preferred_browser_mode,
        "chrome_profile": args.chrome_profile,
        "github_api_version": args.github_api_version,
        "http_protocol": args.http_protocol,
        "x_client_id": args.x_client_id,
        "x_client_secret": args.x_client_secret,
    }

    out_filename = ".gh-api-examples.conf"

    try:
        with open(out_filename, "w") as out_file:
            out_file.write(t.substitute(values))
            logger.info(
                f"\n{bcolors.OKGREEN}Configuration run is complete. Created {out_filename}"
            )
    except Exception as e:
        logger.warn(f"\n{bcolors.WARNING}Configuration run failed. {e}")

    cmd = f"""./{args.primer}"""
    logger.info(f"\n{bcolors.OKGREEN}Launching primer command: {args.primer}")
    # Now run the primer script to execute whatever task is wanted for this particular thing
    # can be useful when creating a container that executes some repetive task.
    subprocess.run(cmd, shell=True, check=True)
    logger.info(
        f"\n{bcolors.OKBLUE}========================================================="
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--org", action="store", dest="org", default="acme")
    parser.add_argument(
        "-b", "--base_branch", action="store", dest="base_branch", default="main"
    )
    parser.add_argument(
        "-d",
        "--configure-app",
        action="store",
        dest="configure_github_app",
        default="no",
    )
    parser.add_argument("-a", "--app-id", action="store", dest="app_id", default=1)
    parser.add_argument(
        "-i", "--installation-id", action="store", dest="installation_id", default=1
    )
    parser.add_argument(
        "-e", "--client-id", action="store", dest="client_id", default=""
    )
    parser.add_argument(
        "--app-client-secret", action="store", dest="app_client_secret", default=""
    )
    parser.add_argument(
        "-u", "--admin-user", action="store", dest="admin_user", default="ghe-admin"
    )
    parser.add_argument(
        "--admin-password", action="store", dest="admin_password", default=""
    )
    parser.add_argument(
        "--mgmt-password", action="store", dest="mgmt_password", default=""
    )
    parser.add_argument(
        "--mgmt-port", action="store", dest="mgmt_port", default=8443
    )
    parser.add_argument(
        "-w",
        "--webhook-url",
        action="store",
        dest="webhook_url",
        default="smee",
        help="Set this if you want to provide your own webhook url.",
    )
    parser.add_argument(
        "--x-client-id",
        action="store",
        dest="x_client_id",
        default="a legacy oauth client id",
        help="Use with legacy oauth apps.",
    )
    parser.add_argument(
        "--x-client-secret",
        action="store",
        dest="x_client_secret",
        default="a legacy oauth client secret",
        help="Use with legacy oauth apps",
    )
    parser.add_argument(
        "--number-of-users",
        action="store",
        dest="number_of_users_to_create_on_ghes",
        default=4,
        help="Number of users to create on GHES systems.",
    )
    parser.add_argument(
        "--runner-version",
        action="store",
        dest="runner_version",
        default="v2.312.0",
        help="Version of self hosted runner. Be sure to use the tag like this: `v2.294.0`",
    )
    parser.add_argument(
        "--runner-os",
        action="store",
        dest="runner_os",
        default="osx",
        help="OS for self hosted runner.",
    )
    parser.add_argument(
        "--runner-platform",
        action="store",
        dest="runner_platform",
        default="x64",
        help="CPU platform for self hosted runner",
    )
    parser.add_argument(
        "-c",
        "--copy-config",
        action="store",
        dest="dotcom_config",
        default="",
        help="Set this for github.com config",
    )
    parser.add_argument(
        "-r",
        "--repo-name",
        action="store",
        dest="repo_name",
        default="testrepo",
        help="Provide a repository name.",
    )
    parser.add_argument(
        "-n",
        "--hostname",
        action="store",
        dest="hostname",
        default="",
        help="Provide a fully qualified hostname/IP Address for a GHES appliance or use the default api.github.com",
    )
    parser.add_argument(
        "-t",
        "--token",
        action="store",
        dest="token",
        default="",
        help="Provide a personal access token.",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        action="store",
        dest="loglevel",
        default="info",
        help="Set the log level",
    )
    parser.add_argument(
        "-p",
        "--primer",
        action="store",
        dest="primer",
        default="list-user.sh",
        help="The name of a primer script which will be executed when configuration is complete",
    )
    parser.add_argument(
        "--team-name",
        action="store",
        dest="team_name",
        default="Justice League",
        help="The name of a team to create.",
    )
    parser.add_argument(
        "--private-pem-file",
        action="store",
        dest="private_pem_file",
        default="",
        help="The location of the apps private key (pem) file.",
    )
    parser.add_argument(
        "--number-of-orgs",
        action="store",
        dest="number_of_orgs",
        default=3,
        help="The number of orgs for the bulk creators to create.",
    )
    parser.add_argument(
        "--number-of-repos",
        action="store",
        dest="number_of_repos",
        default=3,
        help="The number of repos for the bulk creators to create.",
    )
    parser.add_argument(
        "--number-of-teams",
        action="store",
        dest="number_of_teams",
        default=3,
        help="The number of teams for the bulk creators to create.",
    )
    parser.add_argument(
        "--number-of-branches",
        action="store",
        dest="number_of_branches",
        default=10,
        help="The number of branches for the bulk creators to create.",
    )
    parser.add_argument(
        "--team-members",
        action="store",
        dest="team_members",
        default="mona hubot mario luigi",
        help="The members of your team.",
    )
    parser.add_argument(
        "--team-admin",
        action="store",
        dest="team_admin",
        default="mona",
        help="The admin of your team.",
    )
    parser.add_argument(
        "--default-committer",
        action="store",
        dest="default_committer",
        default="hubot",
        help="The user who will make default actions such as create commits, be assigned issues.",
    )
    parser.add_argument(
        "--allow-auto-merge",
        action="store",
        dest="allow_auto_merge",
        default="true",
        help="allow auto merge"
    )
    parser.add_argument(
        "--delete-branch-on-merge",
        action="store",
        dest="delete_branch_on_merge",
        default="true",
        help="delete branch on merge"
    )
    parser.add_argument(
        "--enterprise-name",
        action="store",
        dest="enterprise_name",
        default="",
        help="The name of your enterprise.",
    )
    parser.add_argument(
        "--pr-approver-token",
        action="store",
        dest="pr_approver_token",
        default="replace_with_a_PAT",
        help="The PAT of a pr approver.",
    )
    parser.add_argument(
        "--pr-approver-name",
        action="store",
        dest="pr_approver_name",
        default="abc",
        help="The name of a user.",
    )
    parser.add_argument(
        "--preferred_client",
        action="store",
        dest="preferred_client",
        default="curl",
        help="The preferred client program to use for interaction with the API's. Valid values are gh or curl.",
    )
    parser.add_argument(
        "--custom-curl-flags",
        action="store",
        dest="curl_custom_flags",
        default="--no-progress-meter",
        help="curl custom flags.",
    )
    parser.add_argument(
        "--preferred_browser",
        action="store",
        dest="preferred_browser",
        default="chrome",
        help="chrome, firefox, edge are allowed values.",
    )
    parser.add_argument(
        "--preferred_browser_mode",
        action="store",
        dest="preferred_browser_mode",
        default="incognito",
        help="incognito, normal are allowed values.",
    )
    parser.add_argument(
        "--chrome-profile",
        action="store",
        dest="chrome_profile",
        default="Profile 1",
        help="The Chrome profile to start in.",
    )
    parser.add_argument(
        "--github-api-version",
        action="store",
        dest="github_api_version",
        default="2022-11-28",
        help="see GitHub API version docs",
    )
    parser.add_argument(
        "--http-protocol",
        action="store",
        dest="http_protocol",
        default="https",
        help="Mostly always https",
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.getLogger().handlers.clear()
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(args.loglevel.upper())
    logger = logging.getLogger(__name__)
    logger.addHandler(console_handler)

    main(args)
