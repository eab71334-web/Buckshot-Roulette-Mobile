"""
Patches the project for mobile export by replacing Steam-dependent scripts
with no-op stubs. Run before Godot export on the build machine.
"""
import os, re

# ── Steam.gd → no-op stub ─────────────────────────────────────────────────────
# The original calls Steam.loggedOn() / getSteamID() / run_callbacks() etc.
# which come from the GodotSteam native plugin (not available on iOS/Android).
# Replace the whole file with a stub that keeps the same public API so the
# rest of the code (GlobalSteam.*) compiles without errors.

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
\tprint("Steam stub active (mobile build — Steam disabled)")

func _process(_delta: float) -> void:
\tpass

func InitializeSteam():
\tpass
'''

STEAM_PATH = "scripts/Steam.gd"
with open(STEAM_PATH, "w", encoding="utf-8") as f:
    f.write(STEAM_STUB)
print(f"Patched {STEAM_PATH} → mobile stub")

# ── LeaderboardManager.gd — guard every Steam.* call ─────────────────────────
# The class-level `var details_max: int = Steam.setLeaderboardDetailsMax(2)`
# runs at parse time and crashes even before _ready(). Replace with 0.

LB_PATH = "scripts/LeaderboardManager.gd"
text = open(LB_PATH, encoding="utf-8").read()
patched = re.sub(
    r'var details_max\s*:\s*int\s*=\s*Steam\.setLeaderboardDetailsMax\(\d+\)',
    'var details_max: int = 0  # Steam stub (mobile)',
    text, count=1
)
if patched != text:
    open(LB_PATH, "w", encoding="utf-8").write(patched)
    print(f"Patched {LB_PATH} → removed Steam.setLeaderboardDetailsMax at class level")
else:
    print(f"{LB_PATH} — no class-level Steam call found, skipped")
