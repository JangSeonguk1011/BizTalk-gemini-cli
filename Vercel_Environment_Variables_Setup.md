# Vercel 환경 변수 설정 안내

Vercel에 배포된 애플리케이션에서 Groq API 키를 안전하게 사용하려면, Vercel 프로젝트 설정에 환경 변수로 `GROQ_API_KEY`를 추가해야 합니다.

**설정 방법:**

1.  **Vercel 대시보드 접속**: [vercel.com](https://vercel.com/)에 로그인한 후, 해당 프로젝트 대시보드로 이동합니다.
2.  **프로젝트 설정 열기**: 프로젝트 페이지에서 'Settings' 탭을 클릭합니다.
3.  **환경 변수 추가**:
    *   좌측 메뉴에서 'Environment Variables'를 선택합니다.
    *   'Name' 필드에 `GROQ_API_KEY`를 입력합니다.
    *   'Value' 필드에 발급받은 실제 Groq API 키 값을 입력합니다.
    *   'Add' 버튼을 클릭하여 환경 변수를 추가합니다.
4.  **배포 범위 설정 (선택 사항)**: 일반적으로 'Production', 'Preview', 'Development' 세 가지 환경에 모두 추가하는 것이 권장됩니다.
5.  **변경 사항 적용**: 환경 변수 변경 후에는 새로운 배포가 필요할 수 있습니다. Vercel이 자동으로 새 빌드를 시작하지 않으면, 대시보드에서 수동으로 'Redeploy'를 트리거해야 합니다.

**주의사항:**

*   API 키와 같은 민감한 정보는 절대로 코드 저장소에 직접 커밋하지 마십시오. 항상 환경 변수를 통해 관리해야 합니다.
*   `GROQ_API_KEY`의 이름은 `backend/app.py`에서 `os.environ.get("GROQ_API_KEY")`로 참조되므로 정확하게 일치해야 합니다.