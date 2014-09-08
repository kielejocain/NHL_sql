create table skathold as select nhl_num, season, sum(so_shots) as so_shots, sum(so_goals) as so_goals, sum(game_deciding_goals) as game_deciding_goals from skatso where nhl_num in (select nhl_num from skatso where season = :season group by nhl_num having count(nhl_num) > 1) and season = :season group by nhl_num, season order by nhl_num;
alter table skathold add column so_pct numeric;
update skathold set so_pct = round(cast(so_goals as numeric)/so_shots*100,1);
delete from skatso where nhl_num in (select nhl_num from skatso where season = :season group by nhl_num having count(nhl_num) > 1) and season = :season;
insert into skatso(nhl_num, season, so_shots, so_goals, game_deciding_goals, so_pct) select * from skathold;
drop table skathold;
