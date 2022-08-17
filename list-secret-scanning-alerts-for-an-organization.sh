. .gh-api-examples.conf

# https://docs.github.com/en/enterprise-cloud@latest/rest/secret-scanning#list-secret-scanning-alerts-for-an-organization
# GET /orgs/{org}/secret-scanning/alerts

curl ${curl_custom_flags} \
     -H "Accept: application/vnd.github.v3+json" \
     -H "Authorization: token ${GITHUB_TOKEN}" \
     ${GITHUB_API_BASE_URL}/orgs/${org}/secret-scanning/alerts
