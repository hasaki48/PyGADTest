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
go
-- 定义全过程都会用到的变量
declare @BeginChar varchar(10)
declare @EndChar varchar(10)

select @BeginChar = '2021-06-01',
    @EndChar = '2021-08-01'

-- 选择开始时间或者结束时间在给定区间的生产计划
begin
    declare @BeginDate date
    declare @EndDate date

    select
        @BeginDate = CAST(@BeginChar as date),
        @EndDate = CAST(@EndChar as date)

    select 项目名称, 物料生产位置, 物料料性, 料性ID, 物料方量, 开始日期, 结束日期
    into WeekPlan
    from dbo.生产计划
    where 
    (开始日期 between @BeginDate and @EndDate) or
        (结束日期 between @BeginDate and @EndDate)
end
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
    select @StartWeek = DATENAME(WEEK,@BeginChar), @StartWeekDay = DATEPART(DW,@BeginChar),
        @EndWeek = DATENAME(WEEK,@EndChar), @EndWeekDay = DATEPART(DW,@EndChar)
    declare @LoopSum int
    -- 有多少周就循环多少次
    set @LoopSum = CAST(@EndWeek as int) - CAST(@StartWeek as int)
    declare @LoopCount int
    -- 循环计数器
    set @LoopCount = 0
    declare @StartDateOfWeek date
    declare @EndDateofWeek date
    while @LoopCount <= @LoopSum
    begin
        if(@LoopCount = 0)  -- 如果是第一周
        begin
            set @StartDateOfWeek = dateadd(day,0,@BeginChar)
            -- 这周的开始时间取区间开始日期
            set @EndDateofWeek = dateadd(day,7 - CAST(@StartWeekDay as int),@BeginChar)
            -- 这周的结束时间取周末
            select @LoopCount = @LoopCount + 1
            -- 计数器加一
            select *, 周开始时间=@StartDateOfWeek, 周结束时间=@EndDateofWeek, DATEDIFF(d,@StartDateOfWeek,@EndDateofWeek) as 持续时间,
                物料方量/DATEDIFF(d,开始日期,结束日期) as 每天方量
            from WeekPlan
            -- 查询结果
            continue
        end
        if(@LoopCount = @LoopSum)  -- 如果是最后一周
        begin
            set @StartDateOfWeek = dateadd(day,@LoopCount*7-(CAST(@StartWeekDay as int)-1),@BeginChar)
            -- 这周的开始时间正常的取周一
            set @EndDateofWeek = dateadd(day,0,@EndChar)
            -- 这周的结束时间取区间最后日期
            select @LoopCount = @LoopCount + 1
            select *, 周开始时间=@StartDateOfWeek, 周结束时间=@EndDateofWeek, DATEDIFF(d,@StartDateOfWeek,@EndDateofWeek) as 持续时间,
                物料方量/DATEDIFF(d,开始日期,结束日期) as 每天方量
            from WeekPlan
            continue
        end
        -- 其余无特殊情况
        set @StartDateOfWeek = dateadd(day,@LoopCount*7-(CAST(@StartWeekDay as int)-1),@BeginChar)
        -- 通过一点小小的计算，取周一
        set @EndDateofWeek = dateadd(day,(@LoopCount+1)*7-(CAST(@StartWeekDay as int)),@BeginChar)
        -- 取周末
        select @LoopCount = @LoopCount + 1
        select *, 周开始时间=@StartDateOfWeek, 周结束时间=@EndDateofWeek, DATEDIFF(d,@StartDateOfWeek,@EndDateofWeek) as 持续时间,
            物料方量/DATEDIFF(d,开始日期,结束日期) as 每天方量
        from WeekPlan
    end
end
