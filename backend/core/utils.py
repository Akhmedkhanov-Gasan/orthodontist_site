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
        payload = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    except requests.RequestException as e:
        logging.error("reCAPTCHA verify error: %s", e)
        return False
    except ValueError:
        logging.error("reCAPTCHA non-JSON response: %r", getattr(r, "text", "")[:200])
        return False

    logging.warning("reCAPTCHA response: %s", payload)

    ok = payload.get("success") is True
    score = float(payload.get("score") or 0)
    action = payload.get("action")
    if not ok:
        return False
    if score < 0.5:
        return False
    if action and action != "appointment":
        return False
    return True
