CheckExists = """
use Transport
-- 删除WeekPlan表如果其存在
if exists (
    select *
from sys.tables
    join sys.schemas
    on sys.tables.schema_id = sys.schemas.schema_id
where sys.schemas.name = 'dbo'
    and sys.tables.name = 'WeekPlan'
)
    drop table dbo.WeekPlan
"""
SelInto = """
-- 选择开始时间或者结束时间在给定区间的生产计划
begin
    declare @BeginDate date
    declare @EndDate date

    select
        @BeginDate = CAST({BeginChar} as date),
        @EndDate = CAST({EndChar} as date)

    select 项目名称, 物料生产位置, 物料料性, 料性ID, 物料方量, 开始日期, 结束日期
    into WeekPlan
    from dbo.生产计划
    where 
    (开始日期 between @BeginDate and @EndDate) or
        (结束日期 between @BeginDate and @EndDate)
end
"""
SelWeek = """
set datefirst 1
begin
    -- select *, DATEDIFF(d,开始日期,结束日期) as 持续时间,
    --     物料方量/DATEDIFF(d,开始日期,结束日期) as 每天方量
    -- from WeekPlan
    declare @StartWeekDay varchar(10)
    -- 开始于周几
    declare @EndWeekDay varchar(10)
    -- 结束于周几
    declare @StartWeek varchar(10)
    -- 开始于第几周
    declare @EndWeek varchar(10)
    -- 结束于第几周
    select @StartWeek = DATENAME(WEEK,{BeginChar}), @StartWeekDay = DATEPART(DW,{BeginChar}),
        @EndWeek = DATENAME(WEEK,{EndChar}), @EndWeekDay = DATEPART(DW,{EndChar})
end
"""
SQL = """
select *, 周开始时间={StartDateOfWeek}, 周结束时间={EndDateOfWeek}, DATEDIFF(d,{StartDateOfWeek},{EndDateOfWeek}) as 持续时间,
                物料方量/DATEDIFF(d,开始日期,结束日期) as 每天方量
            from WeekPlan
"""
