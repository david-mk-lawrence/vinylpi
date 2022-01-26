interface DisplayProps {
    track: Spotify.Track
}

export default function DisplayPlayer(props: DisplayProps): JSX.Element {
    return (
        <>
            <img src={props.track.album.images[0].url} alt="" />
            <div>
                <div>
                    {props.track.name}
                </div>
                <div>
                    {props.track.artists.map((artist, key) => (
                        <p key={key}>{artist.name}</p>
                    ))}
                </div>
            </div>
        </>
    )
}
