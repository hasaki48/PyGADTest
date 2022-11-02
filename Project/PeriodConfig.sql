-- 删除SomeDays表如果其存在
if exists (
    select *
from sys.tables
    join sys.schemas
    on sys.tables.schema_id = sys.schemas.schema_id
where sys.schemas.name = 'dbo'
    and sys.tables.name = 'SomeDays'
)
    drop table dbo.SomeDays
go

-- 选择开始时间或者结束时间在给定区间的生产计划
begin
    declare @BeginDate date
    declare @EndDate date
    declare @BeginChar varchar(10)
    declare @EndChar varchar(10)

    select @BeginChar = '2021-05-01',
        @EndChar = '2021-06-01'

    select
        @BeginDate = CAST(@BeginChar as date),
        @EndDate = CAST(@EndChar as date)

    select *
    into SomeDays
    from dbo.生产计划
    where 
    (开始日期 between @BeginDate and @EndDate) or
        (结束日期 between @BeginDate and @EndDate)
end

select *
from SomeDays
