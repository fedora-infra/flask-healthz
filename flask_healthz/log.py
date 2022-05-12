class PrefixFilter:
    def __init__(self, prefix):
        self.prefix = prefix

    # gunicorn seems to be using both int and str for status codes
    SUCCESS_STATUS = (200, "200")

    def filter(self, record):
        url = None

        # Gunicorn logs
        url = record.args.get("U") if isinstance(record.args, dict) else None

        do_not_log = (
            url is not None
            and url.startswith(f"{self.prefix}/")
            and record.args.get("s") in PrefixFilter.SUCCESS_STATUS
        )
        return 0 if do_not_log else 1
