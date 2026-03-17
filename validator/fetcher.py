import requests

def fetch(url, timeout=10):
    result = {
        "url": url,
        "success": False,
        "data": None,
        "error": None,
        "status_code": None
    }

    try:
        response = requests.get(url, timeout=timeout)
        result["status_code"] = response.status_code

        if response.status_code != 200:
            result["error"] = f"HTTP {response.status_code}"
            return result

        result["data"] = response.json()
        result["success"] = True

    except requests.exceptions.Timeout:
        result["error"] = "Request timed out"

    except requests.exceptions.ConnectionError:
        result["error"] = "Connection failed"

    except requests.exceptions.JSONDecodeError:
        result["error"] = "Response is not valid JSON"

    except requests.exceptions.RequestException as e:
        result["error"] = str(e)

    return result
