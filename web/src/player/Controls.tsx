import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

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
        <div>
            <button onClick={onPrev} >
                <FontAwesomeIcon icon="step-backward" />
            </button>

            <button onClick={onPlay} >
                { props.paused ? <FontAwesomeIcon icon="play" /> : <FontAwesomeIcon icon="pause" /> }
            </button>

            <button onClick={onNext} >
                <FontAwesomeIcon icon="step-forward" />
            </button>
        </div>
    )
}
