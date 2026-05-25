MAX_NAME_LEN = 124
MAX_PJ_NAME_LEN = 200
MAX_STAT_LEN = 6

PAGINATION_PAGE_SIZE = 12
SKILL_AUTOCOMPLETE_LIMIT = 10

GITHUB_URL_PREFIX = "https://github.com/"

class ProjectStatus:
    OPEN = "open"
    CLOSED = "closed"


STATUS_CHOICES = [
    (ProjectStatus.OPEN, "Открыт"),
    (ProjectStatus.CLOSED, "Завершен"),
]