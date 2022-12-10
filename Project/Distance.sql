use Transport

select 场站管理.场站名称, 项目管理.项目名称, 场站管理.场站纬度, 场站管理.场站经度, 项目管理.项目纬度, 项目管理.项目经度, 6378.138 * 2 * ASIN(
		SQRT(
			POWER(
				SIN( ( Distance.[场站纬度] * PI( ) / 180 - Distance.[项目纬度] * PI( ) / 180 ) / 2 ),
				2 
				) + COS( Distance.[场站纬度] * PI( ) / 180 ) * COS( Distance.[项目纬度] * PI( ) / 180 ) * POWER(
				SIN( ( Distance.[场站经度] * PI( ) / 180 - Distance.[项目经度] * PI( ) / 180 ) / 2 ),
				2 
			) 
		) 
	) as 距离
into Distance
from dbo.场站管理 
cross join dbo.项目管理

-- select
--     Distance.[场站名称],
--     Distance.[项目名称],
--     Distance.[场站纬度],
--     Distance.[场站经度],
--     Distance.[项目纬度],
--     Distance.[项目经度],
--     6378.138 * 2 * ASIN(
-- 		SQRT(
-- 			POWER(
-- 				SIN( ( Distance.[场站纬度] * PI( ) / 180 - Distance.[项目纬度] * PI( ) / 180 ) / 2 ),
-- 				2 
-- 				) + COS( Distance.[场站纬度] * PI( ) / 180 ) * COS( Distance.[项目纬度] * PI( ) / 180 ) * POWER(
-- 				SIN( ( Distance.[场站经度] * PI( ) / 180 - Distance.[项目经度] * PI( ) / 180 ) / 2 ),
-- 				2 
-- 			) 
-- 		) 
-- 	) as 距离
-- from
--     dbo.Distance
--     inner join dbo.WeekPlan on Distance.项目名称 = WeekPlan.项目名称