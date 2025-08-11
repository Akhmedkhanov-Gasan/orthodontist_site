# core/utils.py
def verify_recaptcha(token, remote_ip=None):
    from django.conf import settings
    import requests, logging

    if not token or not getattr(settings, "RECAPTCHA_SECRET", ""):
        logging.warning("reCAPTCHA: missing token or secret")
        return False

    data = {"secret": settings.RECAPTCHA_SECRET, "response": token}
    if remote_ip:
        data["remoteip"] = remote_ip

    try:
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data, timeout=5)
        r.raise_for_status()
        try:
            result = r.json()
        except Exception:
            logging.exception("reCAPTCHA: JSON parse failed, text=%r", r.text[:200])
            return False
    except requests.RequestException:
        logging.exception("reCAPTCHA: request failed")
        return False

    ok = bool(result.get("success")) and result.get("action") == "appointment" and float(result.get("score", 0)) >= 0.5
    logging.warning("reCAPTCHA response: %s", result)
    return ok
