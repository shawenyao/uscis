import cloudscraper

def query_uscis(receipt_number):
    session = cloudscraper.CloudScraper()

    # 1st request: get cookies
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en',
        'Cache-Control': 'max-age=0',
        'Dnt': '1',
        'Priority': 'u=0, i',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }
    page_visit_response = session.get("https://egov.uscis.gov/", headers=headers)
    cookies = page_visit_response.cookies

    # 2nd request: get token
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en',
        'Content-Type': 'application/json',
        'Dnt': '1',
        'Priority': 'u=1, i',
        'Referer': 'https://egov.uscis.gov/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    ui_auth_response = session.get(f"https://egov.uscis.gov/csol-api/ui-auth/{receipt_number}", cookies=cookies, headers=headers)
    token_type = ui_auth_response.json()['JwtResponse']['tokenType']
    access_token = ui_auth_response.json()['JwtResponse']['accessToken']

    # 3rd request: get case status
    headers['Authorization'] = f'{token_type} {access_token}'
    query_response = session.get(f'https://egov.uscis.gov/csol-api/case-statuses/{receipt_number}', cookies=cookies, headers=headers)
    case = query_response.json()['CaseStatusResponse']
    status = case['detailsEng']['actionCodeText']

    session.close()

    return status
