import React, { useEffect, useState } from "react"

interface WebPlayerProps {
    token: string
}

export default function WebPlayer(props: WebPlayerProps): JSX.Element {
    const [player, setPlayer] = useState<Spotify.Player>()
    const [track, setTrack] = useState<Spotify.Track>()
    const [error, setError] = useState<Spotify.Error>()
    const [paused, setPaused] = useState<boolean>(false)

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
                name: 'Web Playback SDK',
                getOAuthToken: cb => { cb(props.token); },
            })

            setPlayer(player)

            player.addListener('ready', ({ device_id }) => {
                console.log('Ready with Device ID', device_id);
            })

            player.addListener('not_ready', ({ device_id }) => {
                console.log('Device ID has gone offline', device_id);
            })

            player.addListener("authentication_error", (err) => {
                setError(err)
            })

            player.addListener("initialization_error", (err) => {
                setError(err)
            })

            player.addListener("playback_error", (err) => {
                setError(err)
            })

            player.addListener("player_state_changed", (state) => {
                if (!state) {
                    return
                }

                player.getCurrentState().then((currentState) => {
                    if (currentState) {
                        setTrack(currentState.track_window.current_track)
                        setPaused(currentState.paused)
                    }
                })
            })

            player.connect()
        }
    }, [props.token])

    const onPlay = (_: React.MouseEvent<HTMLButtonElement>) => {
        player?.togglePlay()
    }
    const onPrev = (_: React.MouseEvent<HTMLButtonElement>) => {
        player?.previousTrack()
    }
    const onNext = (_: React.MouseEvent<HTMLButtonElement>) => {
        player?.nextTrack()
    }

    if (error) {
        return <p>Error: {error}</p>
    }

    if (!track) {
        return <div>Nothing Playing</div>
    }

    if (!player) {
        return <div>No Player</div>
    }

    return (
        <div>
            <img src={track.album.images[0].url} alt="" />
            <div>
                <div>
                    {track.name}
                </div>
                <div>
                    {track.artists.map((artist, key) => (
                        <p key={key}>{artist.name}</p>
                    ))}
                </div>
            </div>
            <button onClick={onPrev} >
                &lt;&lt;
            </button>

            <button onClick={onPlay} >
                { paused ? "Play" : "Pause" }
            </button>

            <button onClick={onNext} >
                &gt;&gt;
            </button>
        </div>
    )
}
