from datetime import datetime

import bcrypt
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "637f05a790b9"
down_revision = "1da2bbc8a66e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    now = datetime.now()

    user_table = sa.table(
        "users",
        sa.column("name", sa.String),
        sa.column("username", sa.String),
        sa.column("password", sa.String),
        sa.column("created_at", sa.DateTime),
    )

    op.bulk_insert(
        user_table,
        [
            {
                "name": "Admin",
                "username": "admin",
                "password": bcrypt.hashpw(
                    "admin123".encode("utf-8"), bcrypt.gensalt(12)
                ),
                "created_at": now,
            }
        ],
    )

    log_table = sa.table(
        "logs",
        sa.column("category", sa.String),
        sa.column("color", sa.String),
        sa.column("status", sa.String),
        sa.column("created_at", sa.DateTime),
        sa.column("user_id", sa.Integer),
    )

    colors = ["blue", "green", "yellow", "white", "black"]
    categories = ["flammable", "non-flammable", "recyclable"]
    statuses = ["success", "error"]

    logs = []
    for color in colors:
        for category in categories:
            for status in statuses:
                logs.append(
                    {
                        "category": category,
                        "color": color,
                        "status": status,
                        "created_at": now,
                        "user_id": 1,
                    }
                )

    op.bulk_insert(log_table, logs)

    dashboard_table = sa.table(
        "dashboards",
        sa.column("image", sa.String),
        sa.column("label", sa.Integer),
        sa.column("confidence", sa.Float),
        sa.column("created_at", sa.DateTime),
        sa.column("user_id", sa.Integer),
    )

    op.bulk_insert(
        dashboard_table,
        [
            {
                "image": "sample.png",
                "label": 1,
                "confidence": 0.95,
                "created_at": now,
                "user_id": 1,
            }
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM dashboards")
    op.execute("DELETE FROM logs")
    op.execute("DELETE FROM users WHERE username = 'admin'")
