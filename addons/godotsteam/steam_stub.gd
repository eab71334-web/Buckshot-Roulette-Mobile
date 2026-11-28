extends Node
## Mobile stub for GodotSteam — all calls are silent no-ops.
## Registered as the "Steam" autoload so every script that uses Steam.*
## compiles and runs without errors on iOS / Android.

# ── Constants ─────────────────────────────────────────────────────────────────
const LOBBY_TYPE_PUBLIC            = 2
const LOBBY_TYPE_FRIENDS_ONLY      = 1
const LOBBY_DISTANCE_FILTER_CLOSE  = 0
const LOBBY_DISTANCE_FILTER_FAR    = 2
const LOBBY_DISTANCE_FILTER_WORLDWIDE = 3

const CHAT_ROOM_ENTER_RESPONSE_SUCCESS          = 1
const CHAT_ROOM_ENTER_RESPONSE_DOESNT_EXIST     = 2
const CHAT_ROOM_ENTER_RESPONSE_NOT_ALLOWED      = 3
const CHAT_ROOM_ENTER_RESPONSE_FULL             = 4
const CHAT_ROOM_ENTER_RESPONSE_ERROR            = 5
const CHAT_ROOM_ENTER_RESPONSE_BANNED           = 6
const CHAT_ROOM_ENTER_RESPONSE_LIMITED          = 7
const CHAT_ROOM_ENTER_RESPONSE_CLAN_DISABLED    = 8
const CHAT_ROOM_ENTER_RESPONSE_COMMUNITY_BAN    = 9
const CHAT_ROOM_ENTER_RESPONSE_MEMBER_BLOCKED_YOU    = 10
const CHAT_ROOM_ENTER_RESPONSE_YOU_BLOCKED_MEMBER    = 11

const CHAT_MEMBER_STATE_CHANGE_ENTERED = 1
const CHAT_MEMBER_STATE_CHANGE_LEFT    = 2
const CHAT_MEMBER_STATE_CHANGE_BANNED  = 8
const CHAT_MEMBER_STATE_CHANGE_KICKED  = 4

const LEADERBOARD_DATA_REQUEST_GLOBAL             = 0
const LEADERBOARD_DATA_REQUEST_GLOBAL_AROUND_USER = 1
const LEADERBOARD_DATA_REQUEST_FRIENDS            = 2

# ── Signals (declared so .connect() calls don't crash) ────────────────────────
signal lobby_created(result, lobby_id)
signal lobby_joined(lobby_id, permissions, locked, response)
signal lobby_match_list(lobbies)
signal lobby_chat_update(lobby_id, change_id, making_change_id, chat_state)
signal join_requested(lobby_id, friend_id)
signal persona_state_change(steam_id, flags)
signal avatar_loaded(steam_id, size, buffer)
signal leaderboard_find_result(handle, found)
signal leaderboard_score_uploaded(success, handle, score)
signal leaderboard_scores_downloaded(message, handle, result)

# ── Methods — all no-ops ──────────────────────────────────────────────────────
func steamInit(_retrieve_stats: bool = true) -> Dictionary:
	return {"status": 0, "verbal": "Steam stub — mobile build"}

func run_callbacks() -> void:
	pass

func loggedOn() -> bool:
	return false

func getSteamID() -> int:
	return 0

func getPersonaName() -> String:
	return "Player"

func getFriendPersonaName(_steam_id: int) -> String:
	return "Player"

func isSteamRunningOnSteamDeck() -> bool:
	return false

func getPlayerAvatar(_size: int = 1, _steam_id: int = 0) -> void:
	pass

# Lobby
func createLobby(_type: int, _max_members: int) -> void:
	pass

func joinLobby(_lobby_id: int) -> void:
	pass

func leaveLobby(_lobby_id: int) -> void:
	pass

func setLobbyType(_lobby_id: int, _type: int) -> bool:
	return false

func setLobbyJoinable(_lobby_id: int, _joinable: bool) -> bool:
	return false

func setLobbyMemberLimit(_lobby_id: int, _max: int) -> bool:
	return false

func setLobbyData(_lobby_id: int, _key: String, _value: String) -> bool:
	return false

func getLobbyData(_lobby_id: int, _key: String) -> String:
	return ""

func getLobbyOwner(_lobby_id: int) -> int:
	return 0

func getNumLobbyMembers(_lobby_id: int) -> int:
	return 0

func getLobbyMemberByIndex(_lobby_id: int, _index: int) -> int:
	return 0

func requestLobbyList() -> void:
	pass

func addRequestLobbyListResultCountFilter(_count: int) -> void:
	pass

func addRequestLobbyListDistanceFilter(_filter: int) -> void:
	pass

func activateGameOverlayInviteDialog(_lobby_id: int) -> void:
	pass

# Packets
func sendP2PPacket(_steam_id: int, _data, _send_type: int = 0, _channel: int = 0) -> bool:
	return false

func readP2PPacket(_packet_size: int, _channel: int = 0) -> Dictionary:
	return {}

func getAvailableP2PPacketSize(_channel: int = 0) -> int:
	return 0

func acceptP2PSessionWithUser(_steam_id: int) -> bool:
	return false

func closeP2PSessionWithUser(_steam_id: int) -> bool:
	return false

func allowP2PPacketRelay(_allow: bool) -> void:
	pass

# Achievements / stats
func setAchievement(_api_name: String) -> bool:
	return false

func clearAchievement(_api_name: String) -> bool:
	return false

func storeStats() -> bool:
	return false

# Leaderboards
func setLeaderboardDetailsMax(_max: int) -> int:
	return _max

func findLeaderboard(_name: String) -> void:
	pass

func uploadLeaderboardScore(_score: int, _keep_best: bool = true,
		_details: Array = [], _handle: int = 0) -> void:
	pass

func downloadLeaderboardEntries(_start: int, _end: int,
		_request_type: int = 0, _handle: int = 0) -> void:
	pass

func getLeaderboardEntryCount(_handle: int) -> int:
	return 0
