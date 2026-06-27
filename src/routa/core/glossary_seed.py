"""Routa glossary seed.

Single source of truth for all Routa-specific user-facing strings.
Portal/shared keys (brand, nav_*, manifest_name, error_unauthorized, etc.)
live in avalone_core.glossary_db and are NOT duplicated here.
"""

from typing import Any

from routa.core import glossary, ui_glossary


def _row(key: str, ru: str, en: str, ko: str, kind: str = "ui", desc: str = "") -> dict[str, Any]:
    return {
        "key": key,
        "ru": ru,
        "en": en,
        "ko": ko,
        "kind": kind,
        "module": "work",
        "desc": desc or ui_glossary.describe(key),
    }


_ROUTA_SEED: list[dict[str, Any]] = [
    # --- Manifest ---
    _row("manifest_name_work", "Работа — Avalone", "Work — Avalone", "업무 — Avalone", "manifest"),
    _row("manifest_short_name_work", "Работа", "Work", "업무", "manifest"),

    # --- Work page: buttons ---
    _row("btn_create_trip", "Создать поездку", "Create trip", "출퇴근 만들기"),
    _row("btn_save", "Сохранить", "Save", "저장"),
    _row("btn_cancel", "Отмена", "Cancel", "취소"),
    _row("btn_invite", "Пригласить", "Invite", "초대"),
    _row("btn_copy", "Копировать", "Copy", "복사"),
    _row("btn_open", "Открыть", "Open", "열기"),
    _row("btn_edit", "Редактировать", "Edit", "편집"),
    _row("btn_close", "Закрыть", "Close", "닫기"),
    _row("btn_reopen", "Открыть снова", "Reopen", "다시 열기"),
    _row("btn_delete", "Удалить", "Delete", "삭제"),
    _row("btn_export_csv", "Скачать CSV", "Download CSV", "CSV 다운로드"),
    _row("btn_mark_read", "Отметить все прочитанными", "Mark all read", "모두 읽음 표시"),
    _row("btn_open_profile", "Открыть профиль", "Open profile", "프로필 열기"),

    # --- Work page: labels ---
    _row("label_filter_all", "Все", "All", "전체"),
    _row("label_filter_upcoming", "Предстоящие", "Upcoming", "예정"),
    _row("label_filter_past", "Прошедшие", "Past", "지난"),
    _row("label_filter_mine", "Мои", "Mine", "내 것"),
    _row("label_period_all", "Всё время", "All time", "전체 기간"),
    _row("label_period_year", "Год", "Year", "년"),
    _row("label_period_month", "Месяц", "Month", "월"),
    _row("label_period_week", "Неделя", "Week", "주"),
    _row("label_profile", "Профиль", "Profile", "프로필"),
    _row("label_profile_hint", "Профиль редактируется на портале Avalone.", "Profile is managed on the Avalone portal.", "프로필은 Avalone 포털에서 관리됩니다."),
    _row("label_notify_invites", "Email о приглашениях", "Email about invites", "초대 이메일"),
    _row("label_notify_roles", "Email об изменении роли", "Email about role changes", "역할 변경 이메일"),
    _row("label_notify_reminders", "Напоминания о поездках", "Trip reminders", "출퇴근 알림"),
    _row("label_direction", "Направление", "Direction", "방향"),
    _row("label_to_work", "На работу", "To work", "출근"),
    _row("label_from_work", "С работы", "From work", "퇴근"),
    _row("label_date", "Дата", "Date", "날짜"),
    _row("label_time", "Время", "Time", "시간"),
    _row("label_comment", "Комментарий", "Comment", "코멘트"),
    _row("label_members", "Участники", "Members", "참석자"),
    _row("label_driver", "Водитель", "Driver", "운전자"),
    _row("label_passenger", "Пассажир", "Passenger", "동승자"),
    _row("label_not_going", "Не еду", "Not going", "미참석"),
    _row("label_unknown", "Не определился", "Undecided", "미정"),
    _row("label_trip_open", "Открыта", "Open", "열림"),
    _row("label_trip_closed", "Закрыта", "Closed", "닫힘"),
    _row("label_trip_cancelled", "Отменена", "Cancelled", "취소됨"),
    _row("label_empty_trips", "Пока нет поездок", "No trips yet", "출퇴근 없음"),
    _row("label_empty_trips_hint", "Создайте первую поездку, чтобы начать", "Create the first trip to get started", "첫 출퇴근을 만들어보세요"),
    _row("label_loading", "Загрузка...", "Loading...", "로딩 중..."),
    _row("label_no_data", "Нет данных", "No data", "데이터 없음"),
    _row("label_copied", "Ссылка скопирована", "Link copied", "링크 복사됨"),
    _row("label_trip_updated", "Поездка обновлена", "Trip updated", "출퇴근이 업데이트되었습니다"),
    _row("label_trip_created", "Поездка создана", "Trip created", "출퇴근이 생성되었습니다"),
    _row("label_organizer", "Организатор", "Organizer", "주최자"),
    _row("label_seats", "мест", "seats", "석"),
    _row("label_member", "Участник", "Member", "참석자"),
    _row("label_members_count", "участников", "members", "명"),
    _row("label_invite_title", "Пригласить", "Invite", "초대"),
    _row("label_invite_hint", "Отправьте ссылку — человек сможет присоединиться после входа в Avalone.", "Send the link — the person can join after signing in to Avalone.", "링크를 복사해서 복사 — Avalone에 로그인 후 참석할 수 있습니다."),
    _row("label_activity_by_day", "Активность по дням", "Activity by day", "일별 활동"),
    _row("label_empty_notifications", "Нет уведомлений", "No notifications", "알림 없음"),
    _row("title_edit_trip", "Редактировать поездку", "Edit trip", "출퇴근 편집"),

    # --- Work page: errors / confirmations ---
    _row("error_load_trips", "Не удалось загрузить поездки", "Could not load trips", "출퇴근을 불러올 수 없습니다", "error"),
    _row("error_load_notifications", "Не удалось загрузить уведомления", "Could not load notifications", "알림을 불러올 수 없습니다", "error"),
    _row("error_load_stats", "Не удалось загрузить статистику", "Could not load statistics", "통계를 불러올 수 없습니다", "error"),
    _row("error_not_found_trip", "Поездка не найдена", "Trip not found", "출퇴근을 찾을 수 없습니다", "error"),
    _row("error_enter_date", "Укажите дату и время", "Please enter date and time", "날짜와 시간을 입력하세요", "error"),
    _row("confirm_delete_trip", "Удалить поездку?", "Delete trip?", "출퇴근을 삭제할까요?", "ui"),

    # --- Stats labels ---
    _row("label_stat_total", "Всего поездок", "Total trips", "총 출퇴근"),
    _row("label_stat_driver", "Водителем", "As driver", "운전자로"),
    _row("label_stat_passenger", "Пассажиром", "As passenger", "동승자로"),

    # --- Dashboard ---
    _row("label_dashboard_subtitle", "на {today}", "on {today}", "{today}"),
    _row("label_assets", "Активы", "Assets", "자산"),
    _row("label_liabilities", "Обязательства", "Liabilities", "부채"),
    _row("label_net", "Чистыми", "Net", "순자산"),
    _row("label_account_balances", "Остатки по счетам", "Account balances", "계좌 잔액"),
    _row("label_expenses_by_category", "Расходы по категориям", "Expenses by category", "카테고리별 지출"),
    _row("label_recent_entries", "Последние проводки", "Recent entries", "최근 거래"),

    # --- Admin dashboard ---
    _row("admin_title", "Админ — Работа", "Admin — Work", "관리자 — 업무", "admin"),
    _row("admin_subtitle", "Панель управления инстансом · build", "Instance admin panel · build", "인스턴스 관리 패널 · build", "admin"),
    _row("section_instance", "Инстанс", "Instance", "인스턴스", "admin"),
    _row("section_config", "Конфигурация", "Configuration", "설정", "admin"),
    _row("label_reg_mode", "Режим регистрации", "Registration mode", "등록 모드", "admin"),
    _row("label_reg_mode_open", "Открытая", "Open", "공개", "admin"),
    _row("label_reg_mode_invite", "По приглашению", "Invite only", "초대 전용", "admin"),
    _row("label_reg_mode_closed", "Закрытая", "Closed", "비공개", "admin"),
    _row("label_invite_code", "Код приглашения", "Invite code", "초대 코드", "admin"),
    _row("label_strict_pw", "Строгая политика паролей (≥8, заглавная, строчная, цифра, спецсимвол)", "Strict password policy (≥8, uppercase, lowercase, digit, special)", "엄격한 비밀번호 정책 (8자 이상, 대문자, 소문자, 숫자, 특수문자)", "admin"),
    _row("label_base_currency", "Базовая валюта", "Base currency", "기준 통화", "admin"),
    _row("label_llm_provider", "LLM-провайдер", "LLM provider", "LLM 공급자", "admin"),
    _row("label_llm_model", "LLM-модель", "LLM model", "LLM 모델", "admin"),
    _row("label_llm_fallback", "Fallback LLM-модель", "Fallback LLM model", "Fallback LLM 모델", "admin"),
    _row("label_stt_model", "STT-модель", "STT model", "STT 모델", "admin"),
    _row("label_web_base_url", "Web base URL", "Web base URL", "Web 기본 URL", "admin"),
    _row("btn_save_settings", "Сохранить настройки", "Save settings", "설정 저장", "admin"),
    _row("heading_static_constants", "Статические константы", "Static constants", "정적 상수", "admin"),
    _row("section_runtime_constants", "Константы runtime", "Runtime constants", "Runtime 상수", "admin"),
    _row("hint_runtime_constants", "Числовые пороги, таймауты и лимиты. Меняются без перезапуска.", "Numeric thresholds, timeouts and limits. Change without restart.", "숫자 임계값, 시간 초과 및 제한. 재시작 없이 변경.", "admin"),
    _row("btn_save_constants", "Сохранить константы", "Save constants", "상수 저장", "admin"),
    _row("section_secrets", "Секреты (read-only)", "Secrets (read-only)", "비밀 (읽기 전용)", "admin"),
    _row("hint_secrets", "Меняются через env-переменные / launchctl / plist сервиса.", "Change via env vars / launchctl / service plist.", "env 변수 / launchctl / 서비스 plist에서 변경.", "admin"),
    _row("section_users", "Пользователи", "Users", "사용자", "admin"),
    _row("section_admins", "Администраторы", "Administrators", "관리자", "admin"),
    _row("label_add_admin", "Добавить администратора (логин)", "Add administrator (login)", "관리자 추가 (로그인)", "admin"),
    _row("placeholder_login", "логин", "login", "로그인", "admin"),
    _row("section_logs", "Логи", "Logs", "로그", "admin"),
    _row("btn_refresh", "Обновить", "Refresh", "새로고침", "admin"),
    _row("label_empty_logs", "(пусто)", "(empty)", "(비어 있음)", "admin"),
    _row("section_danger", "Опасная зона", "Danger zone", "위험 영역", "admin"),
    _row("hint_danger_restart", "Перезапускает весь сервис. launchd поднимет процесс заново.", "Restarts the whole service. launchd will bring it back up.", "전체 서비스를 재시작합니다. launchd가 다시 시작합니다.", "admin"),
    _row("btn_restart_work", "Перезапустить Работу", "Restart Work", "업무 재시작", "admin"),
    _row("label_restart_confirm1", "Перезапустить Работу? Сервис будет недоступен несколько секунд.", "Restart Work? The service will be unavailable for a few seconds.", "업무를 재시작할까요? 서비스를 몇 초 동안 사용할 수 없습니다.", "admin"),
    _row("label_restart_confirm2", "Точно? Все активные сессии прервутся.", "Are you sure? All active sessions will be interrupted.", "확실합니까? 모든 활성 세션이 중단됩니다.", "admin"),
    _row("label_restart_wait", "Перезапуск… обновите страницу через несколько секунд.", "Restarting… refresh the page in a few seconds.", "재시작 중… 몇 초 후 페이지를 새로고침하세요.", "admin"),
    _row("section_qr", "QR-код приложения", "App QR code", "앱 QR 코드", "admin"),
    _row("hint_qr", "Ссылка на главную страницу Работы.", "Link to the Work home page.", "업무 메인 페이지 링크.", "admin"),
    _row("section_health", "Health", "Health", "Health", "admin"),
    _row("label_db_available", "БД доступна", "DB available", "DB 사용 가능", "admin"),
    _row("label_db_path", "Путь к БД", "DB path", "DB 경로", "admin"),
    _row("label_ok", "OK", "OK", "OK", "admin"),
    _row("label_fail", "FAIL", "FAIL", "FAIL", "admin"),
    _row("btn_logout", "Выйти", "Log out", "로그아웃", "admin"),
    _row("label_database", "База данных", "Database", "데이터베이스", "admin"),
    _row("label_db_size", "Размер БД", "DB size", "DB 크기", "admin"),
    _row("label_id", "ID", "ID", "ID", "admin"),
    _row("label_verified", "Подтв.", "Verified", "확인", "admin"),
    _row("label_created", "Создан", "Created", "생성", "admin"),
    _row("label_actions", "Действия", "Actions", "작업", "admin"),
    _row("btn_reset_password", "Сбросить пароль", "Reset password", "비밀번호 재설정", "admin"),
    _row("btn_delete_user", "Удалить", "Delete", "삭제", "admin"),
    _row("confirm_reset_password", "Сбросить пароль пользователю {login}?", "Reset password for {login}?", "{login}의 비밀번호를 재설정할까요?", "admin"),
    _row("label_reset_link", "Ссылка для сброса пароля для {login} (действительна {expires_min} мин):", "Password reset link for {login} (valid {expires_min} min):", "{login}의 비밀번호 재설정 링크 ({expires_min}분 유효):", "admin"),
    _row("confirm_delete_user", "УДАЛИТЬ пользователя {login} и ВСЕ его данные? Это необратимо.", "DELETE user {login} and ALL their data? This cannot be undone.", "사용자 {login}과(와) 모든 데이터를 삭제할까요? 되돌릴 수 없습니다.", "admin"),
    _row("label_user_deleted", "Пользователь удалён", "User deleted", "사용자가 삭제되었습니다", "admin"),
    _row("label_no_users", "Нет пользователей", "No users", "사용자 없음", "admin"),
    _row("label_no_admins", "Нет администраторов", "No admins", "관리자 없음", "admin"),
    _row("confirm_remove_admin", "Снять права администратора?", "Remove admin rights?", "관리자 권한을 해제할까요?", "admin"),
    _row("label_admin_added", "Добавлен: {login}", "Added: {login}", "추가됨: {login}", "admin"),
    _row("label_saved", "Сохранено", "Saved", "저장됨", "admin"),
    _row("label_error_prefix", "Ошибка: {msg}", "Error: {msg}", "오류: {msg}", "admin"),

    # --- API / backend errors ---
    _row("error_forbidden", "Доступ запрещён", "Forbidden", "접근 금지", "error"),
    _row("error_amount_positive", "сумма должна быть положительным числом", "amount must be a positive number", "금액은 양수여야 합니다", "error"),
    _row("error_unknown_account", "неизвестный счёт", "unknown account", "알 수 없는 계좌", "error"),
    _row("error_entry_not_found", "запись не найдена", "entry not found", "기록을 찾을 수 없습니다", "error"),
    _row("error_entry_accounts_read", "не удалось прочитать счета записи", "could not read entry accounts", "거래 계좌를 읽을 수 없습니다", "error"),
    _row("error_old_password_wrong", "Старый пароль неверен", "Old password is wrong", "현재 비밀번호가 틀렸습니다", "error"),
    _row("error_invalid_email", "Некорректная почта", "Invalid email", "잘못된 이메일", "error"),
    _row("error_rate_limit", "Слишком часто. Подождите.", "Too many requests. Please wait.", "너무 많은 요청입니다. 잠시 후 다시 시도하세요.", "error"),
    _row("error_email_required", "Сначала укажите почту", "Please set an email first", "먼저 이메일을 설정하세요", "error"),
    _row("error_email_not_configured", "Почта не настроена на сервере", "Email is not configured on the server", "서버에서 이메일이 설정되지 않았습니다", "error"),
    _row("error_empty_name", "пустое имя", "name is empty", "이름이 비어 있습니다", "error"),
    _row("error_unknown_currency", "неизвестная валюта", "unknown currency", "알 수 없는 통화", "error"),
    _row("error_confirm_required", "требуется подтверждение", "confirmation required", "확인이 필요합니다", "error"),
    _row("error_move_to_required", "укажите счёт для переноса", "target account required", "이체 대상 계좌를 지정하세요", "error"),
    _row("error_bad_target", "некорректный счёт назначения", "invalid target account", "잘못된 대상 계좌", "error"),
    _row("error_invalid_mode", "некорректный режим регистрации", "invalid registration mode", "잘못된 등록 모드", "error"),
    _row("error_invalid_value", "некорректное значение: {key}", "invalid value: {key}", "잘못된 값: {key}", "error"),
    _row("error_invalid_currency", "некорректная валюта", "invalid currency", "잘못된 통화", "error"),
    _row("error_invalid_code", "неверный код подтверждения", "invalid verification code", "잘못된 인증 코드", "error"),
    _row("error_unknown_constant", "неизвестная константа: {key}", "unknown constant: {key}", "알 수 없는 상수: {key}", "error"),
    _row("error_cannot_reset_self", "нельзя сбросить пароль самому себе", "cannot reset your own password here", "여기서 자신의 비밀번호는 재설정할 수 없습니다", "error"),
    _row("error_last_admin", "нельзя удалить последнего администратора", "cannot remove the last admin", "마지막 관리자는 삭제할 수 없습니다", "error"),
    _row("error_cannot_delete_self", "нельзя удалить самого себя", "cannot delete yourself", "자신을 삭제할 수 없습니다", "error"),
    _row("error_user_app_required", "требуются user_id и app_id", "user_id and app_id required", "user_id와 app_id가 필요합니다", "error"),
    _row("error_unknown_app", "неизвестное приложение: {app_id}", "unknown app: {app_id}", "알 수 없는 앱: {app_id}", "error"),
    _row("error_trip_creator_edit", "только организатор может редактировать", "only the creator can edit", "주최자만 편집할 수 있습니다", "error"),
    _row("error_trip_creator_delete", "только организатор может удалить", "only the creator can delete", "주최자만 삭제할 수 있습니다", "error"),
    _row("error_trip_not_found", "поездка не найдена", "trip not found", "출퇴근을 찾을 수 없습니다", "error"),
    _row("error_trip_closed", "поездка закрыта или отменена", "trip is closed or cancelled", "출퇴근이 닫혔거나 취소되었습니다", "error"),
    _row("error_invalid_invite_code", "некорректный код приглашения", "invalid invite code", "잘못된 초대 코드", "error"),
    _row("error_not_member", "вы не участник этой поездки", "not a member of this trip", "이 출퇴근의 참석자가 아닙니다", "error"),
    _row("error_currency_transfer", "перевод между счетами разной валюты запрещён", "transfer between accounts of different currencies is forbidden", "다른 통화 계좌 간 이체는 금지되어 있습니다", "error"),
    _row("error_account_in_use", "счёт {name} ещё используется в {used} строках проводок", "account {name} is still used in {used} ledger lines", "계좌 {name}은(는) 아직 {used}개의 거래 라인에서 사용 중", "error"),
    _row("error_amount_positive_core", "сумма должна быть положительной", "amount must be positive", "금액은 양수여야 합니다", "error"),
    _row("error_unbalanced_entries", "несбалансированные проводки: {bad}", "unbalanced entries: {bad}", "불균형 거래: {bad}", "error"),
    _row("error_global_imbalance", "глобальный дисбаланс: debit={gd} credit={gc}", "global imbalance: debit={gd} credit={gc}", "전체 불균형: debit={gd} credit={gc}", "error"),
    _row("error_tenant_missing", "tenant не установлен", "tenant is not set", "테넌트가 설정되지 않았습니다", "error"),
    _row("error_login_password_required", "логин и пароль обязательны", "login and password are required", "아이디와 비밀번호는 필수입니다", "error"),
    _row("error_admin_only", "только администратор может менять глобальные настройки", "only admins can change global settings", "관리자만 전역 설정을 변경할 수 있습니다", "error"),

    # --- Password validation errors ---
    _row("error_password_empty", "Пароль не может быть пустым", "Password cannot be empty", "비밀번호는 비워둘 수 없습니다", "error"),
    _row("error_password_too_short", "Пароль ≥{min_len} символов", "Password must be ≥{min_len} characters", "비밀번호는 {min_len}자 이상이어야 합니다", "error"),
    _row("error_password_no_upper", "Пароль должен содержать заглавную букву", "Password must contain an uppercase letter", "비밀번호에 대문자가 포함되어야 합니다", "error"),
    _row("error_password_no_lower", "Пароль должен содержать строчную букву", "Password must contain a lowercase letter", "비밀번호에 소문자가 포함되어야 합니다", "error"),
    _row("error_password_no_digit", "Пароль должен содержать цифру", "Password must contain a digit", "비밀번호에 숫자가 포함되어야 합니다", "error"),
    _row("error_password_no_special", "Пароль должен содержать спецсимвол", "Password must contain a special character", "비밀번호에 특수문자가 포함되어야 합니다", "error"),

    # --- Email templates ---
    _row("email_verify_subject", "Код подтверждения Routa", "Routa verification code", "Routa 인증 코드", "email"),
    _row("email_verify_body", "Ваш код подтверждения: {code}\n\nКод действителен 30 минут. Если вы не запрашивали подтверждение — просто проигнорируйте письмо.", "Your verification code: {code}\n\nThe code is valid for 30 minutes. If you did not request verification, simply ignore this email.", "인증 코드: {code}\n\n코드는 30분 동안 유효합니다. 인증을 요청하지 않으셨다면 이 이메일을 무시하세요.", "email"),
    _row("email_reset_subject", "Сброс пароля", "Password reset", "비밀번호 재설정", "email"),
    _row("email_reset_body", "Вы запросили сброс пароля Routa.\n\nПерейдите по ссылке, чтобы задать новый пароль:\n{link}\n\nСсылка действительна {expires_min} минут. Если вы не запрашивали сброс — проигнорируйте письмо.", "You requested a Routa password reset.\n\nFollow the link to set a new password:\n{link}\n\nThe link is valid for {expires_min} minutes. If you did not request a reset, please ignore this email.", "Routa 비밀번호 재설정을 요청하셨습니다.\n\n새 비밀번호를 설정하려면 링크를 클릭하세요:\n{link}\n\n링크는 {expires_min}분 동안 유효합니다. 재설정을 요청하지 않으셨다면 이 이메일을 무시하세요.", "email"),
]

