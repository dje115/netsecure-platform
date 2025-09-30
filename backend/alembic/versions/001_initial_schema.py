"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-09-30 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('openai_api_key', sa.String(), nullable=True),
        sa.Column('anthropic_api_key', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create scan_sessions table
    op.create_table(
        'scan_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('target_range', sa.String(), nullable=False),
        sa.Column('scan_type', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('current_phase', sa.Integer(), nullable=True),
        sa.Column('total_phases', sa.Integer(), nullable=True),
        sa.Column('progress', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('phases_enabled', sa.JSON(), nullable=True),
        sa.Column('tools_config', sa.JSON(), nullable=True),
        sa.Column('devices_found', sa.Integer(), nullable=True),
        sa.Column('vulnerabilities_found', sa.Integer(), nullable=True),
        sa.Column('hvt_count', sa.Integer(), nullable=True),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scan_sessions_id'), 'scan_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_scan_sessions_name'), 'scan_sessions', ['name'], unique=False)

    # Create scan_logs table
    op.create_table(
        'scan_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scan_session_id', sa.Integer(), nullable=True),
        sa.Column('phase', sa.Integer(), nullable=True),
        sa.Column('phase_name', sa.String(), nullable=True),
        sa.Column('tool_name', sa.String(), nullable=True),
        sa.Column('log_level', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('output', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['scan_session_id'], ['scan_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scan_logs_id'), 'scan_logs', ['id'], unique=False)

    # Create devices table
    op.create_table(
        'devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scan_session_id', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('mac_address', sa.String(), nullable=True),
        sa.Column('hostname', sa.String(), nullable=True),
        sa.Column('vendor', sa.String(), nullable=True),
        sa.Column('os_name', sa.String(), nullable=True),
        sa.Column('os_version', sa.String(), nullable=True),
        sa.Column('os_family', sa.String(), nullable=True),
        sa.Column('device_type', sa.String(), nullable=True),
        sa.Column('is_hvt', sa.Boolean(), nullable=True),
        sa.Column('hvt_type', sa.String(), nullable=True),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('risk_level', sa.String(), nullable=True),
        sa.Column('first_seen', sa.DateTime(), nullable=True),
        sa.Column('last_seen', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('ai_classification', sa.JSON(), nullable=True),
        sa.Column('ai_recommendations', sa.Text(), nullable=True),
        sa.Column('ai_attack_surface', sa.JSON(), nullable=True),
        sa.Column('nmap_data', sa.JSON(), nullable=True),
        sa.Column('additional_data', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['scan_session_id'], ['scan_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_devices_id'), 'devices', ['id'], unique=False)
    op.create_index(op.f('ix_devices_ip_address'), 'devices', ['ip_address'], unique=False)

    # Create ports table
    op.create_table(
        'ports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('port_number', sa.Integer(), nullable=False),
        sa.Column('protocol', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('service_name', sa.String(), nullable=True),
        sa.Column('service_version', sa.String(), nullable=True),
        sa.Column('service_product', sa.String(), nullable=True),
        sa.Column('banner', sa.Text(), nullable=True),
        sa.Column('script_output', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ports_id'), 'ports', ['id'], unique=False)

    # Create services table
    op.create_table(
        'services',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('service_type', sa.String(), nullable=False),
        sa.Column('service_name', sa.String(), nullable=True),
        sa.Column('port', sa.Integer(), nullable=True),
        sa.Column('version', sa.String(), nullable=True),
        sa.Column('enumeration_data', sa.JSON(), nullable=True),
        sa.Column('configuration', sa.JSON(), nullable=True),
        sa.Column('users_found', sa.JSON(), nullable=True),
        sa.Column('shares_found', sa.JSON(), nullable=True),
        sa.Column('is_vulnerable', sa.Boolean(), nullable=True),
        sa.Column('weak_config', sa.Boolean(), nullable=True),
        sa.Column('default_creds', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=False)

    # Create vulnerabilities table
    op.create_table(
        'vulnerabilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('cve_id', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('cvss_score', sa.Float(), nullable=True),
        sa.Column('cvss_vector', sa.String(), nullable=True),
        sa.Column('cvss_version', sa.String(), nullable=True),
        sa.Column('exploitable', sa.Boolean(), nullable=True),
        sa.Column('exploit_available', sa.Boolean(), nullable=True),
        sa.Column('exploit_db_id', sa.String(), nullable=True),
        sa.Column('metasploit_module', sa.String(), nullable=True),
        sa.Column('affected_service', sa.String(), nullable=True),
        sa.Column('affected_port', sa.Integer(), nullable=True),
        sa.Column('affected_component', sa.String(), nullable=True),
        sa.Column('remediation', sa.Text(), nullable=True),
        sa.Column('patch_available', sa.Boolean(), nullable=True),
        sa.Column('patch_info', sa.Text(), nullable=True),
        sa.Column('detection_method', sa.String(), nullable=True),
        sa.Column('detection_tool', sa.String(), nullable=True),
        sa.Column('confidence', sa.String(), nullable=True),
        sa.Column('false_positive', sa.Boolean(), nullable=True),
        sa.Column('references', sa.JSON(), nullable=True),
        sa.Column('cwe_ids', sa.JSON(), nullable=True),
        sa.Column('validated', sa.Boolean(), nullable=True),
        sa.Column('validation_result', sa.String(), nullable=True),
        sa.Column('validation_date', sa.DateTime(), nullable=True),
        sa.Column('discovered_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vulnerabilities_cve_id'), 'vulnerabilities', ['cve_id'], unique=False)
    op.create_index(op.f('ix_vulnerabilities_id'), 'vulnerabilities', ['id'], unique=False)

    # Create attack_paths table
    op.create_table(
        'attack_paths',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('path_type', sa.String(), nullable=False),
        sa.Column('source_device', sa.String(), nullable=True),
        sa.Column('target_device', sa.String(), nullable=True),
        sa.Column('attack_vector', sa.String(), nullable=True),
        sa.Column('technique_id', sa.String(), nullable=True),
        sa.Column('technique_name', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('requirements', sa.JSON(), nullable=True),
        sa.Column('credentials_needed', sa.JSON(), nullable=True),
        sa.Column('impact_level', sa.String(), nullable=True),
        sa.Column('potential_damage', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(), nullable=True),
        sa.Column('detection_difficulty', sa.String(), nullable=True),
        sa.Column('validated', sa.Boolean(), nullable=True),
        sa.Column('validation_result', sa.Text(), nullable=True),
        sa.Column('discovered_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attack_paths_id'), 'attack_paths', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_attack_paths_id'), table_name='attack_paths')
    op.drop_table('attack_paths')
    op.drop_index(op.f('ix_vulnerabilities_id'), table_name='vulnerabilities')
    op.drop_index(op.f('ix_vulnerabilities_cve_id'), table_name='vulnerabilities')
    op.drop_table('vulnerabilities')
    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.drop_table('services')
    op.drop_index(op.f('ix_ports_id'), table_name='ports')
    op.drop_table('ports')
    op.drop_index(op.f('ix_devices_ip_address'), table_name='devices')
    op.drop_index(op.f('ix_devices_id'), table_name='devices')
    op.drop_table('devices')
    op.drop_index(op.f('ix_scan_logs_id'), table_name='scan_logs')
    op.drop_table('scan_logs')
    op.drop_index(op.f('ix_scan_sessions_name'), table_name='scan_sessions')
    op.drop_index(op.f('ix_scan_sessions_id'), table_name='scan_sessions')
    op.drop_table('scan_sessions')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

