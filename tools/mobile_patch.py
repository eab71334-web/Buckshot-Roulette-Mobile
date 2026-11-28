"""
Patches the project for mobile export by replacing Steam-dependent scripts
with no-op stubs. Run before Godot export on the build machine.
"""

# ── Steam.gd → no-op stub ─────────────────────────────────────────────────────
STEAM_STUB = '''\
extends Node

# Mobile stub — GodotSteam native plugin is PC-only.
# All Steam calls are silent no-ops; using_steam is always false on mobile.

var appid : int = 0
const PACKET_READ_LIMIT: int = 32

var DATA
var LOBBY_ID = 0
var LOBBY_MEMBERS = []
var USER_ID_LIST_TO_IGNORE : Array[int]
var LOBBY_INVITE_ARG = false
var STEAM_ID = 0
var STEAM_NAME = "Player"
var ONLINE = false
var HOST_ID = 0

var is_lobby_friends_only = true
var lobby_player_limit = 4

func _ready():
\tprocess_priority = 1000
\tset_process_internal(true)
\tprint("Steam stub active (mobile build)")

func _process(_delta: float) -> void:
\tpass

func InitializeSteam():
\tpass
'''

with open("scripts/Steam.gd", "w", encoding="utf-8") as f:
    f.write(STEAM_STUB)
print("Patched scripts/Steam.gd → mobile stub")

# ── LeaderboardManager.gd → full no-op stub ───────────────────────────────────
# This file has Steam.* calls at class level (parse time) AND inside every
# function. Replacing the whole file is safer than patching individual lines.

LB_STUB = '''\
class_name Board extends Node

# Mobile stub — leaderboards require GodotSteam (PC-only).
# All public methods are silent no-ops so the rest of the project compiles.

@export var ach : Achievement
@export var crt : CRT
@export var save : SaveFileManager
@export var display_instances : Array[Label3D]
@export var display_instances_alt : Array[Node3D]
var display_instances_act = []
@export var display_overview : Node3D
@export var text_globalpos : Label3D
@export var nocon : Node3D
@export var lock : Node3D
var leaderboard_handle = 0
var details_max: int = 0
var activeArray = []
var active_result_array = []
var active_entry_count = 0

func _ready():
\tdisplay_instances_act = display_instances
\tClearDisplay()

func _process(_delta):
\tpass

func PassLeaderboard(_range1: int, _range2: int, _alias: String):
\tpass

var initialsetup = false
var active_alias = ""
var active_range1 = 0
var active_range2 = 0
func SetupLeaderboard():
\tpass

func Timeout(_s: bool):
\tpass

func ClearDisplay():
\tif display_overview: display_overview.visible = false
\tif text_globalpos: text_globalpos.text = ""
\tfor disp in display_instances_act:
\t\tvar score : Label3D = disp.get_child(0)
\t\tdisp.text = ""
\t\tscore.text = ""

func TurnOffDisplay():
\tpass

func UpdateDisplay():
\tpass

@export var stat_shotsFired : Label3D
@export var stat_shellsEjected : Label3D
@export var stat_doorsKicked : Label3D
@export var stat_cigSmoked : Label3D
@export var stat_roundsBeat : Label3D
@export var stat_mlDrank : Label3D
@export var stat_totalCash : Label3D
func UpdateStats():
\tif not FileAccess.file_exists(save.savePath_stats): return
\tvar file = FileAccess.open(save.savePath_stats, FileAccess.READ)
\tvar temp_data = file.get_var()
\tif stat_shotsFired: stat_shotsFired.text = str(temp_data.shots_fired)
\tif stat_shellsEjected: stat_shellsEjected.text = str(temp_data.shells_ejected)
\tif stat_doorsKicked: stat_doorsKicked.text = str(temp_data.doors_kicked)
\tif stat_cigSmoked: stat_cigSmoked.text = str(temp_data.cigs_smoked)
\tif stat_roundsBeat: stat_roundsBeat.text = str(temp_data.rounds_beat)
\tif stat_mlDrank: stat_mlDrank.text = str(temp_data.ml_drank)
\tif stat_totalCash: stat_totalCash.text = str(temp_data.total_cash)

func GetLeaderboard():
\tpass

func UploadScore_Deprecated(_rounds_beat, _visible_score, _initial_score):
\tpass

func UploadScore(_rounds_beat, _visible_score, _initial_score):
\tpass

func DownloadEntries(_range1: int, _range2: int, _alias: String):
\tpass

func val2compressed(val):
\tvar accuracy_bits = 17
\tvar a = max(0, floor(log(val) / log(2)) + 1 - accuracy_bits)
\tif 2**accuracy_bits * (2**a - 1) > val: a -= 1
\tvar b = (val - 2**accuracy_bits * (2**a - 1)) / (2**a)
\treturn floor((a * 2**accuracy_bits) + b)
'''

with open("scripts/LeaderboardManager.gd", "w", encoding="utf-8") as f:
    f.write(LB_STUB)
print("Patched scripts/LeaderboardManager.gd → mobile stub")

# ── AchievementManager.gd — guard Steam calls ─────────────────────────────────
# Already guarded by `if GlobalVariables.using_steam` but let's be safe.
ACH_STUB = '''\
class_name Achievement extends Node

# Mobile stub — achievements require GodotSteam (PC-only).
func UnlockAchievement(_apiname: String):
\tpass

func ClearAchievement(_apiname: String):
\tpass
'''

with open("scripts/AchievementManager.gd", "w", encoding="utf-8") as f:
    f.write(ACH_STUB)
print("Patched scripts/AchievementManager.gd → mobile stub")

print("mobile_patch.py done.")