# --- Tips ---
_TIP_TEXTS: dict[str, dict[str, dict[str, str]]] = {
    "expense_gt_income": {
        "ru": {"title": "Вы живёте за счёт будущего себя", "body": "Расходы превысили доходы. Найдите сегодня одну трату, которую можно отложить или сократить.", "book": "Morgan Housel — The Psychology of Money"},
        "en": {"title": "You're borrowing from your future self", "body": "Expenses exceeded income. Find one spend you can delay or cut today.", "book": "Morgan Housel — The Psychology of Money"},
        "ko": {"title": "미래의 자신에게 빌려 살고 있습니다", "body": "지출이 수입을 초과했습니다. 오늘 미루거나 줄일 수 있는 지출 하나를 찾으세요.", "book": "Morgan Housel — The Psychology of Money"},
    },
    "no_savings": {
        "ru": {"title": "Вы платите всем, кроме себя", "body": "В этом периоде нет отложенного. Переведите 10% дохода в сбережения сразу при получении — до того, как деньги растворятся.", "book": "George Clason — The Richest Man in Babylon"},
        "en": {"title": "You're paying everyone except yourself", "body": "No savings this period. Move 10% of income to savings the moment you receive it.", "book": "George Clason — The Richest Man in Babylon"},
        "ko": {"title": "자신 외 모두에게 지불하고 있습니다", "body": "이 기간 저축이 없습니다. 돈이 사라지기 전에 수입의 10%를 저축으로 옮기세요.", "book": "George Clason — The Richest Man in Babylon"},
    },
    "housing_high": {
        "ru": {"title": "Жильё съедает больше трети", "body": "Вы работаете больше месяца в году только на крышу над головой. Пересмотрите аренду, тарифы или страховки.", "book": "Thomas Stanley — The Millionaire Next Door"},
        "en": {"title": "Housing eats more than a third", "body": "You work more than a month per year just for a roof. Review rent, utilities or insurance.", "book": "Thomas Stanley — The Millionaire Next Door"},
        "ko": {"title": "주거비가 3분의 1 이상", "body": "지붕을 위해 1년 중 한 달 이상 일합니다. 임대료, 공과금, 보험을 재검토하세요.", "book": "Thomas Stanley — The Millionaire Next Door"},
    },
    "debt": {
        "ru": {"title": "Долг крадёт ваше будущее", "body": "Прошлое не должно управлять вашим завтра. Закройте самый маленький долг агрессивно — первая победа даст импульс.", "book": "Dave Ramsey — The Total Money Makeover"},
        "en": {"title": "Debt is stealing your future", "body": "Your past shouldn't run your tomorrow. Attack the smallest debt first for momentum.", "book": "Dave Ramsey — The Total Money Makeover"},
        "ko": {"title": "빚이 미래를 훔치고 있습니다", "body": "과거가 내일을 지배하지 않게 하세요. 가장 작은 빚부터 공격적으로 갚아 모멘텀을 만드세요.", "book": "Dave Ramsey — The Total Money Makeover"},
    },
    "subscriptions_high": {
        "ru": {"title": "Подписки исчезают из головы, но не из выписки", "body": "Проведите аудит: отмените всё, что вы не использовали за последние 30 дней.", "book": "Ramit Sethi — I Will Teach You to Be Rich"},
        "en": {"title": "Subscriptions vanish from memory, not statements", "body": "Audit them: cancel anything you haven't used in the last 30 days.", "book": "Ramit Sethi — I Will Teach You to Be Rich"},
        "ko": {"title": "구독은 기억에서 사라지지만 명세서는 아닙니다", "body": "점검하세요: 최근 30일 동안 사용하지 않은 구독을 모두 해지하세요.", "book": "Ramit Sethi — I Will Teach You to Be Rich"},
    },
    "eating_out_gt_food": {
        "ru": {"title": "Вы кормите рестораны, а не себя", "body": "Траты на еду вне дома превысили продукты. Попробуйте неделю готовить дома — разница в бюджете и самочувствии ощутима.", "book": "Vicki Robin — Your Money or Your Life"},
        "en": {"title": "You're feeding restaurants, not yourself", "body": "Eating out beat groceries. Try one week of home cooking and feel the budget difference.", "book": "Vicki Robin — Your Money or Your Life"},
        "ko": {"title": "식당을 먹이고 있습니다", "body": "외식비가 식료품을 넘었습니다. 일주일간 집에서 요리해 예산 차이를 느껴 보세요.", "book": "Vicki Robin — Your Money or Your Life"},
    },
    "shopping_high": {
        "ru": {"title": "Вещи обещают счастье, но крадут свободу", "body": "Перед покупкой спросите: 'Готов ли я отдать за это часы жизни, на которые заработал?' Если нет — отложите на 30 дней.", "book": "Vicki Robin — Your Money or Your Life"},
        "en": {"title": "Stuff promises happiness but steals freedom", "body": "Before buying, ask: 'Am I willing to trade the life-hours I earned this for?' If not, wait 30 days.", "book": "Vicki Robin — Your Money or Your Life"},
        "ko": {"title": "물건은 행복을 약속하지만 자유를 훔칩니다", "body": "구매 전 스스로에게 물으세요: '이것을 위해 번 시간을 희생할 의사가 있나요?' 아니라면 30일 미루세요.", "book": "Vicki Robin — Your Money or Your Life"},
    },
    "no_education": {
        "ru": {"title": "Вы не вкладываете в главный актив — себя", "body": "90 дней без инвестиций в навыки. Купите книгу или курс — это единственная инвестиция с гарантированной доходностью.", "book": "Robert Kiyosaki — Rich Dad Poor Dad"},
        "en": {"title": "You're not investing in your best asset — you", "body": "90 days without skill spending. Buy a book or course; it's the only guaranteed-return investment.", "book": "Robert Kiyosaki — Rich Dad Poor Dad"},
        "ko": {"title": "최고의 자산인 자신에게 투자하지 않고 있습니다", "body": "90일 동안 기술 투자가 없습니다. 책이나 강의를 사세요. 유일한 보장 수익 투자입니다.", "book": "Robert Kiyosaki — Rich Dad Poor Dad"},
    },
    "fun_high": {
        "ru": {"title": "Развлечения стали главной статьёй", "body": "Бюджет не должен вращаться вокруг досуга. Бесплатный отдых — прогулки, библиотека, друзья — часто радует больше.", "book": "JL Collins — The Simple Path to Wealth"},
        "en": {"title": "Entertainment became the main budget line", "body": "Budget shouldn't revolve around leisure. Free rest — walks, library, friends — often brings more joy.", "book": "JL Collins — The Simple Path to Wealth"},
        "ko": {"title": "여가가 주요 예산 항목이 되었습니다", "body": "예산이 여가에 맞춰져서는 안 됩니다. 산책, 도서관, 친구들과의 물리적 휴식이 더 큰 기쁨을 줍니다.", "book": "JL Collins — The Simple Path to Wealth"},
    },
    "transport_high": {
        "ru": {"title": "Транспорт превратился в дыру", "body": "Сравните такси, общественный транспорт и личный авто. Часто самый удобный вариант — не самый дешёвый.", "book": "Scott Pape — The Barefoot Investor"},
        "en": {"title": "Transport became a leak", "body": "Compare taxi, public transit and owning a car. The most convenient option is often not the cheapest.", "book": "Scott Pape — The Barefoot Investor"},
        "ko": {"title": "교통비가 누수로 변했습니다", "body": "택시, 대중교통, 자차를 비교해 보세요. 가장 편한 선택이 가장 저렴한 것은 아닙니다.", "book": "Scott Pape — The Barefoot Investor"},
    },
    "health_zero": {
        "ru": {"title": "Экономия на здоровье — самая дорогая экономия", "body": "В этом месяце нет трат на здоровье. Профилактика сегодня стоит копеек по сравнению с лечением завтра.", "book": "Morgan Housel — The Psychology of Money"},
        "en": {"title": "Saving on health is the most expensive saving", "body": "No health spending this month. Prevention today costs pennies compared to treatment tomorrow.", "book": "Morgan Housel — The Psychology of Money"},
        "ko": {"title": "건강에 아끼는 것이 가장 비싼 절약입니다", "body": "이번 달 건강 지출이 없습니다. 예방은 내일 치료비와 비교하면 푼돈입니다.", "book": "Morgan Housel — The Psychology of Money"},
    },
    "income_up_savings_flat": {
        "ru": {"title": "Доход вырос, а сбережения — нет", "body": "Эффект образа жизни: расходы подстроились под доход. Прибавку надо автоматически перенаправлять в цели.", "book": "JL Collins — The Simple Path to Wealth"},
        "en": {"title": "Income rose but savings didn't", "body": "Lifestyle creep: spending adjusted to income. Auto-redirect raises to goals before you notice them.", "book": "JL Collins — The Simple Path to Wealth"},
        "ko": {"title": "수입은 늘었지만 저축은 아닙니다", "body": "라이프스타일 크립: 지출이 수입에 맞춰졌습니다. 알아차리기 전에 인상분을 목표로 자동 이체하세요.", "book": "JL Collins — The Simple Path to Wealth"},
    },
    "net_positive_streak": {
        "ru": {"title": "Вы стабильно в плюсе", "body": "Отличная работа. Следующий шаг — экстренный фонд на 3–6 месяцев расходов. Спокойствие дороже доходности.", "book": "JL Collins — The Simple Path to Wealth"},
        "en": {"title": "You're consistently in the green", "body": "Great job. Next step: an emergency fund covering 3–6 months of expenses. Peace beats returns.", "book": "JL Collins — The Simple Path to Wealth"},
        "ko": {"title": "꾸준히 흑자입니다", "body": "잘하고 있습니다. 다음 단계: 3~6개월 지출을 커버하는 비상자금입니다. 안정이 수익보다 소중합니다.", "book": "JL Collins — The Simple Path to Wealth"},
    },
    "travel_high": {
        "ru": {"title": "Путешествия съедают будущее", "body": "Путешествия важны, но не за счёт подушки безопасности. Откладывайте на поездку заранее, а не на кредитке.", "book": "Bill Perkins — Die with Zero"},
        "en": {"title": "Travel is eating your future", "body": "Travel matters, but not at the cost of your safety net. Save for trips in advance, not on credit.", "book": "Bill Perkins — Die with Zero"},
        "ko": {"title": "여행이 미래를 먹고 있습니다", "body": "여행은 중요하지만 안전망을 희생해서는 안 됩니다. 신용카드가 아닌 미리 저축하세요.", "book": "Bill Perkins — Die with Zero"},
    },
    "family_high": {
        "ru": {"title": "Семья не должна съедать всё", "body": "Дети — не инвестиция, но и их потребности не могут поглощать бюджет. Введите лимит на импульсные семейные покупки.", "book": "Ron Lieber — The Opposite of Spoiled"},
        "en": {"title": "Family shouldn't devour everything", "body": "Kids aren't an investment, but their needs can't swallow the budget. Cap impulse family spending.", "book": "Ron Lieber — The Opposite of Spoiled"},
        "ko": {"title": "가족이 모든 것을 삼켜서는 안 됩니다", "body": "아이들은 투자가 아니지만 그들의 필요가 예산을 삼켜서는 안 됩니다. 충동적 가족 지출에 한도를 정하세요.", "book": "Ron Lieber — The Opposite of Spoiled"},
    },
    "wants_gt_needs": {
        "ru": {"title": "Хочу обогнали нужды", "body": "Лайфстайл в обычный месяц не должен превышать базовые траты. Пересмотрите хотя бы одну категорию 'хочу'.", "book": "Vicki Robin — Your Money or Your Life"},
        "en": {"title": "Wants overtook needs", "body": "In a normal month, lifestyle shouldn't exceed basics. Review at least one 'want' category.", "book": "Vicki Robin — Your Money or Your Life"},
        "ko": {"title": "원하는 것이 필요를 앞섰습니다", "body": "평범한 달에 라이프스타일이 기본 지출을 초과해서는 안 됩니다. '원하는 것' 카테고리 하나를 검토하세요.", "book": "Vicki Robin — Your Money or Your Life"},
    },
    "goal_low": {
        "ru": {"title": "Вы работаете на сегодня, но не на завтра", "body": "На финансовые цели уходит меньше 10% дохода. Даже 5% в месяц создадут подушку через год. Начните с малого.", "book": "George Clason — The Richest Man in Babylon"},
        "en": {"title": "You're working for today, not tomorrow", "body": "Less than 10% of income goes to goals. Even 5% monthly builds a cushion in a year. Start small.", "book": "George Clason — The Richest Man in Babylon"},
        "ko": {"title": "오늘을 위해 일하지 내일은 아닙니다", "body": "수입의 10% 미만이 목표에 사용됩니다. 매달 5%만으로도 1년이면 쿠션이 생깁니다. 작게 시작하세요.", "book": "George Clason — The Richest Man in Babylon"},
    },
    "mindful_checkout": {
        "ru": {"title": "Стоя на кассе, задумайтесь", "body": "Точно ли этот товар стоит часов жизни, которые вы отдали, чтобы его заработать?", "book": "Vicki Robin — Your Money or Your Life"},
        "en": {"title": "At the checkout, pause", "body": "Is this item really worth the life-hours you traded to earn it?", "book": "Vicki Robin — Your Money or Your Life"},
        "ko": {"title": "계산대에서 잠시 멈추세요", "body": "이 물건이 정말 이를 위해 번 시간만큼 가치가 있나요?", "book": "Vicki Robin — Your Money or Your Life"},
    },
    "first_week": {
        "ru": {"title": "Идеальная категория — враг записи", "body": "Не гонитесь за идеалом. Лучше неточная запись, чем отсутствие записи. Внесите хотя бы одну трату сегодня.", "book": "James Clear — Atomic Habits"},
        "en": {"title": "Perfect categorization is the enemy of tracking", "body": "Don't chase perfection. A rough entry is better than no entry. Log at least one expense today.", "book": "James Clear — Atomic Habits"},
        "ko": {"title": "완벽한 분류는 기록의 적입니다", "body": "완벽을 추구하지 마세요. 부정확한 기록이 없는 것보다 낫습니다. 오늘 지출 하나라도 기록하세요.", "book": "James Clear — Atomic Habits"},
    },
    "irregular_entries": {
        "ru": {"title": "Финансовая амнезия начинается с пропущенной траты", "body": "Записывайте расходы сразу — это 10 секунд сейчас и часы экономии потом.", "book": "James Clear — Atomic Habits"},
        "en": {"title": "Financial amnesia starts with one missed expense", "body": "Log expenses immediately — 10 seconds now saves hours later.", "book": "James Clear — Atomic Habits"},
        "ko": {"title": "금융 망각은 하나의 누락된 지출에서 시작됩니다", "body": "지출을 즉시 기록하세요. 지금 10초가 나중에 시간을 절약합니다.", "book": "James Clear — Atomic Habits"},
    },
    "gratitude": {
        "ru": {"title": "Благодарность снижает импульс к покупкам", "body": "Прежде чем купить ещё одну вещь, назовите три, за которые вы уже благодарны. Желание часто уходит.", "book": "Rhonda Byrne — The Secret"},
        "en": {"title": "Gratitude reduces the urge to buy", "body": "Before buying another thing, name three you're grateful for. The urge often fades.", "book": "Rhonda Byrne — The Secret"},
        "ko": {"title": "감사는 구매 충동을 줄입니다", "body": "또 다른 것을 사기 전에 감사한 세 가지를 말해 보세요. 충동이 사라지는 경우가 많습니다.", "book": "Rhonda Byrne — The Secret"},
    },
    "praise_green": {
        "ru": {"title": "Вы на правильном пути", "body": "Доход превышает расходы и вы откладываете. Продолжайте, и через год удивитесь, как далеко продвинулись.", "book": "Morgan Housel — The Psychology of Money"},
        "en": {"title": "You're on the right track", "body": "Income exceeds spending and you're saving. Keep going; in a year you'll be amazed how far you've come.", "book": "Morgan Housel — The Psychology of Money"},
        "ko": {"title": "올바른 방향으로 가고 있습니다", "body": "수입이 지출을 초과하고 저축하고 있습니다. 계속하세요. 1년 후 얼마나 멀리 왔는지 놀랄 것입니다.", "book": "Morgan Housel — The Psychology of Money"},
    },
}

