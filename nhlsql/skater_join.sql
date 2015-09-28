create table skaterstats as select 
	skatsum.nhl_num, skatsum.season, games_played,
	(goals - pp_goals - sh_goals) as es_goals, -- es stats extrapolated from pp, sh, total
	pp_goals, sh_goals, goals,
	(assists - pp_assists - sh_assists) as es_assists,
	pp_assists, sh_assists, assists,
	(points - pp_points - sh_points) as es_points,
	pp_points, sh_points, points,
	team_goals_for, team_pp_goals_for, team_goals_against, team_pp_goals_against, plus_minus,
	minors, majors, misconducts, game_misconducts, matches, penalty_minutes,
	(shots - pp_shots - sh_shots) as es_shots,
	0.1 as es_shot_pct, -- to be updated later
	pp_shots, pp_shot_pct, sh_shots, sh_shot_pct, shots, shot_pct,
	(missed_shots - pp_missed_shots - sh_missed_shots) as es_missed_shots,
	pp_missed_shots, sh_missed_shots, missed_shots,
	(shots_blocked - pp_shots_blocked - sh_shots_blocked) as es_shots_blocked,
	pp_shots_blocked, sh_shots_blocked, shots_blocked,
	(hits - pp_hits - sh_hits) as es_hits,
	pp_hits, sh_hits, hits, 
	(giveaways - pp_giveaways - sh_giveaways) as es_giveaways,
	pp_giveaways, sh_giveaways, giveaways, 
	(takeaways - pp_takeaways - sh_takeaways) as es_takeaways,
	pp_takeaways, sh_takeaways, takeaways,
	(faceoff_wins - pp_faceoff_wins - sh_faceoff_wins) as es_faceoff_wins,
	(faceoff_losses - pp_faceoff_losses - sh_faceoff_losses) as es_faceoff_losses,
	0.1 as es_faceoff_pct, -- to be updated later
	pp_faceoff_wins, pp_faceoff_losses, pp_faceoff_pct,
	sh_faceoff_wins, sh_faceoff_losses, sh_faceoff_pct,
	faceoff_wins, faceoff_losses, faceoff_pct,
	es_toi, pp_toi, sh_toi, toi,
	so_shots, so_goals, so_pct, gw_goals, ot_goals
	from skatsum
		join skatpp
			on skatsum.nhl_num = skatpp.nhl_num
			and skatsum.season = skatpp.season
		join skatsh
			on skatsum.nhl_num = skatsh.nhl_num
			and skatsum.season = skatsh.season
		-- skatso data don't exist before 2006, some observations missing
		left outer join skatso
			on skatsum.nhl_num = skatso.nhl_num
			and skatsum.season = skatso.season
		join skatpm
			on skatsum.nhl_num = skatpm.nhl_num
			and skatsum.season = skatpm.season
		join skatrts
			on skatsum.nhl_num = skatrts.nhl_num
			and skatsum.season = skatrts.season
		join skatpim
			on skatsum.nhl_num = skatpim.nhl_num
			and skatsum.season = skatpim.season
		join skattoi
			on skatsum.nhl_num = skattoi.nhl_num
			and skatsum.season = skattoi.season;
update skaterstats set es_shot_pct = 
	case when es_shots > 0
		then (es_goals::float / es_shots)
		else null
	end;
update skaterstats set es_faceoff_pct =
	case when (es_faceoff_wins + es_faceoff_losses) > 0
		then (es_faceoff_wins::float / (es_faceoff_wins + es_faceoff_losses))
		else null
	end;
drop table skatsum, skatpp, skatsh, skatso, skatpm, skatrts, skatpim, skattoi;
alter table skaterstats add column id serial;
alter table skaterstats add primary key (id);
alter table skaterstats add foreign key (nhl_num) references players;
