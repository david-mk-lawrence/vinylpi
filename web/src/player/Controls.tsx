interface ControlsProps {
    player: Spotify.Player
    paused: boolean
}

export default function ControlsPlayer(props: ControlsProps): JSX.Element {
    const onPlay = (_: React.MouseEvent<HTMLButtonElement>) => {
        props.player.togglePlay()
    }
    const onPrev = (_: React.MouseEvent<HTMLButtonElement>) => {
        props.player.previousTrack()
    }
    const onNext = (_: React.MouseEvent<HTMLButtonElement>) => {
        props.player.nextTrack()
    }

    return (
        <>
            <button onClick={onPrev} >
                &lt;&lt;
            </button>

            <button onClick={onPlay} >
                { props.paused ? "Play" : "Pause" }
            </button>

            <button onClick={onNext} >
                &gt;&gt;
            </button>
        </>
    )
}
