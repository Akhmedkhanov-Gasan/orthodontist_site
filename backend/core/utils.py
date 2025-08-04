# core/utils.py
def verify_recaptcha(token, remote_ip=None):
    from django.conf import settings
    import requests, logging

    # if settings.DEBUG and not token:
    #     return True

    data = {
        "secret": settings.RECAPTCHA_SECRET,
        "response": token,
    }
    if remote_ip:
        data["remoteip"] = remote_ip

    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data, timeout=5)
    r.raise_for_status()
    result = r.json()
    logging.warning("reCAPTCHA response: %s", result)


    return result.get("success") and result.get("score", 0) >= 0.5 and result.get("action") == "appointment"
