"""first migration

Revision ID: 42d8bc2d4864
Revises: 
Create Date: 2024-08-14 12:47:56.932741

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '42d8bc2d4864'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

roles_table = sa.table(
    'roles',
    sa.column('role_id', sa.String(length=36)),
    sa.column('role_name', sa.String(length=50)),
    sa.column('description', sa.String(length=100))
)

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('persons',
    sa.Column('person_id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('person_id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('roles',
    sa.Column('role_id', sa.String(length=36), nullable=False),
    sa.Column('role_name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('role_id'),
    sa.UniqueConstraint('role_name')
    )
    # Inserting roles data
    op.bulk_insert(
        roles_table,
        [
            {"role_id": str(uuid.uuid4()), "role_name": "user", "description": "Standard user with usage permissions"},
            {"role_id": str(uuid.uuid4()), "role_name": "admin", "description": "Administrator with business permissions"},
        ]
    )
    op.create_table('accounts',
    sa.Column('account_id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('photo', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('role_id', sa.String(length=36), nullable=False),
    sa.Column('person_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['persons.person_id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.role_id'], ),
    sa.PrimaryKeyConstraint('account_id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accounts')
    op.drop_table('roles')
    op.drop_table('persons')
    # ### end Alembic commands ###
