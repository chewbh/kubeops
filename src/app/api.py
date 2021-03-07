
from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from .svcreq import router as svcreq_router

URI_PREFIX_API = "api"
URI_PREFIX_API_DOCS = "docs"
API_VERSION_V1 = "v1"
LATEST_API_VERSION = API_VERSION_V1

api_router = APIRouter(default_response_class=JSONResponse)

# api routes (by version)
# NOTE: all api routes should be authenticated by default
router_v1 = APIRouter()

router_v1.include_router(
    svcreq_router, prefix="/requests", tags=["service requests"])


# api_router.include_router(authenticated_api_router,
#     dependencies=[Depends(get_current_user)])

#auth_api_router = APIRouter()
#api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

# api docs (by version) via open api
doc_router_v1 = APIRouter()


@doc_router_v1.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint_v1():
    return JSONResponse(get_openapi(
        title="API Documentation",
        version=API_VERSION_V1,
        routes=router_v1.routes))


@doc_router_v1.get("/", include_in_schema=False)
async def get_api_documentation_v1():
    return get_swagger_ui_html(
        openapi_url=f"/{URI_PREFIX_API}/{API_VERSION_V1}/{URI_PREFIX_API_DOCS}/openapi.json",
        title="API Documentation")

router_v1.include_router(doc_router_v1, prefix=f"/{URI_PREFIX_API_DOCS}")
api_router.include_router(router_v1, prefix=f"/{API_VERSION_V1}")
