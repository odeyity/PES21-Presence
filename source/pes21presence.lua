local m = {}
local isML = false
local isTraining = false

local exhib_same_league_tid

local function get_common_lib(ctx)
    return ctx.common_lib or _empty
end




function m.data_ready(ctx, filename)
    local matchLoad = string.match(filename, "common\\script\\flow\\Match\\MatchSetup.json")
    if matchLoad then
        io.output(MatchState)
        local stateW = io.open(MatchState, "w")
        io.write("game")
        io.close(stateW)
    end
    local goal = string.match(filename, "goal\\cut_data\\goal_celebrate_(%d+)")
    local owngoal = string.match(filename, "common\\demo\\fixdemo\\goal\\cut_data\\goal_cmnCam_outM00.fdc")
    local cam = string.match(filename, "common\\bg\\model\\bg\\bill\\p_global\\movie\\bill_p_global.usm")
    if goal or owngoal or cam then
        local homeS = "homescore: " .. tostring(match.stats()["home_score"]) .. "\n"
        local awayS = "awayscore: " .. tostring(match.stats()["away_score"]) .. "\n"
        io.output(MatchScore)
        local scoreW = io.open(MatchScore, "w")
        scoreW:write(homeS)
        scoreW:write(awayS)
        io.close(scoreW)
    end
    local topmenu = string.match(filename, "common\\menu\\general\\topModeSelectDMM.bin")
    if topmenu then
        io.output(MatchState)
        local stateW = io.open(MatchState, "w")
        io.write("menu")
        io.close(stateW)
        local infoW = io.open(MatchInfo, "w")
        io.output(MatchInfo)
        io.write("")
        io.close(infoW)
        local scoreW = io.open(MatchScore, "w")
        io.output(MatchScore)
        io.write("")
        io.close(scoreW)
    end
    local mlmenu = string.match(filename, "common\\script\\flow\\ML\\MLMainManu.json")
    if mlmenu then
        io.output(MatchState)
        local stateW = io.open(MatchState, "w")
        io.write("ml")
        io.close(stateW)
        local isML = true
    end

    local training = string.match(filename, "common\\script\\flow\\Match\\MatchTrainingMatchMenu.json")
    if training then
        io.output(MatchState)
        local stateW = io.open(MatchState, "w")
        io.write("training")
        io.close(stateW)
        local isTraining = true
    end
end

function m.teams(ctx)
    local comp = "comp: " .. tostring(ctx.tournament_id) .. "\n"
    local homeT = "hometeam: " .. tostring(ctx.home_team) .. "\n"
    local awayT = "awayteam: " .. tostring(ctx.away_team) .. "\n"
    local leg = "leg: " .. tostring(ctx.match_leg) .. "\n"
    local special = "special: " .. tostring(ctx.match_info) .. "\n"
    local scoreboard = "scoreboard: " .. get_common_lib(ctx).tid_same_league(ctx.home_team, ctx.away_team)

    io.output(MatchInfo)
    local infoW = io.open(MatchInfo, "w")
    log("writing info")
    io.write(comp)
    io.write(homeT)
    io.write(awayT)
    io.write(leg)
    io.write(special)
    io.write(scoreboard)
    log("closing file")
    io.close(infoW)

    if isML == false and isTraining == false then
        io.output(MatchState)
        local stateW = io.open(MatchState, "w")
        io.write("game")
        io.close(stateW)
    end
end

function m.init(ctx)
    MatchInfo = ctx.sider_dir .. "modules/PES21-Presence/info/matchinfo.txt"
    MatchScore = ctx.sider_dir .. "modules/PES21-Presence/info/matchscore.txt"
    MatchState = ctx.sider_dir .. "modules/PES21-Presence/info/matchstate.txt"
    SiderDir = "sider_dir.txt"

    PythonFile = 'cmd /c start "" /min "' .. ctx.sider_dir .. 'modules\\PES21-Presence\\python\\pes21presence.exe"'

    local infoW = io.open(MatchInfo, "w")
    io.output(MatchInfo)
    io.write("")
    io.close(infoW)

    local scoreW = io.open(MatchScore, "w")
    io.output(MatchScore)
    io.write("")
    io.close(scoreW)

    local stateW = io.open(MatchState, "w")
    io.output(MatchState)
    io.write("menu")
    io.close(stateW)

    local sider_dirW = io.open(SiderDir, "w")
    io.output(SiderDir)
    io.write(ctx.sider_dir)
    io.close(sider_dirW)


    log("Activated.")
    log("Launching Python script...")
    io.popen(PythonFile)
    log("Launched.")
    ctx.register("set_teams", m.teams)
    ctx.register("livecpk_data_ready", m.data_ready)
end

return m
