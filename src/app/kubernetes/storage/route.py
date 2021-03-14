from typing import Optional  # noqa: F401

from fastapi import APIRouter, Depends, HTTPException, Request  # noqa: F401
from pydantic import BaseModel


class JiraIssue(BaseModel):
    id: str
    # self: str
    key: str
    # fields: hashmap


class JSDRequest(BaseModel):
    issue: JiraIssue
    timestamp: int


router = APIRouter()


@router.post("/pv/smb")
def submit_create_smb_pv_request(request: JSDRequest):
    """
    Submit a request to create a SMB based persistent volume.
    It is taken that invocation of this endpoint implies approval
    is already granted (i.e. handled as part of the workflow in JSD).

    jira web hook indicate request must be POST. response code 200-300
    5 secs for connection and 20 secs for response. Note JSD will not retry

    payload
    """
    return {"service": "requests"}
