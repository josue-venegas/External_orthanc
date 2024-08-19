import orthanc
import girder_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("authentication")
logger.setLevel(logging.INFO)

LOCAL_URL = "localhost"
LOCAL_IP = "127.0.0.1"
HOST_IP = "host.docker.internal"  # Host URL : since we are in a Docker localhost and 127.0.0.1 have to be redirected to the host machine

print("Registering filter function...")


def Filter(uri: str, **request):
    logger.debug("User trying to access URI : %s" % uri)

    if "dicom-web" not in uri:
        return allow_access(uri)

    return handle_dicom_web(uri, **request)


def handle_dicom_web(uri: str, **request):
    gc, token = init_client(request)
    if not gc:
        logger.error(f"Couldn't init Girder client : missing information (URI: {uri})")
        return False

    try:
        with gc.session() as session:
            session.verify = (
                HOST_IP not in gc.urlBase
            )  # disable ssl check if sending request to host because host certificate is self-signed
            session.headers["cookie"] = request["headers"].get("cookie", "")
            params = {
                "sourceType": "Orthanc",
                "uri": uri,
                #"token": token,  # should be removed in future versions (the Girder client should handle the token)
            }

            if "/dicom-web/studies" == uri:
                return allow_access(uri)

            resp = gc.sendRestRequest(
                "GET", "authOhif/uriVerification", parameters=params
            )

            if resp:
                return allow_access(uri)
            else:
                return deny_access(uri)
    except Exception as ex:
        logger.error(
            f"Error while checking access to uri {uri} (Girder server : '{gc.urlBase}', error: <{type(ex)}: {str(ex)}>)"
        )
        return False


def init_client(request):
    cookies = request["headers"].get("cookie", "")
    cookie_dict = (
        {
            cookie.split("=")[0].strip(): cookie.split("=")[1].strip()
            for cookie in cookies.split(";")
        }
        if cookies != ""
        else {}
    )

    url = cookie_dict.get("girderUrl", "")
    token = cookie_dict.get("girderToken", "")

    if url and token:
        apiUrl = (
            url.replace("%3A", ":")
            .replace(LOCAL_URL, HOST_IP)
            .replace(LOCAL_IP, HOST_IP)
        )

        gc = girder_client.GirderClient(apiUrl=apiUrl)
        gc.setToken(token)
        return gc, token

    url = request["headers"].get("serverurl", "")
    token = request["headers"].get("servertoken", "")
    if url and token:
        apiUrl = (
            url.replace("%3A", ":")
            .replace(LOCAL_URL, HOST_IP)
            .replace(LOCAL_IP, HOST_IP)
        )

        gc = girder_client.GirderClient(apiUrl=apiUrl)
        gc.setToken(token)
        return gc, token

    return None, None


def allow_access(uri: str):
    logger.info(f"Access allowed to {uri}")
    return True


def deny_access(uri: str):
    logger.warning(f"Access denied to {uri}")
    return False


orthanc.RegisterIncomingHttpRequestFilter(Filter)  # type: ignore
