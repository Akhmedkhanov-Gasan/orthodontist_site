# core/utils.py
def verify_recaptcha(token, remote_ip=None):
    from django.conf import settings
    import requests, logging

    if not token:
        logging.warning("reCAPTCHA: empty token")
        return False

    data = {"secret": settings.RECAPTCHA_SECRET, "response": token}
    if remote_ip:
        data["remoteip"] = remote_ip

    try:
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data=data,
            timeout=5,
        )
        r.raise_for_status()
        result = r.json()
    except requests.RequestException as e:
        logging.exception("reCAPTCHA HTTP error: %s", e)
        return False
    except ValueError:
        logging.exception("reCAPTCHA invalid JSON")
        return False

    logging.warning("reCAPTCHA response: %s", result)
    return bool(result.get("success")) and result.get("action") == "appointment" and float(result.get("score", 0)) >= 0.5
