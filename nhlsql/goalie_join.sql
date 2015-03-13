create table goaliestats as select goalsum.nhl_num, goalsum.season, team, team2, team3, games_played, games_started, wins, losses, ties, overtime_losses, shots_against, goals_against, gaa, saves, save_pct, shutouts, goals, assists, penalty_minutes, toi, ps_attempts, ps_goals_against, ps_saves, so_wins, so_losses, so_shots_against, so_goals_against, es_shots_against, es_goals_against, es_saves, es_save_pct, pp_shots_against, pp_goals_against, pp_saves, pp_save_pct, sh_shots_against, sh_goals_against, sh_saves, sh_save_pct from goalsum left outer join goalps on goalsum.nhl_num = goalps.nhl_num and goalsum.season = goalps.season left outer join goalso on goalsum.nhl_num = goalso.nhl_num and goalsum.season = goalso.season left outer join goalst on goalsum.nhl_num = goalst.nhl_num and goalsum.season = goalst.season;
drop table goalsum, goalps, goalso, goalst;
alter table goaliestats add column id serial;
update goaliestats set id default;
alter table goaliestats add primary key (id);
alter table goaliestats add foreign key (nhl_num) references goalies;