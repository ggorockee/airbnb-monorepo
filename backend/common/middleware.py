# common/middleware.py

import logging

# 'access' 로거는 settings.py에서 정의한 로거 이름
access_logger = logging.getLogger("access")


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 요청 처리 전에 로그를 남길 수 있음 (필요 시)

        response = self.get_response(request)

        # 응답 후에 로그 남기기
        # User-Agent, IP 등 필요한 정보를 추가할 수 있음
        log_data = {
            "user": (
                request.user.username if request.user.is_authenticated else "anonymous"
            ),
            "method": request.method,
            "path": request.get_full_path(),
            "status_code": response.status_code,
        }
        access_logger.info(log_data)

        return response
