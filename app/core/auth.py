import os

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def get_current_username(
    request: Request, authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> str:
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        # Lambda実行の場合（sam local start-apiも含む）
        event = request.scope["event"]
        claims = event["requestContext"]["authorizer"]["claims"]
        return claims["cognito:username"]

    if os.environ["STAGE"] == "local":
        # Lambda実行でないかつローカルの場合＝docker composeによるFastAPI起動
        token = authorization.credentials
        if username := jwt.decode(token, options={"verify_signature": False}).get("username"):
            return username

    raise HTTPException(status_code=401)
