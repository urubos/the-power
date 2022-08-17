. .gh-api-examples.conf

# https://docs.github.com/en/rest/reference/repos#create-a-repository-webhook
# POST /repos/:owner/:repo/hooks

if [ -z "$1" ]
  then
    org=$org
  else
    org=$1
fi

json_file=tmp/webhook.json
rm -f ${json_file}

jq -n \
        --arg name "web" \
        --arg webhook_url "${webhook_url}" \
        --arg ct "json" \
        '{
           name: $name,
           active: true,
           events: [
             "organization"
           ],
           config: {
             url: $webhook_url,
             content_type: $ct,
             insecure_ssl: "0"
           }
         }' > ${json_file}


curl ${curl_custom_flags} \
     -H "Authorization: token ${GITHUB_TOKEN}" \
     -H "Accept: application/vnd.github.v3+json" \
     -H "Content-Type: application/json" \
     ${GITHUB_API_BASE_URL}/orgs/${org}/hooks --data @${json_file}
