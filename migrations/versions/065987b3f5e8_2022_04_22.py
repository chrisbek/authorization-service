"""2022-04-22

Revision ID: 065987b3f5e8
Revises: 
Create Date: 2022-04-22 23:52:17.076103

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '065987b3f5e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authorizationdata',
    sa.Column('access_token', mysql.LONGTEXT(), nullable=True),
    sa.Column('refresh_token', mysql.LONGTEXT(), nullable=True),
    sa.Column('id_token', mysql.LONGTEXT(), nullable=True),
    sa.Column('code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('client',
    sa.Column('client_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('client_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('client_secret', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('client_id'),
    sa.UniqueConstraint('client_name')
    )
    op.create_table('redirect_uris',
    sa.Column('redirect_uri', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('redirect_uri')
    )
    op.create_table('user',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('external_identifier', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('external_identifier')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('redirect_uris')
    op.drop_table('client')
    op.drop_table('authorizationdata')
    # ### end Alembic commands ###