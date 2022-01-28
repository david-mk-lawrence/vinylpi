import React, { useEffect, useState, useCallback } from "react"
import axios from "axios"

import Display from "./Display"
import Controls from "./Controls"
import Playback from "./Playback"
import { Device } from "./types"

interface WebPlayerProps {
    token: string
}

const getDevice = async (): Promise<Device | undefined> => {
    const resp = await axios.get(process.env.REACT_APP_API_URL + "/device")
    if (resp.data && resp.data.error) {
        throw new Error(resp.data.error)
    }
    return resp.data
}

const transferPlayback = async (devId: string): Promise<Device | undefined> => {
    const resp = await axios.get(process.env.REACT_APP_API_URL + `/transfer/${devId}`)
    if (resp.data.error) {
        throw new Error(resp.data.error)
    }
    return resp.data
}

export default function WebPlayer(props: WebPlayerProps): JSX.Element {
    const [player, setPlayer] = useState<Spotify.Player>()
    const [track, setTrack] = useState<Spotify.Track>()
    const [error, setError] = useState<Spotify.Error | Error>()
    const [paused, setPaused] = useState<boolean>(false)
    const [deviceId, setDeviceId] = useState<string>()
    const [currentDevice, setCurrentDevice] = useState<Device>()

    const handleNewDevice = useCallback((devId?: string, dev?: Device) => {
        setCurrentDevice(dev)
        if (!devId || (devId && dev?.id !== devId)) {
            setTrack(undefined)
        }
    }, [])

    const onTransfer = useCallback(async (_: React.MouseEvent<HTMLButtonElement>) => {
        if (deviceId) {
            try {
                const dev = await transferPlayback(deviceId)
                handleNewDevice(deviceId, dev)
            } catch (error: unknown) {
                setError(error as Error)
            }
        }
    }, [deviceId, handleNewDevice])

    useEffect(() => {
        const script = document.createElement("script")
        script.src = "https://sdk.scdn.co/spotify-player.js"
        script.async = true

        document.body.appendChild(script);

        return () => {
            script.remove()
        }
    }, [])

    useEffect(() => {
        window.onSpotifyWebPlaybackSDKReady = () => {
            const player = new window.Spotify.Player({
                name: process.env.REACT_APP_WEBPLAYER_NAME,
                getOAuthToken: cb => { cb(props.token); },
            })

            setPlayer(player)
        }
    }, [props.token])

    useEffect(() => {
        if (player) {
            player.on("account_error", (err) => {
                console.error("account_error", err)
            })

            player.on("autoplay_failed", () => {
                console.log("autoplay_failed")
            })

            player.on("ready", async (inst: Spotify.WebPlaybackInstance) => {
                setDeviceId(inst.device_id)
                try {
                    const dev = await getDevice()
                    handleNewDevice(inst.device_id, dev)
                } catch (error: unknown) {
                    setError(error as Error)
                }
            })

            player.on("not_ready", (inst: Spotify.WebPlaybackInstance) => {
                console.log("not_ready", inst)
            })

            player.on("authentication_error", (err) => {
                setError(err)
            })

            player.on("initialization_error", (err) => {
                setError(err)
            })

            player.on("playback_error", (err) => {
                setError(err)
            })

            player.connect()
        }

        return () => {
            player?.removeListener("account_error")
            player?.removeListener("ready")
            player?.removeListener("not_ready")
            player?.removeListener("authentication_error")
            player?.removeListener("initialization_error")
            player?.removeListener("playback_error")
            player?.disconnect()
        }
    }, [player, handleNewDevice])

    useEffect(() => {
        if (player) {
            player.on("player_state_changed", async (state: Spotify.PlaybackState) => {
                try {
                    const dev = await getDevice()
                    handleNewDevice(deviceId, dev)
                } catch (error: unknown) {
                    setError(error as Error)
                }

                if (state) {
                    const currentState = await player.getCurrentState()
                    if (currentState) {
                        setTrack(currentState.track_window.current_track)
                        setPaused(currentState.paused)
                    }
                }
            })
        }

        return () => {
            player?.removeListener("player_state_changed")
        }
    }, [player, deviceId, handleNewDevice])

    return (
        <div>
            {error && <p>Error: {error}</p>}
            {deviceId && <Playback deviceId={deviceId} currentDevice={currentDevice} onTransfer={onTransfer} />}
            {track &&
                <>
                    <Display track={track} />
                    {player && <Controls
                        player={player}
                        paused={paused}
                    />}
                </>
            }
        </div>
    )
}
