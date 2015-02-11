create table goalhold as select nhl_num, season, sum(so_wins) as so_wins, sum(so_losses) as so_losses, sum(so_shots_against) as so_shots_against, sum(so_goals_against) as so_goals_against from goalso where nhl_num in (select nhl_num from goalso where season = :season group by nhl_num having count(nhl_num) > 1) and season = :season group by nhl_num, season;
delete from goalso where nhl_num in (select nhl_num from goalso where season = :season group by nhl_num having count(nhl_num) > 1) and season = :season;
insert into goalso(nhl_num, season, so_wins, so_losses, so_shots_against, so_goals_against) select * from goalhold;
drop table goalhold;
