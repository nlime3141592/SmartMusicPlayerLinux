const c_METHOD_GET = "GET"
const c_METHOD_POST = "POST"

const c_DEFAULT_METHOD = "GET"
const c_DEFAULT_HEADERS = {}
const c_DEFAULT_BODY = undefined

document.getElementById("btn_music_next").onclick = async () =>
{
    let response = await fetch("/music/control/next", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}

document.getElementById("btn_music_prev").onclick = async () =>
{
    let response = await fetch("/music/control/prev", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}

document.getElementById("btn_music_shuffle").onclick = async () =>
{
    let response = await fetch("/music/control/change_shuffle", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}

document.getElementById("btn_music_loop").onclick = async () =>
{
    let response = await fetch("/music/control/change_loop", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}

document.getElementById("btn_music_like").onclick = async () =>
{
    let response = await fetch("/music/control/toggle_like", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}

document.getElementById("btn_music_vol_up").onclick = async () =>
{
    let response = await fetch("/music/control/volup", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}

document.getElementById("btn_music_vol_down").onclick = async () =>
{
    let response = await fetch("/music/control/voldown", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}

document.getElementById("btn_music_vol_mute").onclick = async () =>
{
    let response = await fetch("/music/control/volmute", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}

document.getElementById("btn_music_play").onclick = async () =>
{
    let response = await fetch("/music/control/toggle_playing", {
        method: c_METHOD_POST,
        headers: c_DEFAULT_HEADERS,
        body: c_DEFAULT_BODY
    })

    musicPlayerStatus = response.json()
}
