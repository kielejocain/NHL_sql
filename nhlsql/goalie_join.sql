create table goaliestats as select
	goalsum.nhl_num, goalsum.season, games_played,
	games_started,
	wins, losses, ties, ot_losses, shutouts,
	es_shots_against, pp_shots_against, sh_shots_against, shots_against,
	es_goals_against, pp_goals_against, sh_goals_against, goals_against,
	es_saves, pp_saves, sh_saves, saves,
	es_save_pct, pp_save_pct, sh_save_pct, save_pct,
	gaa, toi,
	so_wins, so_losses, so_shots_against, so_goals_against, so_saves, so_save_pct
	from goalsum
		join goales
			on goalsum.nhl_num = goales.nhl_num
			and goalsum.season = goales.season
		join goalpp
			on goalsum.nhl_num = goalpp.nhl_num
			and goalsum.season = goalpp.season
		join goalsh
			on goalsum.nhl_num = goalsh.nhl_num
			and goalsum.season = goalsh.season
		-- goalso data don't exist before 2006, some observations missing
		left outer join goalso
			on goalsum.nhl_num = goalso.nhl_num
			and goalsum.season = goalso.season;
drop table goalsum, goales, goalpp, goalsh, goalso;
alter table goaliestats add column id serial;
alter table goaliestats add primary key (id);
alter table goaliestats add foreign key (nhl_num) references players;
