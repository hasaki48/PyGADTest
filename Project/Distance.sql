use Transport

select 场站管理.场站名称, 项目管理.项目名称, 场站管理.场站纬度, 场站管理.场站经度, 项目管理.项目纬度, 项目管理.项目经度
into Distance
from dbo.场站管理 
cross join dbo.项目管理

