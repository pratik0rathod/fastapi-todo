"""updated columns

Revision ID: b8dd7a44afa3
Revises: f143bd393874
Create Date: 2024-04-10 14:44:22.014226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8dd7a44afa3'
down_revision: Union[str, None] = 'f143bd393874'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
