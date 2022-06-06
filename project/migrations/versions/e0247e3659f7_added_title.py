"""added_title

Revision ID: e0247e3659f7
Revises: 8e5574badfe6
Create Date: 2022-06-03 17:58:48.772647

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'e0247e3659f7'
down_revision = '8e5574badfe6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=256), server_default="NoTitle", nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notes', 'title')
    # ### end Alembic commands ###