for _tip_id, _texts in _TIP_TEXTS.items():
    _ROUTA_SEED.append(_row(
        f"tip_{_tip_id}_title",
        _texts["ru"]["title"], _texts["en"]["title"], _texts["ko"]["title"], "tip"))
    _ROUTA_SEED.append(_row(
        f"tip_{_tip_id}_body",
        _texts["ru"]["body"], _texts["en"]["body"], _texts["ko"]["body"], "tip"))
    _ROUTA_SEED.append(_row(
        f"tip_{_tip_id}_book",
        _texts["ru"]["book"], _texts["en"]["book"], _texts["ko"]["book"], "tip"))


_CATEGORY_SEED: list[dict[str, Any]] = [
    # needs
    _row("cat_housing", "Жильё", "Housing", "주거", "category",
         "Name of a basic need expense category (rent, mortgage, utilities)."),
    _row("cat_food", "Продукты", "Food", "식료품", "category",
         "Name of a basic need expense category (groceries)."),
    _row("cat_transport", "Транспорт", "Transport", "교통", "category",
         "Name of a basic need expense category (public transit, fuel, taxi)."),
    _row("cat_health_wellness", "Здоровье и уход", "Health & wellness", "건강 및 관리", "category",
         "Name of a basic need expense category (medical, sport, self-care)."),
    _row("cat_family_kids", "Семья и дети", "Family & kids", "가족 및 아이", "category",
         "Name of a basic need expense category (family and children expenses)."),
    # wants
    _row("cat_eating_out", "Кафе и рестораны", "Eating out", "외식", "category",
         "Name of a discretionary expense category (restaurants, cafes)."),
    _row("cat_shopping_stuff", "Покупки и вещи", "Shopping & stuff", "쇼핑 및 물건", "category",
         "Name of a discretionary expense category (shopping, goods)."),
    _row("cat_fun_subscriptions", "Развлечения и подписки", "Fun & subscriptions", "여가 및 구독", "category",
         "Name of a discretionary expense category (entertainment, subscriptions)."),
    _row("cat_travel", "Путешествия", "Travel", "여행", "category",
         "Name of a discretionary expense category (trips, travel)."),
    _row("cat_other_expense", "Прочее", "Other", "기타", "category",
         "Name of a discretionary expense category (miscellaneous spending)."),
    _row("cat_uncategorized", "Укажу позже", "Set later", "나중에 지정", "category",
         "Fallback expense category name when the user has not picked a category yet."),
    # goals
    _row("cat_savings_investments", "Сбережения и инвестиции", "Savings & investments", "저축 및 투자", "category",
         "Name of a financial goal category (savings, investments)."),
    _row("cat_debt_repayment", "Погашение долгов", "Debt repayment", "빚 상환", "category",
         "Name of a financial goal category (paying off debt)."),
    _row("cat_education_growth", "Образование и рост", "Education & growth", "교육 및 성장", "category",
         "Name of a financial goal category (education, self-development)."),
    # income
    _row("cat_salary_income", "Зарплата", "Salary", "급여", "category",
         "Name of an income source category (salary)."),
    _row("cat_side_income", "Подработка", "Side income", "부수입", "category",
         "Name of an income source category (side jobs, freelance)."),
    _row("cat_passive_income", "Пассивный доход", "Passive income", "패시브 소득", "category",
         "Name of an income source category (passive income)."),
    _row("cat_other_income", "Прочий доход", "Other income", "기타 수입", "category",
         "Name of an income source category (miscellaneous income)."),
]


def seed() -> int:
    """Idempotently seed Routa-specific keys into the unified glossary."""
    n = glossary.upsert_many(_ROUTA_SEED)
    n += glossary.upsert_many(_CATEGORY_SEED)
    ui_glossary.apply_descriptions(glossary)
    return n
