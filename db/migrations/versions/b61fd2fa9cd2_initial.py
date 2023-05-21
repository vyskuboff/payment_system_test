"""initial

Revision ID: b61fd2fa9cd2
Revises: c9ce46c19a9c
Create Date: 2023-04-04 15:12:23.451246

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b61fd2fa9cd2'
down_revision = 'c9ce46c19a9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('user_to', sa.BigInteger(), nullable=True),
    sa.Column('user_from', sa.BigInteger(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_from'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['user_to'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'users', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_table('transactions')
    # ### end Alembic commands ###