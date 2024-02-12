from . import output

from .config import Config


def init_output() -> output.OutputBase:
    print(" > init", Config.OUTPUT_MODULE)
    if Config.OUTPUT_MODULE == "local":
        if not Config.OUTPUT_LOCAL_DIR:
            raise ValueError("Config.OUTPUT_LOCAL_DIR unset")

        return output.LocalDirOutput(Config.OUTPUT_LOCAL_DIR)

    elif Config.OUTPUT_MODULE == "webploy":
        if not Config.OUTPUT_WEBPLOY_URL:
            raise ValueError("Config.OUTPUT_WEBPLOY_URL unset")

        if not Config.OUTPUT_WEBPLOY_SITE:
            raise ValueError("Config.OUTPUT_WEBPLOY_SITE unset")

        if not Config.OUTPUT_WEBPLOY_USER:
            raise ValueError("Config.OUTPUT_WEBPLOY_USER unset")

        if not Config.OUTPUT_WEBPLOY_PASSWORD:
            raise ValueError("Config.OUTPUT_WEBPLOY_PASSWORD unset")

        return output.WebployOutput(
            Config.OUTPUT_WEBPLOY_URL,
            Config.OUTPUT_WEBPLOY_SITE,
            Config.OUTPUT_WEBPLOY_USER,
            Config.OUTPUT_WEBPLOY_PASSWORD,
            Config.OUTPUT_WEBPLOY_META
        )

    else:
        raise ValueError("unknown output module")
