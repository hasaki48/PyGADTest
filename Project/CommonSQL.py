CheckExists = """
use Transport
-- 删除WeekPlan表如果其存在
if exists (
    select *
from sys.tables
    join sys.schemas
    on sys.tables.schema_id = sys.schemas.schema_id
where sys.schemas.name = 'dbo'
    and sys.tables.name = '{TableName}'
)
    drop table dbo.{TableName}
"""
