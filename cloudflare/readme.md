##This uses the cloudflare library located here: 'https://github.com/cloudflare/python-cloudflare'

#Tips

##To get your API key
Navigate to the "Overview" page of your cloudflare account.

Under the "Domain Summary" heading, follow the link that says "Get your API key"

##To find your Zone ID, use this:
```curl -X GET "https://api.cloudflare.com/client/v4/zones?name=example.com&status=active&page=1&per_page=20&order=status&direction=desc&match=all" \
-H "X-Auth-Email: YOUR_EMAIL" \
-H "X-Auth-Key: API_KEY_HERE" \
-H "Content-Type: application/json"```

##To find your dns record ID in python, run this in the interpreter:
    import CloudFlare
    cf = CloudFlare.CloudFlare(email=auth_email, token=api_key)
    cf.zones.dns_records.get(zone_id)


This returns individual dictionaries for each record entry; the dns record ID is under the 'id' key.
