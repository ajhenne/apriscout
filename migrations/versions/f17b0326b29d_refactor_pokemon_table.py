"""refactor pokemon table

Revision ID: f17b0326b29d
Revises: ce5c9ea3e84c
Create Date: 2025-07-19 19:38:37.624107

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f17b0326b29d"
down_revision = "ce5c9ea3e84c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokemon", schema=None) as batch_op:
        batch_op.add_column(sa.Column("evolves_from", sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column("evolution_chain_id", sa.Integer(), nullable=True),
        )
        batch_op.add_column(sa.Column("female_difference", sa.Integer(), nullable=True))
        batch_op.alter_column(
            "is_starter",
            existing_type=sa.INTEGER(),
            type_=sa.Boolean(),
            existing_nullable=True,
        )
        batch_op.drop_column("dex_num")
        batch_op.drop_column("type1")
        batch_op.drop_column("is_legendary")
        batch_op.drop_column("type2")
        batch_op.drop_column("form_id")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokemon", schema=None) as batch_op:
        batch_op.add_column(sa.Column("form_id", sa.VARCHAR(length=10), nullable=True))
        batch_op.add_column(sa.Column("type2", sa.VARCHAR(length=10), nullable=True))
        batch_op.add_column(sa.Column("is_legendary", sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column("type1", sa.VARCHAR(length=10), nullable=True))
        batch_op.add_column(sa.Column("dex_num", sa.INTEGER(), nullable=True))
        batch_op.alter_column(
            "is_starter",
            existing_type=sa.Boolean(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )
        batch_op.drop_column("female_difference")
        batch_op.drop_column("evolution_chain_id")
        batch_op.drop_column("evolves_from")

    # ### end Alembic commands ###
