"""Personalized financial-literacy tips based on current-period analytics.

Tips are intentionally sharp: each one highlights a specific pain and gives one
actionable step. Books are attached as "where to go deeper".

All user-facing tip text now lives in the unified glossary under the keys
`tip_<id>_title`, `tip_<id>_body`, and `tip_<id>_book`.
"""

from routa.core import catalog, glossary

# role order for priority when multiple tips match
_ROLE_PRIORITY = {
    "expense_gt_income": 0,
    "no_savings": 1,
    "housing_high": 2,
    "debt": 3,
    "wants_gt_needs": 4,
    "goal_low": 5,
    "subscriptions_high": 6,
    "eating_out_gt_food": 7,
    "shopping_high": 8,
    "fun_high": 9,
    "travel_high": 10,
    "family_high": 11,
    "transport_high": 12,
    "health_zero": 13,
    "no_education": 14,
    "gratitude": 15,
    "praise_green": 16,
}


# Every tip: id and condition(report). Translations come from the glossary.
# Conditions receive a normalized report dict:
#   total_income, total_expense, total_need, total_want, total_goal,
#   categories: {key: amount}, currency_groups: raw groups from /api/report.
TIP_CATALOG = [
    {
        "id": "expense_gt_income",
        "condition": lambda r: r["total_expense"] > r["total_income"] and r["total_income"] > 0,
    },
    {
        "id": "no_savings",
        "condition": lambda r: r["total_goal"] == 0 and r["total_income"] > 0,
    },
    {
        "id": "housing_high",
        "condition": lambda r: r["categories"].get("cat_housing", 0) > r["total_income"] * 0.30 and r["total_income"] > 0,
    },
    {
        "id": "debt",
        "condition": lambda r: r["total_debt"] > 0,
    },
    {
        "id": "subscriptions_high",
        "condition": lambda r: r["categories"].get("cat_fun_subscriptions", 0) > r["total_expense"] * 0.10 and r["total_expense"] > 0,
    },
    {
        "id": "eating_out_gt_food",
        "condition": lambda r: r["categories"].get("cat_eating_out", 0) > r["categories"].get("cat_food", 0),
    },
    {
        "id": "shopping_high",
        "condition": lambda r: r["categories"].get("cat_shopping_stuff", 0) > r["total_expense"] * 0.15 and r["total_expense"] > 0,
    },
    {
        "id": "no_education",
        "condition": lambda r: r["categories"].get("cat_education_growth", 0) == 0,
    },
    {
        "id": "fun_high",
        "condition": lambda r: r["categories"].get("cat_fun_subscriptions", 0) > r["total_expense"] * 0.15 and r["total_expense"] > 0,
    },
    {
        "id": "transport_high",
        "condition": lambda r: r["categories"].get("cat_transport", 0) > r["total_expense"] * 0.15 and r["total_expense"] > 0,
    },
    {
        "id": "health_zero",
        "condition": lambda r: r["categories"].get("cat_health_wellness", 0) == 0 and r["total_expense"] > 0,
    },
    {
        "id": "income_up_savings_flat",
        "condition": lambda r: False,  # requires trend data; disabled until trend analytics built
    },
    {
        "id": "net_positive_streak",
        "condition": lambda r: r["total_income"] > r["total_expense"] and r["total_goal"] > 0,
    },
    {
        "id": "travel_high",
        "condition": lambda r: r["categories"].get("cat_travel", 0) > r["total_income"] * 0.20 and r["total_income"] > 0,
    },
    {
        "id": "family_high",
        "condition": lambda r: r["categories"].get("cat_family_kids", 0) > r["total_expense"] * 0.25 and r["total_expense"] > 0,
    },
    {
        "id": "wants_gt_needs",
        "condition": lambda r: r["total_want"] > r["total_need"] and r["total_need"] > 0,
    },
    {
        "id": "goal_low",
        "condition": lambda r: r["total_goal"] < r["total_income"] * 0.10 and r["total_income"] > 0,
    },
    {
        "id": "mindful_checkout",
        "condition": lambda r: False,  # fallback only
    },
    {
        "id": "first_week",
        "condition": lambda r: False,  # requires user age; shown manually for new users
    },
    {
        "id": "irregular_entries",
        "condition": lambda r: False,  # requires last-entry age; disabled for now
    },
    {
        "id": "gratitude",
        "condition": lambda r: r["total_want"] > r["total_need"] * 0.5 and r["total_need"] > 0,
    },
    {
        "id": "praise_green",
        "condition": lambda r: r["total_income"] > r["total_expense"] and r["total_want"] <= r["total_need"],
    },
]


def _normalize_report(report_groups: list[dict], total_debt: float = 0.0) -> dict:
    """Aggregate multi-currency report groups into a single analysis dict."""
    total_income = sum(g.get("income", 0) for g in report_groups)
    total_expense = sum(g.get("expense", 0) for g in report_groups)
    categories: dict[str, float] = {}
    labels: dict[str, str] = {}
    for g in report_groups:
        for e in g.get("top_expenses", []):
            key = e.get("key", "")
            if key:
                categories[key] = categories.get(key, 0.0) + e.get("amount", 0)
                labels[key] = e.get("label", key)
        for i in g.get("incomes", []):
            key = i.get("key", "")
            if key:
                categories[key] = categories.get(key, 0.0) + i.get("amount", 0)
                labels[key] = i.get("label", key)

    # role totals from canonical categories
    total_need = total_want = total_goal = 0.0
    for key, amount in categories.items():
        # strip tenant-specific prefix if any; canon keys start with cat_
        base_key = key
        if not base_key.startswith("cat_"):
            continue
        # find canonical account name by key
        name = None
        for n, meta in catalog.CANON.items():
            if catalog.canon_key(n) == base_key:
                name = n
                break
        if not name:
            continue
        role = catalog.role(name)
        if role == "need":
            total_need += amount
        elif role == "want":
            total_want += amount
        elif role == "goal":
            total_goal += amount

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "total_need": total_need,
        "total_want": total_want,
        "total_goal": total_goal,
        "total_debt": total_debt,
        "categories": categories,
        "category_labels": labels,
        "currency_groups": report_groups,
    }


def _tip_text(tip_id: str, lang: str = "ru") -> dict:
    """Load a single tip's title/body/book from the glossary."""
    return {
        "id": tip_id,
        "title": glossary.t(f"tip_{tip_id}_title", lang),
        "body": glossary.t(f"tip_{tip_id}_body", lang),
        "book": glossary.t(f"tip_{tip_id}_book", lang),
    }


def select_tip(report_groups: list[dict], lang: str = "ru",
               total_debt: float = 0.0) -> dict:
    """Pick the highest-priority matching tip for the current period."""
    r = _normalize_report(report_groups, total_debt=total_debt)
    matches = []
    for tip in TIP_CATALOG:
        try:
            if tip["condition"](r):
                priority = _ROLE_PRIORITY.get(tip["id"], 100)
                matches.append((priority, tip))
        except Exception:
            continue
    if not matches:
        # fallback: mindful checkout
        mindful = next(t for t in TIP_CATALOG if t["id"] == "mindful_checkout")
        matches.append((1000, mindful))
    matches.sort(key=lambda x: x[0])
    tip = matches[0][1]
    return _tip_text(tip["id"], lang)


def all_tips(lang: str = "ru") -> list[dict]:
    """Library of all financial-literacy tips."""
    return [_tip_text(tip["id"], lang) for tip in TIP_CATALOG]
