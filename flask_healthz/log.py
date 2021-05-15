class PrefixFilter:
    def __init__(self, prefix):
        self.prefix = prefix

    def filter(self, record):
        url = None

        # Gunicorn logs
        url = record.args.get("U") if isinstance(record.args, dict) else None

        if url is not None and url.startswith(f"{self.prefix}/"):
            return 0
        return 1
