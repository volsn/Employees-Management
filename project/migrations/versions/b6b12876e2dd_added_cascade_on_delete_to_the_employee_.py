"""Added cascade on delete to the employee model.

Revision ID: b6b12876e2dd
Revises: eaf20d8fbe4b
Create Date: 2021-05-09 19:22:57.618899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6b12876e2dd'
down_revision = 'eaf20d8fbe4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('employee_department_id_fkey', 'employee', type_='foreignkey')
    op.create_foreign_key(None, 'employee', 'department', ['department_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.create_foreign_key('employee_department_id_fkey', 'employee', 'department', ['department_id'], ['id'])
    # ### end Alembic commands ###
