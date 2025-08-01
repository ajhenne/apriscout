"""remove is_female pokemon table

Revision ID: 5543adceba6a
Revises: f17b0326b29d
Create Date: 2025-07-19 19:42:27.339899

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5543adceba6a"
down_revision = "f17b0326b29d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokemon", schema=None) as batch_op:
        batch_op.drop_column("is_female")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokemon", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_female", sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
