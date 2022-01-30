interface DisplayProps {
    track: Spotify.Track
}

export default function DisplayPlayer(props: DisplayProps): JSX.Element {
    return (
        <div>
            <p>{props.track.name}</p>
            <div>
                {props.track.artists.map((artist, key) => (
                    <p key={key}>{artist.name}</p>
                ))}
            </div>
        </div>
    )
}
